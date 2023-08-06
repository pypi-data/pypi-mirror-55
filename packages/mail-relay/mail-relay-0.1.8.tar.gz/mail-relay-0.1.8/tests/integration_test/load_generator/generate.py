import os
import random
import time

from pvHelpers.crypto_client import CryptoClient
from pvHelpers.cs_client import BackendClient
from pvHelpers.utils import CaseInsensitiveDict, randUnicode

from .utils import add_member, get_members, send_email


backend_client = BackendClient()
backend_client.init(unicode(os.environ['CS_URL']))
crypto_client = CryptoClient(unicode(os.environ['CRYPTO_URL']))

# create or re-use  existing organization
admin_id = os.environ.get('ADMIN', u'{}@preveil.test'.format(randUnicode()))
org_id = None
existing_users = CaseInsensitiveDict(
    {u['user_id']: u for u in crypto_client.list_local_users()['users']})
if admin_id not in existing_users:
    admin = crypto_client.create_test_account(admin_id, u'journal')
    org_id = crypto_client.create_organization(admin_id)['org_id']
    existing_users = CaseInsensitiveDict(
        {u['user_id']: u for u in crypto_client.update_and_list_local_users(admin_id)['users']})
    admin = existing_users[admin_id]
else:
    admin = existing_users[admin_id]
    org_id = admin['org_info']['org_id']

print admin


class Timings:
    NEW_EMAIL = (10, 0)
    NEW_MEMBER = (100, 0)

    # EXPORT_GROUP_CHANGE = 100
    # MEMBER_REKEY = 100


while True:
    current_time = time.time()

    # take a random member

    if current_time - Timings.NEW_MEMBER[1] > Timings.NEW_MEMBER[0]:
        add_member(admin, crypto_client, backend_client)

        Timings.NEW_MEMBER = (Timings.NEW_MEMBER[0], time.time())

    if current_time - Timings.NEW_EMAIL[1] > Timings.NEW_EMAIL[0]:
        members = get_members(org_id, crypto_client).values()
        sender = random.choice(members)
        recipients = random.sample(members, random.randint(1, len(members)))

        send_email(sender, recipients, crypto_client)

        Timings.NEW_EMAIL = (Timings.NEW_EMAIL[0], time.time())
