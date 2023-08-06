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

logger = logging.getLogger('commands')
click_log.basic_config(logger)


class App(object):
    def __init__(self, config_dir: Path):
        super(App, self).__init__()
        self.config_dir = config_dir
        if not config_dir.exists():
            self.config_dir.mkdir(mode=0o755, parents=True)
        self.dbfile = self.config_dir / 'db.json'
        if not self.dbfile.exists():
            self._write({'schemaVersion': 1, 'commands': {}})
        else:
            data = self._load()
            assert 'schemaVersion' in data
            assert data['schemaVersion'] == 1

    def _load(self) -> dict:
        with self.dbfile.open('r') as fp:
            return json.load(fp)

    def _write(self, data: dict):
        with self.dbfile.open('w') as fp:
            json.dump(data, fp, indent=2)

    def save(self, name: str, user: str, cwd: str, command: List[str]):
        data = self._load()
        assert name not in data['commands'], 'Command with this name already exists'
        data['commands'][name] = {
            'user': user,
            'cwd': cwd,
            'command': command,
        }
        self._write(data)

    def get(self, name: str) -> dict:
        data = self._load()
        assert name in data['commands'], 'Command with this name does not exist'
        return data['commands'][name]

    def get_all(self) -> dict:
        return self._load()['commands']

    def delete(self, name: str):
        data = self._load()
        assert name in data['commands'], 'Command with this name does not exist'
        del data['commands'][name]
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
    app.save(name=name, user=user, cwd=cwd, command=command)


@main.command(help='Run a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def run(app: App, name: str):
    data = app.get(name)
    current_user = pwd.getpwuid(os.getuid()).pw_name
    actual_command = []
    if data['user'] != current_user:
        actual_command.extend(['sudo', '-u', data['user']])
    actual_command.extend(data['command'])
    subprocess.check_call(actual_command, cwd=data['cwd'])


@main.command(help='List all commands')
@click.pass_obj
def list(app: App):
    header = ['name', 'user', 'cwd', 'command']
    data = [(name, d['user'], d['cwd'], ' '.join(d['command'])) for name, d in app.get_all().items()]
    print(tabulate(data, headers=header))


@main.command(help='Show details of a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def show(app: App, name: str):
    data = app.get(name)
    click.echo('name:    {}'.format(name))
    click.echo('user:    {}'.format(data['user']))
    click.echo('cwd:     {}'.format(data['cwd']))
    click.echo('command: {}'.format(' '.join(data['command'])))


@main.command(help='Delete a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def delete(app: App, name: str):
    app.delete(name)


if __name__ == '__main__':
    main()