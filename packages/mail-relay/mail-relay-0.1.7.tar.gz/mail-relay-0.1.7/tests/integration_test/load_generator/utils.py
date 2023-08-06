import os
import StringIO

from pvHelpers.utils import CaseInsensitiveDict, randUnicode
from werkzeug.datastructures import FileStorage


def get_members(org_id, crypto_client):
    existing_users = CaseInsensitiveDict(
        {u['user_id']: u for u in crypto_client.list_local_users()['users']})
    return CaseInsensitiveDict({
        uid: u for uid, u in existing_users.iteritems() if
             u['org_info'] and u['org_info']['org_id'] == org_id
    })


def send_email(sender, recipients, crypto_client):
    subject = randUnicode()
    text = randUnicode()
    tos = recipients
    ccs = []
    bccs = []
    html = u'<div>{}</div>'.format(randUnicode())
    atts = [{
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'image/jpeg'
    }, {
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'application/zip'
    }, {
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'audio/jpeg'
    }, {
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'application/pdf'
    }]

    attachments = [
        FileStorage(
            stream=StringIO.StringIO(a['content']),
            filename=a['name'], content_type=a['type']) for a in atts]

    crypto_client.send_email(
        4, {'user_id': sender['user_id'], 'display_name': sender['display_name']},
        [{'user_id': t['user_id'], 'display_name': t['display_name']} for t in tos],
        [{'user_id': c['user_id'], 'display_name': c['display_name']} for c in ccs],
        [{'user_id': b['user_id'], 'display_name': b['display_name']} for b in bccs],
        subject, text, html, attachments, None, [], [], [])


def add_member(admin, crypto_client, cs_client, member_id=None, department=None, role='standard'):
    member_id = member_id or u'{}@preveil.test'.format(randUnicode())
    department = department or randUnicode()

    crypto_client.invite_org_member(
        admin['user_id'], admin['org_info']['org_id'], member_id, randUnicode(), department, role)
    d = cs_client.get_user_secret(member_id, u'account_setup')
    member = crypto_client.claim_account(member_id, d['secret'], d['metadata']['key_version'])
    if role == 'admin':
        crypto_client.change_member_role(admin['user_id'], admin['org_info']['org_id'], member_id, role)
        member['org_info']['role'] = u'admin'

    return member
