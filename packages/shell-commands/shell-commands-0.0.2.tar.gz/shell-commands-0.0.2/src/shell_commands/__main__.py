import json
import os
import subprocess
from pathlib import Path
from typing import List, Optional

import click
import logging

import pwd

import click_log
from tabulate import tabulate

from shell_commands.commands import CommandRepository, CommandData
from shell_commands.packages import PackageRepository

logger = logging.getLogger('commands')
click_log.basic_config(logger)


def run_as_user(command: List[str], user: str, cwd: Optional[str]=None):
    current_user = pwd.getpwuid(os.getuid()).pw_name
    actual_command = []
    if user != current_user:
        actual_command.extend(['sudo', '-u', user])
    actual_command.extend(command)
    subprocess.check_call(actual_command, cwd=cwd)


class App(CommandRepository, PackageRepository):

    def __init__(self, config_dir: Path):
        super(App, self).__init__()
        self.config_dir = config_dir
        if not config_dir.exists():
            self.config_dir.mkdir(mode=0o755, parents=True)
        self.dbfile = self.config_dir / 'db.json'
        if not self.dbfile.exists():
            self._write({'schemaVersion': 2, 'commands': {}, 'packages': []})

    def _load(self) -> dict:
        with self.dbfile.open('r') as fp:
            data = json.load(fp)
        assert 'schemaVersion' in data
        if data['schemaVersion'] == 1:
            # Upgrade from schema 1 to 2
            data['packages'] = []
            data['schemaVersion'] = 2
            self._write(data)
        assert data['schemaVersion'] == 2
        return data

    def _write(self, data: dict):
        with self.dbfile.open('w') as fp:
            json.dump(data, fp, indent=2)

    def save_command(self, name: str, user: str, cwd: str, command: List[str]):
        data = self._load()
        assert name not in data['commands'], 'Command with this name already exists'
        data['commands'][name] = {
            'user': user,
            'cwd': cwd,
            'command': command,
        }
        self._write(data)

    def get_command(self, name: str) -> CommandData:
        data = self._load()
        assert name in data['commands'], 'Command with this name does not exist'
        user = data['commands'][name]['user']
        cwd = data['commands'][name]['cwd']
        command = data['commands'][name]['command']
        return CommandData(name=name, user=user, cwd=cwd, command=command)

    def get_all_commands(self) -> List[CommandData]:
        return [self.get_command(name) for name in self._load()['commands'].keys()]

    def delete_command(self, name: str):
        data = self._load()
        assert name in data['commands'], 'Command with this name does not exist'
        del data['commands'][name]
        self._write(data)

    def require_package(self, name: str):
        data = self._load()
        assert name not in data['packages'], 'Package is already required so cannot require again'
        data['packages'].append(name)
        self._write(data)

    def get_required_packages(self) -> List[str]:
        data = self._load()
        return data['packages']
    def unrequire_package(self, name: str):
        data = self._load()
        assert name in data['packages'], 'Package is not required so cannot unrequire'
        data['packages'].remove(name)
        self._write(data)




@click.group(help='Utility for maintaining and using a carefully curated list of personal commands')
@click_log.simple_verbosity_option(logger)
@click.pass_context
def main(ctx: click.Context):
    config_dir = Path(click.get_app_dir('commands'))
    ctx.obj = App(config_dir)


@main.command(help='Save a command with given name', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_obj
@click.option('--user', '-u', help='User as which this command should be run, defaults to current user', default=None)
@click.option('--cwd', '-c', type=click.Path(dir_okay=True, exists=True), help='Working directory for this command, defaults to current directory')
@click.argument('name', type=click.STRING, nargs=1)
@click.argument('command', type=click.UNPROCESSED, nargs=-1)
def save(app: App, user: Optional[str], cwd: Optional[str], name: str, command: List[str]):
    if user is None:
        user = pwd.getpwuid(os.getuid()).pw_name
    if cwd is None:
        cwd = os.getcwd()
    logger.info('Saving a command:')
    logger.info('Name:    {}'.format(name))
    logger.info('Cwd:     {}'.format(cwd))
    logger.info('User:    {}'.format(user))
    logger.info('Command: {!r}'.format(command))
    app.save_command(name=name, user=user, cwd=cwd, command=command)


@main.command(help='Run a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def run(app: App, name: str):
    data = app.get_command(name)
    run_as_user(data.command, data.user, data.cwd)


@main.command(help='List all commands')
@click.pass_obj
def list(app: App):
    header = ['name', 'user', 'cwd', 'command']
    data = [(d.name, d.user, d.cwd, ' '.join(d.command)) for d in app.get_all_commands()]
    print(tabulate(data, headers=header))


@main.command(help='Show details of a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def show(app: App, name: str):
    data = app.get_command(name)
    click.echo('name:    {}'.format(name))
    click.echo('user:    {}'.format(data.user))
    click.echo('cwd:     {}'.format(data.cwd))
    click.echo('command: {}'.format(' '.join(data.command)))


@main.command(help='Delete a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def delete(app: App, name: str):
    app.delete_command(name)


@main.group(help='APT Package management')
def apt():
    pass


@apt.command('require', help='Mark a package as required')
@click.argument('name', type=click.STRING)
@click.pass_obj
def apt_require(app: App, name: str):
    app.require_package(name)


@apt.command('unrequire', help='Unmark a package as required')
@click.argument('name', type=click.STRING)
@click.pass_obj
def apt_unrequire(app: App, name: str):
    app.unrequire_package(name)


@apt.command('list', help='List all required packages')
@click.pass_obj
def apt_list(app: App):
    for name in app.get_required_packages():
        click.echo(name)


@apt.command('apply', help='Install all required packages')
@click.pass_obj
def apt_apply(app: App):
    names = app.get_required_packages()
    command = ['apt', 'install', *names]
    run_as_user(command, 'root')


if __name__ == '__main__':
    main()