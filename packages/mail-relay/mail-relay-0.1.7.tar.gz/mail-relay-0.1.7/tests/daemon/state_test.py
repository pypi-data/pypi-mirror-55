from mail_relay.daemon.state import State
from mail_relay.store.handlers import update_config, write_exporter, write_user, write_user_key
import pytest

from ..utils import create_test_account


@pytest.mark.integration
def key_rotatation_test(cs_client, test_config, store):
    # needs exporter
    with pytest.raises(KeyError):
        State(store)

    user = create_test_account(cs_client)

    write_user_key(user.user_id, user.account_version, user.user_key, store)
    write_user(user, store)

    # needs exporter
    with pytest.raises(KeyError):
        State(store)

    write_exporter(user.user_id, user.account_version, store)

    # needs config
    with pytest.raises(AttributeError):
        State(store)

    update_config(test_config, store)
    state = State(store)
    assert len(state.local_users) == 2
    assert state.local_users[(user.account_version, user.user_id)].device.key == user.device.key

    state.rotate_device_key(user.user_id, user.account_version)

    assert state.local_users[(user.account_version, user.user_id)].device.key.key_version == \
        user.device.key.key_version + 1
    assert state.local_users[(user.account_version, user.user_id)].user_key == user.user_key

    # TODO: add test for intermittend rotation and handling of `401`
