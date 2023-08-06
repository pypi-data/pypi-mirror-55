import sys
import datetime
import click
from click import command, argument, pass_context, secho, echo
import requests
import logging
from tabulate import tabulate
from requests import codes
from urllib.parse import urljoin

import nextcode
from nextcode.utils import check_resp_error

from nextcodecli.utils import abort, dumps, print_tab

log = logging.getLogger(__name__)

CLIENT_ID = 'api-key-client'


def get_auth_server():
    client = nextcode.Client()
    root_url = client.profile.root_url
    auth_server = urljoin(root_url, "auth")
    r = requests.get(auth_server)
    # ! temporary hack because services are split between xxx.wuxi and xxx-cluster.wuxi
    if r.status_code == codes.not_found:
        if "-cluster" not in auth_server:
            lst = root_url.split(".", 1)
            auth_server = lst[0] + "-cluster" + lst[1]
        else:
            auth_server = auth_server.replace("-cluster", "")
    return auth_server


def find_user(ctx, user_name):
    users_url = ctx.obj.realm_url + 'users?username=%s' % (user_name)
    resp = ctx.obj.session.get(users_url)
    resp.raise_for_status()
    if not resp.json():
        return None
    user_id = resp.json()[0]['id']
    return user_id


def get_user_roles(ctx, user_id):
    """
    Get the realm roles for this user, ignoring client-specific roles
    """
    url = ctx.obj.realm_url + 'users/%s/role-mappings' % (user_id)
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    roles = resp.json()
    role_names = [r['name'] for r in roles.get('realmMappings', [])]
    return role_names


def test_user_login(ctx, user_name, password):
    # try logging in with the new user
    url = ctx.obj.realm_url + 'protocol/openid-connect/token'
    body = {
        'grant_type': 'password',
        'client_id': CLIENT_ID,
        'password': password,
        'username': user_name,
        'scope': 'offline_access',
    }
    url = url.replace("admin/", "")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    log.debug("Calling POST %s with headers %s and body %s", url, headers, body)
    resp = requests.post(url, headers=headers, data=body)
    check_resp_error(resp)


@click.group()
@click.option(
    '-u',
    '--username',
    default='admin',
    help="Administrator user in the keycloak instance",
    show_default=True,
)
@click.option(
    '-p',
    '--password',
    envvar='KEYCLOAK_PASSWORD',
    prompt=True,
    help="Password for administrator user",
    hide_input=True,
)
@click.option(
    '-r', '--realm', default='wuxinextcode.com', help="Keycloak realm to manage", show_default=True
)
@pass_context
def cli(ctx, username, password, realm):
    """
    Manage keycloak users

    Requires the keycloak admin password, which you can put into envivonment as KEYCLOAK_PASSWORD
    """
    auth_server = get_auth_server()
    log.info("Managing users on keycloak server %s..." % auth_server)
    # check if server is available
    try:
        resp = requests.get(auth_server + '/realms/%s' % realm)
    except requests.exceptions.ConnectionError:
        abort("Keycloak server %s is not reachable" % auth_server)
    if resp.status_code == requests.codes.not_found:
        abort("Realm '%s' was not found on keycloak server %s" % (realm, auth_server))
    check_resp_error(resp)

    url = auth_server + '/realms/master/protocol/openid-connect/token'
    headers_form = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(
        url,
        data='username=%s&password=%s&grant_type=password&client_id=admin-cli'
        % (username, password),
        headers=headers_form,
    )
    if resp.status_code != 200:
        abort(
            "Could not authenticate %s user against %s: %s"
            % (username, url, resp.json()['error_description'])
        )
    access_token = resp.json()['access_token']
    headers = {'Authorization': "Bearer %s" % access_token, 'Content-Type': 'application/json'}
    session = requests.Session()
    session.headers = headers
    ctx.obj.session = session
    ctx.obj.realm_url = auth_server + '/admin/realms/%s/' % (realm)
    ctx.obj.master_url = auth_server + '/admin/realms/master/'
    ctx.obj.realm = realm


@command(help="List all keycloak users in the realm")
@click.option('-r', '--raw', 'is_raw', is_flag=True, help='Dump raw json response')
@pass_context
def users(ctx, is_raw):
    url = ctx.obj.realm_url + 'users/'
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    if is_raw:
        echo(dumps(resp.json()))
        return
    fields = ['username', 'email', 'name', 'enabled', 'created']
    table = []
    for user in resp.json():
        table.append(
            [
                user['username'],
                user['email'],
                user.get('firstName', '') + ' ' + user.get('lastName', ''),
                user['enabled'],
                datetime.datetime.fromtimestamp(user['createdTimestamp'] // 1000),
            ]
        )
    tbl = tabulate(sorted(table), headers=fields)
    echo(tbl)


@command(help="View information about a keycloak user")
@argument('user_name', nargs=1)
@click.option('-r', '--raw', 'is_raw', is_flag=True, help='Dump raw json response')
@pass_context
def user(ctx, user_name, is_raw):
    user_id = find_user(ctx, user_name)
    if not user_id:
        abort("User '%s' not found in realm %s" % (user_name, ctx.obj.realm))

    users_url = ctx.obj.realm_url + 'users/%s' % (user_id)
    resp = ctx.obj.session.get(users_url)
    resp.raise_for_status()
    user = resp.json()

    url = ctx.obj.realm_url + 'users/%s/role-mappings' % (user_id)
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    roles = resp.json()

    if is_raw:
        echo(dumps(user))
        echo(dumps(roles))
        return
    print_tab('Username', user['username'])
    print_tab('Email', user['email'])
    print_tab('Enabled', user['enabled'])
    print_tab('Name', "%s %s" % (user.get('firstName') or '', user.get('lastName') or ''))
    print_tab('Created', datetime.datetime.fromtimestamp(user['createdTimestamp'] // 1000))
    if user.get('federatedIdentities'):
        print_tab('Federation', user['federatedIdentities'][0]['identityProvider'])
    else:
        print_tab('Federation', '(Local user)')
    role_names = get_user_roles(ctx, user_id)
    print_tab('Realm Roles', ', '.join(role_names))

    url = ctx.obj.realm_url + 'users/%s/role-mappings/realm/available' % (user_id)
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    available_roles = resp.json()
    if available_roles:
        echo(
            "\nThe following roles can be added to the user: %s"
            % ', '.join([r['name'] for r in available_roles])
        )


@command(help="Add a new keycloak user")
@argument('user_name', nargs=1)
@click.option('-p', '--new_password', help='Password for new user', prompt=True)
@pass_context
def add_user(ctx, user_name, new_password):
    user_id = find_user(ctx, user_name)
    if user_id:
        abort("User '%s' already exists." % (user_name))

    url = ctx.obj.realm_url + 'users/'
    data = {
        'username': user_name,
        'firstName': 'None',
        'lastName': 'None',
        'email': user_name,
        'enabled': True,
        'emailVerified': True,
    }
    resp = ctx.obj.session.post(url, json=data)
    resp.raise_for_status()
    user_id = find_user(ctx, user_name)

    url = ctx.obj.realm_url + 'users/%s/reset-password' % user_id
    data = {'type': 'password', 'temporary': False, 'value': new_password}
    resp = ctx.obj.session.put(url, json=data)
    resp.raise_for_status()

    log.info(
        "User '%s' has been created in realm '%s'. Trying to log in" % (user_name, ctx.obj.realm)
    )
    test_user_login(ctx, user_name, new_password)
    echo("Success! User has been created. Please use the following authentication information:\n")
    echo(
        "Username: %s\nPassword: %s"
        % (click.style(user_name, bold=True), click.style(new_password, bold=True))
    )
    echo("")


@command(help="Reset the password of a keycloak user")
@argument('user_name', nargs=1)
@click.option('-p', '--new_password', help='Password for new user', prompt=True)
@pass_context
def reset_password(ctx, user_name, new_password):
    user_id = find_user(ctx, user_name)
    if not user_id:
        abort("User '%s' not found." % (user_name))

    url = ctx.obj.realm_url + 'users/%s/reset-password' % user_id
    data = {'type': 'password', 'temporary': False, 'value': new_password}
    resp = ctx.obj.session.put(url, json=data)
    resp.raise_for_status()

    log.info(
        "Password for user '%s' in realm '%s' has been reset. Trying to log in"
        % (user_name, ctx.obj.realm)
    )
    test_user_login(ctx, user_name, new_password)
    echo("Password has been reset. Please use the following authentication information:\n")
    echo(
        "Username: %s\nPassword: %s"
        % (click.style(user_name, bold=True), click.style(new_password, bold=True))
    )
    echo("")


@command(help="Remove a keycloak user")
@argument('user_name', nargs=1)
@pass_context
def remove_user(ctx, user_name):
    user_id = find_user(ctx, user_name)
    if not user_id:
        abort("User '%s' not found." % (user_name))

    url = ctx.obj.realm_url + 'users/%s' % user_id
    resp = ctx.obj.session.delete(url)
    check_resp_error(resp)
    echo("User '%s' has been deleted from realm '%s'" % (user_name, ctx.obj.realm))


@command(help="Add a new role to a keycloak user")
@argument('user_name', nargs=1)
@argument('role_name', nargs=1)
@pass_context
def add_role(ctx, user_name, role_name):
    role_name = role_name.lower()
    user_id = find_user(ctx, user_name)
    if not user_id:
        abort("User '%s' not found in realm %s" % (user_name, ctx.obj.realm))
    user_roles = get_user_roles(ctx, user_id)
    if role_name in user_roles:
        abort("User '%s' already has role '%s'" % (user_name, role_name))

    url = ctx.obj.realm_url + 'users/%s/role-mappings/realm/available' % (user_id)
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    available_roles = resp.json()
    role = None
    for r in available_roles:
        if r['name'].lower() == role_name:
            role = r
            break
    if not role:
        abort("Role '%s' is not available for user '%s'" % (role_name, user_name))

    url = ctx.obj.realm_url + 'users/%s/role-mappings/realm' % (user_id)
    resp = ctx.obj.session.post(url, json=[role])
    check_resp_error(resp)
    secho(
        "Role '%s' has been added to user '%s' in realm '%s'"
        % (role_name, user_name, ctx.obj.realm),
        bold=True,
        fg='green',
    )


@command(help="Remove a role from a keycloak user")
@argument('user_name', nargs=1)
@argument('role_name', nargs=1)
@pass_context
def remove_role(ctx, user_name, role_name):
    role_name = role_name.lower()
    user_id = find_user(ctx, user_name)
    if not user_id:
        abort("User '%s' not found in realm %s" % (user_name, ctx.obj.realm))

    url = ctx.obj.realm_url + 'users/%s/role-mappings' % (user_id)
    resp = ctx.obj.session.get(url)
    resp.raise_for_status()
    roles = resp.json()['realmMappings']
    role = None
    for r in roles:
        if r['name'].lower() == role_name:
            role = r
            break
    if not role:
        abort("User '%s' does not have role '%s'" % (user_name, role_name))

    url = ctx.obj.realm_url + 'users/%s/role-mappings/realm' % (user_id)
    resp = ctx.obj.session.delete(url, json=[role])
    check_resp_error(resp)
    secho(
        "Role '%s' has been removed from user '%s' in realm '%s'"
        % (role_name, user_name, ctx.obj.realm),
        bold=True,
        fg='green',
    )


cli.add_command(users)
cli.add_command(user)
cli.add_command(add_user)
cli.add_command(remove_user)
cli.add_command(reset_password)
cli.add_command(add_role)
cli.add_command(remove_role)
