import os
import shutil
import subprocess
import time
import random

import click
from pvHelpers.utils import jloads, MergeDicts, utf8Decode

from ..utils import crypto_send_user_key, get_rand_port

TEST_RUNNER_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(TEST_RUNNER_ROOT, '.test_data')
TEST_PREFIX = 'test_'
CONFIGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')


def test_dir(test_id):
    return os.path.join(TEST_DIR, '{}{}'.format(TEST_PREFIX, test_id))


def get_test_ids():
    return [int(d.split('_')[1]) for d in os.listdir(TEST_DIR) if d.startswith(TEST_PREFIX)]


def new_test_context():
    existing_test_ids = get_test_ids()
    next_id = max([-1] + existing_test_ids) + 1
    next_dir = test_dir(next_id)
    os.mkdir(next_dir)
    # create volumes
    for v in ['crypto', 'export', 'relay']:
        os.mkdir(os.path.join(next_dir, v))

    # set config file for relay tool
    shutil.copyfile(
        os.path.join(CONFIGS_DIR, 'volume.test.yml'),
        os.path.join(next_dir, 'relay', 'config.yml'))

    return next_id


@click.command('test')
@click.option('-l', '--list-tests', 'list_tests', flag_value=True, default=False)
@click.option('-c', '--clear', 'clear', flag_value=True, default=False)
@click.option(
    '-i', '--test-id', 'test_id',
    type=click.INT, default=None,
    help='Continue specified test number.')
@click.pass_context
def cli(gctx, test_id, list_tests, clear):
    '''handle integration test runner state'''
    p_env = os.environ.copy()
    if (clear):
        for i in get_test_ids():
            subprocess.check_call(
                ['docker-compose', 'down', '-v'], cwd=TEST_RUNNER_ROOT,
                env=MergeDicts(p_env, {'COMPOSE_PROJECT_NAME': str(i), 'CRYPTO_PORT': str(0)}))

            shutil.rmtree(test_dir(i))

        gctx.exit(0)

    if (list_tests):
        test_ids = get_test_ids()
        click.echo(', '.join([str(i) for i in sorted(test_ids)]))
        gctx.exit(0)

    if test_id is None:
        # create new test context
        click.echo('creating new test context!')
        test_id = new_test_context()
        click.echo('test context created!')

        click.echo('provisioning collection server!')
        click.echo('provisioning crypto server!')
        click.echo('provisioning load generator!')
        crypto_port = get_rand_port()
        sp_env = MergeDicts(p_env, {
            'COMPOSE_PROJECT_NAME': str(test_id),
            'CRYPTO_PORT': str(crypto_port)
        })
        # provision collection server, crypto_server
        subprocess.check_call(
            ['docker-compose', 'up', '-d', '--build', '--force-recreate'],
            cwd=TEST_RUNNER_ROOT, env=sp_env)
        # idle some time for services to become reachable
        time.sleep(10)
        click.echo('crypto server instance ready!')
        click.echo('collection server instance ready!')

        # create new user/org
        click.echo('creating test organization!')
        p = subprocess.Popen(
            ['docker-compose', 'run', '--rm', 'load_generator', '-c'],
            stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)

        assert p.wait() == 0
        organization_info = jloads(utf8Decode(p.stdout.read()))
        click.echo('created test organization!')
        click.echo(organization_info)

        # configure relay tool
        click.echo('configuring relay tool!')
        # migrate db
        subprocess.check_call(
            ['docker-compose', 'run', '--rm', 'relay', 'migrate'],
            cwd=TEST_RUNNER_ROOT, env=sp_env)
        click.echo('relay database migrated!')
        # point to config file
        subprocess.check_call(
            ['docker-compose', 'run', '--rm', 'relay', 'config', '-c', './data/config.yml'],
            cwd=TEST_RUNNER_ROOT, env=sp_env)
        click.echo('relay configuration saved!')

        # configure exporter
        p = subprocess.Popen(
            ['docker-compose', 'run', '--rm', 'relay', 'config', 'exporter', organization_info['admin_id']],
            stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
        send_pin_handle = crypto_send_user_key('127.0.0.1', crypto_port, organization_info['admin_id'])
        time.sleep(3)
        p.stdout.readline() # skip just info line
        pin = p.stdout.readline().split('pin: ')[1].strip()
        send_pin_handle(pin)
        assert p.wait() == 0
        click.echo('relay exporter {} configured!'.format(organization_info['admin_id']))

        # configure approvers
        for a in random.sample(organization_info['approvers'], organization_info['optionals_required']):
            p = subprocess.Popen(
                ['docker-compose', 'run', '--rm', 'relay', 'config', 'approver', a['user_id']],
                stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
            send_pin_handle = crypto_send_user_key('127.0.0.1', crypto_port, a['user_id'])
            time.sleep(3)
            p.stdout.readline() # skip just info line
            pin = p.stdout.readline().split('pin: ')[1].strip()
            send_pin_handle(pin)
            assert p.wait() == 0
            click.echo('relay approver {} configured!'.format(a['user_id']))

    else:
        if not os.path.isdir(test_dir(test_id)):
            click.echo('Invalid test {}'.format(test_id))
            gctx.exit(1)
        # continue test

        p_env.update(COMPOSE_PROJECT_NAME=str(test_id))

        # provision collection server, crypto_server
        subprocess.check_call(
            ['docker-compose', 'up', '-d'], cwd=TEST_RUNNER_ROOT, env=p_env)
        time.sleep(4)
        # create new user/org
        p = subprocess.Popen(
            ['docker-compose', 'run', '--rm', 'load_generator', '-c'],
            stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=p_env)

        exit_code = p.wait()
        out = p.stdout.read()
        print out
        print exit_code
        # subprocess.check_call(
        #     ['docker-compose', 'up', '-d'], cwd=TEST_RUNNER_ROOT, env=p_env)



cli()
