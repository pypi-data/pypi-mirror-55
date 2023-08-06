import os

from mail_relay.config import Config, CSConfig, IMAPConfig, SMTPConfig, VolumeConfig
from mail_relay.store.migrate import migrate
from pvHelpers.cs_client import BackendClient
import pytest


@pytest.fixture(scope='session')
def test_config():
    IMAPConfig(
        os.environ['IMAP_HOST'], int(os.environ['IMAP_PORT']), None, None, False)
    VolumeConfig(os.environ['EXPORT_VOLUME'])
    return Config(
        CSConfig(os.environ['CS_HOST'], int(os.environ['CS_PORT']), False),
        smtp=SMTPConfig(os.environ['SMTP_HOST'], int(os.environ['SMTP_PORT']), None, None, False, None))


@pytest.fixture(scope='session')
def cs_client(test_config):
    c = BackendClient()
    c.init(test_config.cs.http)
    return c


@pytest.fixture(scope='module')
def store(tmpdir_factory):
    s = tmpdir_factory.mktemp('store')
    store_path = os.path.abspath(os.path.join(str(s), 'test.sqlite'))
    migrate(store_path)
    return store_path
