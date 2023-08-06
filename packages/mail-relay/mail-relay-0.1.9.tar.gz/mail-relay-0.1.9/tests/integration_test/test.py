import os
import subprocess
import shutil

import click

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
        os.path.join(CONFIGS_DIR, 'volume_export.yml'),
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
    env = os.environ.copy()
    if (clear):
        for i in get_test_ids():
            env.update(
                TEST_DATA_DIR=test_dir(i),
                COMPOSE_PROJECT_NAME=str(i))
            subprocess.check_call(
                ['docker-compose', 'down', '-v'], cwd=TEST_RUNNER_ROOT, env=env)

            shutil.rmtree(test_dir(i))

        gctx.exit(0)

    if (list_tests):
        test_ids = get_test_ids()
        click.echo(', '.join([str(i) for i in sorted(test_ids)]))
        gctx.exit(0)

    test_id = new_test_context() if test_id is None else test_id
    if not os.path.isdir(test_dir(test_id)):
        click.echo('Invalid test {}'.format(test_id))
        gctx.exit(1)

    env.update(
        TEST_DATA_DIR=test_dir(test_id),
        COMPOSE_PROJECT_NAME=str(test_id))

    subprocess.check_call(
        ['docker-compose', 'down'], cwd=TEST_RUNNER_ROOT,
        env=env)

    subprocess.check_call(
        ['docker-compose', 'up', '-d'], cwd=TEST_RUNNER_ROOT,
        env=env)



cli()
