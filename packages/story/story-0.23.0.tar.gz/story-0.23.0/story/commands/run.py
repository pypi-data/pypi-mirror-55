# -*- coding: utf-8 -*-

import click

import emoji

from .. import cli


@cli.cli.command()
def run():
    """Write Storyscript, interactively."""
    click.echo('This command has not been implemented yet.')
    # cli.user()
    #
    # from storyscript import version
    # click.echo(
    #     click.style('Asyncy', fg='magenta') + ' ' +
    #     cli.version + click.style(' - ', dim=True) +
    #     click.style('Storyscript', fg='cyan') + ' ' +
    #     version
    # )
    #
    # from .repl.Repl import Repl
    # try:
    #     Repl().interact()
    #     click.echo(emoji.emojize(':waving_hand:  Goodbye.'))
    # except KeyboardInterrupt:
    #     click.echo(emoji.emojize(':waving_hand:  Goodbye.'))
