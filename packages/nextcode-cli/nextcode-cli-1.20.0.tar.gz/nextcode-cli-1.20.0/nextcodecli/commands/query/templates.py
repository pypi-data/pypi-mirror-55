#!/usr/bin/env python
import click
import sys
import collections
from tabulate import tabulate
import dateutil
import yaml
from pathlib import Path

from nextcode.exceptions import ServerError

from ...utils import print_tab, dumps, get_logger, abort

log = get_logger(name='commands.query', level='INFO')


def fmt_date(dt):
    return dateutil.parser.parse(dt).strftime("%Y-%m-%d %H:%M")


@click.group(help="Query Template management")
def templates():
    pass


@templates.command()
@click.option('-o', '--organization', help="The organization to show templates for")
@click.option('-c', '--category', help="Category for templates")
@click.option(
    '--raw', 'is_raw', is_flag=True, default=False, help='Raw JSON response from endpoint'
)
@click.pass_context
def list(ctx, organization, category, is_raw):
    """

    """
    svc = ctx.obj.service
    all_templates = svc.get_templates(organization=organization, category=category)
    template_list = []
    for name, templ in all_templates.items():
        full_name = templ['full_name']
        template_list.append(
            [
                templ['id'],
                templ['name'],
                templ['version'],
                full_name,
                fmt_date(templ['create_date']),
                templ['list_description'],
            ]
        )

    tbl = tabulate(
        template_list, headers=['id', 'name', 'version', 'full_name', 'date', 'description']
    )
    click.echo(tbl)


@templates.command()
@click.argument('name', nargs=1)
@click.pass_context
def delete(ctx, name):
    """
    Delete a template by full name (e.g. [org]/[category]/[name]/[version])
    """
    svc = ctx.obj.service
    try:
        template = svc.get_template(name)
    except ServerError:
        abort("Template {} not found".format(name))
    try:
        # !TODO: Add support in SDK
        _ = svc.session.delete(template["links"]["self"])
    except ServerError as e:
        abort(e)
    click.secho("Template '%s' has been deleted." % (name), bold=True)


@templates.command()
@click.argument('name', nargs=1)
@click.option(
    '--raw', 'is_raw', is_flag=True, default=False, help='Raw JSON response from endpoint'
)
@click.option('--yaml', 'is_yaml', is_flag=True, default=False, help='Raw yaml template')
@click.option('--args', 'is_args', is_flag=True, default=False, help='View arguments')
@click.pass_context
def view(ctx, name, is_raw, is_yaml, is_args):
    svc = ctx.obj.service
    try:
        template = svc.get_template(name)
    except ServerError:
        abort("Template {} not found".format(name))

    if is_yaml:
        click.echo(template["file_contents"])
        return

    if is_args:
        if is_raw:
            click.echo(dumps(template['arguments']))
            return
        args_list = []
        for arg in template['arguments']:
            args_list.append(
                [
                    arg['name'],
                    arg.get('type'),
                    arg.get('optional'),
                    ", ".join(arg.get('values', [])),
                    arg.get('default', "")[:50],
                ]
            )
        args_list.sort()
        tbl = tabulate(args_list, headers=['name', 'type', 'optional', 'values', 'default'])
        click.echo(tbl)
        return
    if is_raw:
        click.echo(dumps(template))
        return
    print_tab('Template ID', template['id'])
    print_tab('Name', template['name'])
    print_tab('Organization', template['organization'])
    print_tab('Category', template['category'])
    print_tab('Date Created', fmt_date(template['create_date']))
    print_tab('Version', template['version'])
    print_tab('Description', template['list_description'])
    args = []
    for arg in template['arguments']:
        if not arg['optional']:
            args.append(arg['name'])
    print_tab('Required Arguments', ", ".join(args))
    print_tab('Perspectives', ", ".join([p['name'] for p in template['perspectives']]))


@templates.command()
@click.argument('filename', nargs=1)
@click.option('--replace', is_flag=True, default=False, help='Delete and replace existing template')
@click.pass_context
def add(ctx, filename, replace):
    """Add a new template from yaml file.
    """
    svc = ctx.obj.service
    session = svc.session
    p = Path(filename)
    if not p.exists():
        abort("File '%s' not found" % p)
    with p.open() as f:
        yaml_string = f.read()
    try:
        contents = yaml.safe_load(yaml_string)
        if not isinstance(contents, dict):
            raise Exception("Contents is not a dictionary")
    except Exception as ex:
        abort("Yaml is invalid: %s" % ex)
    name = next(iter(contents))
    click.echo("Uploading template '%s'..." % name)
    url = session.url_from_endpoint('templates')
    try:
        resp = session.post(url, json={'yaml': yaml_string})
    except ServerError as ex:
        if ex.response['code'] == 409:
            if replace:
                err = ex.response['error']
                click.echo("Template already exists with ID %s. Replacing..." % err['template_id'])
                try:
                    resp = session.delete(err['template_url'])
                    resp.raise_for_status()
                    resp = session.post(url, json={'yaml': yaml_string})
                    resp.raise_for_status()
                except ServerError as ex:
                    abort(ex)
            else:
                abort("Template '%s' already exists" % name)
        else:
            abort(ex)

    full_name = resp.json()['full_name']
    click.secho(
        "Template '%s' (%s) has been successfully added" % (full_name, resp.json()['id']), bold=True
    )
    click.echo("View the template with: nextcode query templates view %s" % full_name)


@templates.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('name', nargs=1)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def render(ctx, name, args):
    """Render a query from template
    """
    svc = ctx.obj.service
    try:
        template = svc.get_template(name)
    except ServerError:
        abort("Template {} not found".format(name))

    args_txt = "&".join(args)
    render_url = template['links']['render']
    if args_txt:
        render_url += "?" + args_txt
    click.echo("Calling %s" % render_url)
    try:
        # !TODO: Add support in SDK
        resp = svc.session.get(render_url, headers={"Accept": "text/plain"})
    except ServerError as ex:
        if "Missing arguments" in str(ex):
            click.secho(str(ex), fg='red')
            click.echo(
                "Hint: You can view arguments for this template with: nextcode query templates view %s --args"
                % name
            )
            sys.exit(1)
        else:
            abort(ex)
    print(resp.text)
