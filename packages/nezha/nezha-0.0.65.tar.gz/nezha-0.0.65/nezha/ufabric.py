"""
example:
from fabric import task

@task
def upload(ctx):
    pass

fabric -v 2.5
Python 3.7

env='root@47.103.37.xxx'

complete example:
# file name must be: fabfile.py
import os

from fabric import task
from nezha.ufabric import Connection, local
from nezha.ufabric import rm, tar, untar

THIS_DIR = os.path.dirname(os.path.abspath(__name__))
deploy_env = {
    'sit': ('root@47.103.37.xx',),
    'pre': ('root@47.103.37.xx',),
    'prod': ('root@47.101.45.xx', 'root@106.15.203.xxx')
}


@task
def deploy(ctx, env):
    deploy_tar_name = 'deploy.tar'
    deploy_tar_full_path = os.path.join(THIS_DIR, deploy_tar_name)
    if os.path.exists(deploy_tar_full_path):
        rm(deploy_tar_full_path)
    tar(deploy_tar_name, os.path.join(THIS_DIR, 'deploy'))
    for e in deploy_env.get(env):
        remote_machine = Connection(e)
        destination_path = '/usr/local/supplier_platform'
        remote_machine.run(f'mkdir -p {destination_path}')
        local(f'scp -i /Users/yutou/.ssh/id_rsa {deploy_tar_full_path} {e}:{destination_path}')
        untar(os.path.join(destination_path, deploy_tar_name), destination_path, env=e)
        remote_machine.run(f'/bin/cp -rf {destination_path}/deploy/supplier_platform.conf /etc/nginx/conf.d')
        remote_machine.run(f'nginx -s reload')

common command:
    + detect current tasks
    ./venv/bin/fab -l

    + execute task
    ./venv/bin/fab task_name task_arguments
"""
import os
import time
from functools import reduce
from itertools import chain
from typing import Callable, Optional, Tuple

from fabric import Connection as _cn
from invoke import run as _local
from nezha.usetup import update_version


def print_command(func: Callable, is_method: bool = False):
    println = lambda x: print(f'execute => {x[0]}')
    if is_method:
        def wrap(self, *args, **kwargs):
            println(args)
            return func(self, *args, **kwargs)

        return wrap
    else:
        def wrap(*args, **kwargs):
            println(args)
            return func(*args, **kwargs)

        return wrap


local = print_command(_local)
_cn.sudo = print_command(_cn.sudo, is_method=True)
_cn.run = print_command(_cn.run, is_method=True)
Connection = _cn


class Fabric:

    def task(self, *args, **kwargs):
        if len(args) > 0 and callable(args[0]):
            self._task = args[0]
            return self
        else:
            raise TypeError(f'@task() takes exactly 1 argument ({args} given)')


def _run(command, env='') -> None:
    """
    use run replace fabric local or remote_machine.run()
    :param command:
    :param env:
    :return:
    """
    env and Connection(env).run(command) or local(command)

# expose run method.
run = _run


def _join_command_option(command: str, option_name: str, option_val: str) -> str:
    optional_str = f'{option_name}={option_val}' if option_name.startswith('--') else f'{option_name} {option_val}'
    return ' '.join((command, optional_str))


def _join_multi_options(command: str, options: Optional[Tuple[Tuple[str, str], ...]] = None):
    if options:
        reduced = reduce(lambda x, y: _join_command_option('', option_name=x, option_val=y), chain(*options))
        command = ' '.join((command, reduced))
    return command


def rm(tar: str, env: str = '') -> None:
    command = f'rm -f {tar}'
    return _run(command, env)


def tar(tar: str, package: str, env: str = '', exclude: Optional[Tuple] = None) -> None:
    """

    :param tar:
    :param package:
    :param env:
    :param options: tuple(k,v). type dict is not allowed repeated keys.
    :return:
    """
    exclude_option = ' '.join(map(lambda x: f'--exclude={x}', exclude)) if exclude else ''
    head, tail = os.path.split(package)
    command = f'cd {head} && tar {exclude_option} -cvf {tar} {tail}'
    return _run(command, env)


def untar(tar_file: str, untar_path: str, env: str = '') -> None:
    command = f'tar -xvf {tar_file} -C {untar_path}'
    return _run(command, env)


def scp(env: str, local_file: str, destination_path: str) -> None:
    command = f'scp {local_file} {env}:{destination_path}'
    return _run(command, env)


def fab_pypi_project(ctx, interpreter: str, project_name: str, version: str, project_dir: str):
    retry = 5
    python = interpreter
    update_version(f'{project_dir}/setup.py', version)
    local(f'cd {project_dir} && bash {project_dir}/pypi.sh')
    for i in range(retry):
        current_version = local(f'{python} -m pip freeze|grep {project_name}').stdout.strip()
        if current_version != f'{project_name}=={version}':
            print(f'now {current_version} is not latest')
            local(f'{python} -m pip install {project_name}=={version}', warn=True)
        else:
            break
        time.sleep(2)


if __name__ == '__main__':
    exclude = ['pyc', '.git']
    print(' '.join(map(lambda x: f'--exclude={x}', exclude)))
