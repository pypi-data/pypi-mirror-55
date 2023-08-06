import calendar
import time

from flanker import mime
from pvHelpers.crypto.utils import CryptoException, HexEncode, Sha256Sum
from pvHelpers.logger import g_log
from pvHelpers.mail.email import EmailException, EmailV1, PROTOCOL_VERSION
from pvHelpers.utils import b64dec, EncodingException, jloads, MergeDicts, utf8Decode

ACCEPTED_PROTOCOL_VERSIONS = [1, 4]


# encryption_key needed for later
def decrypt_server_message(encryption_key, decrypt_key, message):
    p_meta = jloads(utf8Decode(decrypt_key.decrypt(b64dec(message['private_metadata']))))
    return MergeDicts(message, {
        'body': MergeDicts(
                    message['body'],
                    {'snippet': utf8Decode(decrypt_key.decrypt(b64dec(message['body']['snippet'])))}),
        'private_metadata': p_meta,
        'timestamp': calendar.timegm(time.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S')),
        'attachments': map(lambda att: MergeDicts(
            att, {'name': utf8Decode(decrypt_key.decrypt(b64dec(att['name'])))}), message['attachments'])
    })


def reconstruct_content_blocks(block_ids, blocks, symm_key):
    part = ''
    for block_id in block_ids:
        encrypted_block = blocks.get(block_id)
        if encrypted_block is None:
            return None, KeyError('missing block with block_id {}'.format(block_id))

        encrypted_block = encrypted_block.get('data')
        if encrypted_block is None:
            return None, KeyError('data missing')

        try:
            p = symm_key.decrypt(b64dec(encrypted_block))
        except (CryptoException, EncodingException) as e:
            return None, e
        part += p

    return part, None


def get_wrapped_key(server_message):
    for block in server_message['body']['blocks']:
        return block['key_version'], block['wrapped_key']
    for att in server_message['attachments']:
        for block in att['blocks']:
            return block['key_version'], block['wrapped_key']
    raise KeyError('No wrapped key provided in server message {}'.format(server_message))


def get_email_mime(email, blocks, decrypt_key):
    content_ref_ids = [
        email.body.reference_id] + map(lambda att: att.content.reference_id, email.attachments)

    contents = {}
    for reference_id in content_ref_ids:
        raw_content, err = reconstruct_content_blocks(
            reference_id.split(','), blocks, decrypt_key)
        if err is not None:
            g_log.exception(err)
            continue
        contents[reference_id] = raw_content

    if not all(map(lambda ref_id: ref_id in contents, content_ref_ids)):
        raise EmailException('Failed to reconstuct email contents, missing blocks')

    body_content = contents[email.body.reference_id]
    if email.protocol_version is PROTOCOL_VERSION.V1:
        body_mime = mime.create.from_string(contents[email.body.reference_id])
        for att in email.attachments:
            # This replacement due protocol_version 1 body serialization which uses
            # block_ids of attachments for referencing dummy nodes, while locally we use
            # attachment hash for referencing so that attachment separation can be independent
            # of any encryption or server storage upload
            att_hash = HexEncode(Sha256Sum(contents[att.content.reference_id]))
            status, body_mime = EmailV1.replaceDummyReferences(
                body_mime, {u','.join(att.content.block_ids): att_hash})
            if not status:
                raise EmailException('Failed to replace dummy references')

        body_content = body_mime.to_string()

    email.loadBody(body_content)
    for att in email.attachments:
        if att.content.reference_id in contents:
            att.loadContent(contents[att.content.reference_id])

    return email.toMime().to_string()


def wrap_for_export(mime):
    # add header
    return mime
