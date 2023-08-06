import click
import os, sys
import logging

from nextcode.client import Client
from nextcode.exceptions import InvalidProfile
from .utils import console_handler, abort

help_string = """A utility for interfacing with WuXi Nextcode services.

This tool allows you to communicate with the pipelines service, CSA, workflow service and GOR Query API.
For all usage you will need to authenticate against the specific service profile you are using.

Please look at the subcommands below for details.
"""

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')
profile_check = False

class CLI(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        click.MultiCommand.__init__(self, *args, **kwargs)
        opt = click.Option(
            param_decls=["--verbose", "-v"],
            help='Output logs for debugging',
            type=click.Choice(['warning', 'error', 'info']),
        )
        self.params.append(opt)
        opt = click.Option(
            param_decls=["--profile", "-p"], help='Use a specific profile for this command'
        )
        self.params.append(opt)

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.startswith("__"):
                continue
            if filename.endswith('.py'):
                rv.append(filename[:-3])
            elif os.path.isdir(os.path.join(plugin_folder, filename)):
                rv.append(filename)
        rv.sort()

        return rv

    def get_command(self, ctx, name):
        # quick and dirty profile check
        global profile_check
        if not profile_check:
            profile_check = True
            try:
                _ = Client()
            except InvalidProfile:
                cmd = sys.argv[1] if len(sys.argv) > 1 else None
                if cmd not in ("profile", "version"):
                    click.secho("You need to add a profile with: nextcode profile add <name>", fg="yellow")

        ns = {}
        fn = os.path.join(plugin_folder, name)
        # if the command is a folder we look for the entrypoint in the __init__ file
        if os.path.isdir(fn):
            fn = os.path.join(fn, '__init__.py')
        else:
            fn = os.path.join(plugin_folder, name + '.py')

        if not os.path.exists(fn):
            abort("Command {} not found".format(name))

        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            # We are only passing our own code to eval
            # No unchecked external code should ever be passed to eval
            eval(code, ns, ns)  # nosec
        cmd = ns.get('cli', None)
        return cmd


class Context(object):
    def __init__(self):
        self.verbose = False
        self.profile_name = None
        self.home = os.getcwd()
        self.session = None
        self.service = None
        self.client = None


@click.command(cls=CLI, help=help_string)
@click.pass_context
def cli(ctx, verbose=None, profile=None):
    """Convert files using specified converter"""
    if ctx.obj is None:
        ctx.obj = Context()
        ctx.obj.verbose = verbose
        ctx.obj.profile_name = profile
        try:
            ctx.obj.client = Client(profile=profile)
        except InvalidProfile:
            pass

    # by default we log out to console WARN and higher but can view info with -v
    if verbose:
        console_handler.setLevel(getattr(logging, verbose.upper()))


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
