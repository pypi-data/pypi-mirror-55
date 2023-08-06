"""Define functionality for manipulating the configuration.
"""

import pathlib

import click

from arbory.const import KW_CONF_SEL


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Display current configuration name."""
    if ctx.invoked_subcommand is None:
        cfg = ctx.obj['config']
        click.echo('Current configuration: {}'.format(
            cfg['DEFAULT'][KW_CONF_SEL]))


@config.command(context_settings=CONTEXT_SETTINGS)
@click.argument('conf_name')
@click.pass_obj
def use(obj, conf_name):
    """Specify a configuration to use."""
    cfg = obj['config']
    if conf_name in cfg:
        cfg['DEFAULT'][KW_CONF_SEL] = conf_name
        with open(pathlib.Path('arbory') / 'config.ini', 'w') as cf:
            cfg.write(cf)
        click.echo('Configuration selected: {}'.format(conf_name))
    else:
        click.echo('{!r} does not exist.'.format(conf_name))


@config.command(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def available(obj):
    """List all available configurations."""
    output = []
    for conf in obj['config']:
        output.append(conf)
    click.echo('\n'.join(output))


@config.command(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def options(obj):
    """List all configuration options."""
    output = []
    for opt in obj['config']['DEFAULT']:
        if opt != KW_CONF_SEL:
            output.append(opt)
    click.echo('\n'.join(output))
