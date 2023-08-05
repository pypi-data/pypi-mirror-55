import click
import json
import subprocess
from sys import exit
from os import listdir, remove
from os.path import isfile, join, isdir, exists
from typing import List

configs = None


class Options:
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Options, ensure=True)


def check_existence(paths: List[str]):
    for path in paths:
        if not exists(path):
            click.echo(f'{path} does not exist')
            exit(1)


def validate_config(config):
    names = set()
    inputs = set()
    repo = config['repository']

    if not exists(repo):
        raise ValueError(f'{repo} does not exist')

    for device in config['devices']:
        name = device['name']
        input_ = device['input']
        output = device['mount_point']

        if name in names:
            raise ValueError('Duplicate names are not allowed!')

        if input_ in inputs:
            raise ValueError('Duplicate input paths are not allowed!')

        if not exists(input_):
            raise ValueError(f'{input_} does not exist!')

        if not exists(output):
            raise ValueError(f'{output} does not exist!')

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
        raise ValueError(".dropconfig is not found in the current directory")
    elif len(files) > 1:
        raise ValueError("you have more than one .dropconfig file")

    with open(files[0]) as f:
        config = json.load(f)
        validate_config(config)
        return config


def get_configuration(config, name):
    for device in config['devices']:
        if device['name'] == name:
            return device
    raise ValueError('Device does not exist in .dropconfig')


def run_command(command: List[str]):
    result = subprocess.run(command, capture_output=True)
    if result.returncode:
        raise ValueError(f'{result.stderr}')


@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(opts, verbose):
    opts.verbose = verbose
    pass


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

    run_command(['cryptsetup', 'luksOpen', repo_path, str(name)])
    run_command(['mount', join('/dev/mapper/', str(name)), str(mount_point)])


@cli.command()
@click.argument('name', required=True)
@pass_config
def umount(opts, name):
    config = get_configuration(configs, name)

    repo = configs['repository']
    input_ = config['input']
    mount = config['mount_point']

    check_existence([repo, input_, mount])

    run_command(['umount', mount])
    run_command(['sudo', 'cryptsetup', 'luksClose', f'/dev/mapper/{name}'])

    for file in listdir(input_):
        remove(join(input_, file))

    repo_path = join(repo, name)

    if opts.verbose:
        click.echo(f'Splitting a file {repo_path}')

    run_command(['split', '--bytes=100MB', repo_path, join(input_, name)])


if __name__ == "__main__":
    configs = load_configs()
    cli()
