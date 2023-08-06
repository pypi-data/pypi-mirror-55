#!/usr/bin/env python

import os
import sys

import click
from click import pass_context, command, option, secho, echo
import requests
import logging
from nextcodecli.utils import dumps

log = logging.getLogger(__name__)


@command()
@option('-u', '--username')
@option('-p', '--password')
@option('-r', '--realm', default='wuxinextcode.com')
@option(
    '-h',
    '--host',
    default=None,
    help="Host override if not using profile, e.g. platform.wuxinextcodedev.com",
)
@option(
    '-t',
    '--token',
    'is_token',
    is_flag=True,
    help="Return access tokens as json instead of writing into current profile",
)
@pass_context
def cli(ctx, username, password, realm, host, is_token):
    """
    Authenticate against keycloak.
    """
    if not is_token:
        echo("Authenticating for profile %s..." % config.profile)
    # create empty files for tokens
    if not os.path.exists(config.token_files['refresh_token']):
        open(config.token_files['refresh_token'], 'a').close()
    open(config.token_files['access_token'], 'w').close()

    if username and password:
        if not is_token:
            echo("Authenticating from commandline parameters")
        client_id = 'api-key-client'
        body = {
            'grant_type': 'password',
            'client_id': client_id,
            'password': password,
            'username': username,
            'scope': 'offline_access',
        }
        if host:
            auth_server = "https://%s/auth" % host
        else:
            auth_server = config.get_profile_config()['auth_server']
        log.info("Using auth server '%s'" % auth_server)
        url = '%s/realms/%s/protocol/openid-connect/token' % (auth_server, realm)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        log.debug("Calling POST %s with headers %s and body %s", url, headers, body)
        resp = requests.post(url, headers=headers, data=body)
        log.debug("Response (%s): %s", resp.status_code, resp.text)
        if resp.status_code != 200:
            click.secho("Error logging in: %s" % resp.text, fg='red')
            sys.exit(1)
        if is_token:
            echo(dumps(resp.json()))
            return
        with open(config.token_files['refresh_token'], 'w') as f:
            f.write(resp.json()['refresh_token'])
        echo("You have been logged in")
    else:
        if host:
            login_server = "https://%s/api-key-service" % host
        else:
            login_server = config.get_profile_config()['login_server']

        if login_server:
            echo("Launching login webpage ==> Please authenticate and then press continue.")
            click.launch(login_server)
            click.pause()
        else:
            click.secho(
                "No login server configured. Please aquire a refresh_token from "
                "somewhere manually.",
                fg='yellow',
            )

        if 'EDITOR' not in os.environ and not config.editor:
            echo(
                "Paste the Refresh token from the webpage into the following file: %s"
                % config.token_files['refresh_token']
            )
        else:
            echo(
                "Your default editor has been opened on the refresh_token file. "
                "Please paste the refresh_token in it and save it. Close the file in your editor"
                " to continue."
            )
            click.edit(
                filename=config.token_files['refresh_token'],
                require_save=True,
                editor=config.editor,
            )
            config.load_tokens()
            click.secho("You have been logged in", fg='green')
