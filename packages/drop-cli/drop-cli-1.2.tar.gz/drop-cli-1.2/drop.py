import click
import json
import subprocess
from sys import exit
from os import listdir, remove
from os.path import isfile, join, isdir, exists
from typing import List


class Options:
    def __init__(self):
        self.verbose = False
        self.configs = None


pass_config = click.make_pass_decorator(Options, ensure=True)


def check_existence(paths: List[str]):
    for path in paths:
        if not exists(path):
            click.echo(f'{path} does not exist')
            exit(1)


def does_device_exist(device_name: str):
    return any([f for f in listdir('/dev/mapper') if f == device_name])


def validate_config(config):
    names = set()
    inputs = set()
    repo = config['repository']

    if not exists(repo):
        click.echo(f'{repo} does not exist')
        exit(1)

    for device in config['devices']:
        name = device['name']
        input_ = device['input']
        output = device['mount_point']

        if name in names:
            click.echo('Duplicate names are not allowed!')
            exit(1)

        if input_ in inputs:
            click.echo('Duplicate input paths are not allowed!')
            exit(1)

        if not exists(input_):
            click.echo(f'{input_} does not exist!')
            exit(1)

        if not exists(output):
            click.echo(f'{output} does not exist!')
            exit(1)

        names.add(name)
        inputs.add(input_)


def load_configs():
    '''
    This command looks for .dropconfig file
    in the directory if it does not find it
    it will throw an error else it will silently load it and other
    programs can use it in the background.
    '''
    files = [file for file in listdir('.')
             if isfile(file) and file == '.dropconfig']

    if len(files) == 0:
        click.echo(".dropconfig is not found in the current directory")
        exit(1)

    elif len(files) > 1:
        click.echo("you have more than one .dropconfig file")
        exit(1)

    with open(files[0]) as f:
        config = json.load(f)
        validate_config(config)
        return config


def get_configuration(config, name):
    for device in config['devices']:
        if device['name'] == name:
            return device
    click.echo(f'Device does not exist in .dropconfig''')
    exit(1)


def run_command(command: List[str]):
    result = subprocess.run(command, capture_output=True)
    if result.returncode:
        click.echo(f'{result.stderr}')
        exit(1)


@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(opts, verbose):
    opts.verbose = verbose
    opts.configs = load_configs()


@cli.command()
@pass_config
def generate_config(opts):
    if exists('.dropconfig'):
        click.echo(f'.dropconfig already exists')
        exit(1)
    config = '''{
    "repository":"./repository",
    "devices": [
        {
            "name": "storage_name",
            "input": "./data",
            "mount_point": "./mount"
        }
    ]
}
    '''
    with open('.dropconfig', 'w') as f:
        f.write(config)

    if opts.verbose:
        print('.dropconfig is created')


@cli.command()
@click.argument('name', required=True)
@pass_config
def mount(opts, name):
    configs = opts.configs
    config = get_configuration(configs, name)
    in_path, mount_point = config['input'], config['mount_point']
    repo = configs['repository']

    check_existence([in_path, repo])

    files = sorted([join(in_path, file) for file in listdir(in_path)])

    if any(map(isdir, files)):
        click.echo(f'{in_path} should not contain directories!')
        exit(1)

    repo_path = join(repo, name)

    if exists(repo_path):
        if opts.verbose:
            click.echo(f'Remove {repo_path}')

        remove(repo_path)

    with open(repo_path, 'ab') as f:
        for file in files:

            if opts.verbose:
                click.echo(f'join file: {file}')

            with open(file, 'rb') as fp:
                f.write(fp.read())

    if does_device_exist(str(name)):
        click.echo(f'/dev/mapper/{name} already exists.')
        exit(1)

    run_command(['sudo', 'cryptsetup', 'luksOpen', repo_path, str(name)])
    run_command(['sudo', 'mount', join(
        '/dev/mapper/', str(name)), str(mount_point)])


@cli.command()
@click.argument('name', required=True)
@pass_config
def umount(opts, name):
    configs = opts.configs
    config = get_configuration(configs, name)

    repo = configs['repository']
    input_ = config['input']
    mount = config['mount_point']

    check_existence([repo, input_, mount])

    run_command(['sudo', 'umount', mount])
    run_command(['sudo', 'cryptsetup', 'luksClose', f'/dev/mapper/{name}'])

    for file in listdir(input_):
        remove(join(input_, file))

    repo_path = join(repo, name)

    if opts.verbose:
        click.echo(f'Splitting a file {repo_path}')

    run_command(['split', '--bytes=100MB', repo_path, join(input_, name)])


if __name__ == "__main__":
    cli()
