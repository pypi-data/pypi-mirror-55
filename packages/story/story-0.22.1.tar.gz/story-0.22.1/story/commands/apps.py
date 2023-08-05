# -*- coding: utf-8 -*-
import os
import sys

from blindspin import spinner

import click

import emoji

from .. import api
from .. import awesome
from .. import cli
from .. import options
from ..helpers import datetime


def maintenance(enabled: bool) -> str:
    if enabled:
        return 'in maintenance'
    else:
        return 'running'


@cli.cli.group()
def apps():
    """Create, list, and manage apps on Storyscript Cloud."""
    pass


@apps.command(name='list')
def list_command():
    """List apps that you have access to."""
    from texttable import Texttable

    cli.user()

    with spinner():
        res = api.Apps.list()

    count = 0
    # Heads up! Texttable does not like colours.
    # So don't use click.style here.
    table = Texttable(max_width=800)
    table.set_deco(Texttable.HEADER)
    table.set_cols_align(['l', 'l', 'l'])
    all_apps = [['NAME', 'STATE', 'CREATED']]
    for app in res:
        count += 1
        date = datetime.parse_psql_date_str(app['timestamp'])
        all_apps.append(
            [
                app['name'],
                maintenance(app['maintenance']),
                datetime.reltime(date)
            ]
        )

    table.add_rows(rows=all_apps)

    if count == 0:
        click.echo('No application found. Create your first app with')
        click.echo(click.style('$ story apps create', fg='magenta'))
    else:
        click.echo(table.draw())


@apps.command()
@click.argument('name', nargs=1, required=False)
@click.option(
    '--team', type=str, help='Team name that owns this new Application'
)
def create(name, team):
    """Create a new app."""

    cli.user()
    story_yaml = cli.find_story_yml()

    if story_yaml is not None:
        click.echo(
            click.style(
                'There appears to be a Storyscript Cloud project in '
                f'{story_yaml} already.\n',
                fg='red',
            )
        )
        click.echo(
            click.style(
                'Are you trying to deploy? ' 'Try the following:', fg='red'
            )
        )
        click.echo(click.style('$ story deploy', fg='magenta'))
        sys.exit(1)

    # _is_git_repo_good()

    name = name or awesome.new()

    # Sanity check.
    if len(name) < 4:
        click.echo(
            click.style(
                'The name you specified is too short. \n'
                'Please use at least 4 characters in your app name.',
                fg='red',
            )
        )
        sys.exit(1)

    click.echo('Creating application… ', nl=False)

    with spinner():
        api.Apps.create(name=name, team=team)

    click.echo(
        '\b' + click.style(emoji.emojize(':heavy_check_mark:'), fg='green')
    )

    create_story_yaml(name)


@apps.command()
@click.argument('name', nargs=1, required=True)
def init(name):
    story_yaml = cli.find_story_yml()

    if story_yaml is not None:
        click.echo(
            click.style(
                'There appears to be a Storyscript Cloud project in '
                f'{story_yaml} already.\n',
                fg='red',
            )
        )
        sys.exit(1)

    api.Apps.get_uuid_from_hostname(name)

    create_story_yaml(name)


def create_story_yaml(name):
    # click.echo('Adding git-remote... ', nl=False)
    # cli.run(f'git remote add asyncy https://git.asyncy.com/{name}')
    # click.echo(click.style(emoji.emojize(':heavy_check_mark:'), fg='green'))

    click.echo('Creating story.yml… ', nl=False)
    cli.settings_set(f'app_name: {name}\n', 'story.yml')

    click.echo(
        '\b' + click.style(emoji.emojize(':heavy_check_mark:'), fg='green')
    )

    click.echo('\nApp Name: ' + click.style(name, bold=True))
    click.echo(
        'App URL: '
        + click.style(f'https://{name}.storyscriptapp.com/', fg='blue')
        + '\n'
    )

    click.echo(
        'You are now ready to write your first Storyscript! '
        f'{emoji.emojize(":party_popper:")}'
    )
    click.echo()

    cli.track('App Created', {'App name': name})

    click.echo(' - [ ] Write a Story:')
    click.echo(
        '       $ '
        + click.style('story template http > http.story', fg='magenta')
    )
    click.echo()
    click.echo(' - [ ] Deploy to Storyscript Cloud:')
    click.echo('       $ ' + click.style('story deploy', fg='magenta'))
    click.echo()
    click.echo('We hope you enjoy your deployment experience!')


@apps.command()
@options.app()
def url(app):
    """Display the full URL of an app.

    Great to use with $(story apps url) in bash.
    """
    cli.user()
    print_nl = False

    if _isatty():
        print_nl = True

    click.echo(f'https://{app}.storyscriptapp.com/', nl=print_nl)


def _isatty():
    os.isatty(sys.stdout.fileno())


@apps.command('open')
@options.app()
def do_open(app):
    """Open the full URL of an app, in the browser."""
    cli.user()
    url = f'https://{app}.storyscriptapp.com/'

    click.echo(url)
    click.launch(url)
    sys.exit(0)


@apps.command()
@options.app()
@click.option(
    '--yes', '-y', is_flag=True, help='Assume yes to destruction confirmation.'
)
@click.option(
    '--all', is_flag=True, help='Destroy all Storyscript Cloud apps.'
)
def destroy(yes=False, app=None, all=False):
    """Destroy an app."""

    cli.user()

    if all:
        click.echo('Destroying all Storyscript Cloud applications:', err=True)
        apps = [app['name'] for app in api.Apps.list()]
    else:
        apps = [app]

    for app in apps:

        if yes or click.confirm(
            f'Do you want to destroy {app!r}?', abort=True
        ):
            click.echo(f'Destroying application {app!r}… ', nl=False)

            with spinner():
                api.Apps.destroy(app=app)
                cli.track('App Destroyed', {'App name': app})

            click.echo(
                '\b'
                + click.style(emoji.emojize(':heavy_check_mark:'), fg='green')
            )
            click.echo()

    sys.exit(0)
