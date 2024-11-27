from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.uuid import UUID
from pubnub.models.consumer.v3.group import Group
from .config import config

pn_config = PNConfiguration()

cipher_key = config.get("PUBNUB_CIPHER_KEY")
pn_config.publish_key = config.get("PUBNUB_PUBLISH_KEY")
pn_config.subscribe_key = config.get("PUBNUB_SUBSCRIBE_KEY")
pn_config.uuid = config.get("GOOGLE_ADMIN_ID")
pn_config.secret_key = config.get("PUBNUB_SECRET_KEY")
#pn_config.cipher_key = cipher_key
pubnub = PubNub(pn_config)


def grant_read_write_access(user_id):
    print(f"GRANTING READ AND WRITE ACCESS {user_id}")
    envelope = pubnub.grant_token() \
    .channels([Channel.id("sd3b-iot-channel").read().write()]) \
    .authorized_uuid(user_id) \
    .ttl(60) \
    .sync()
    return envelope.result.token


def grant_read_access(user_id):
    print(f"GRANTING READ ACCESS {user_id}")
    envelope = pubnub.grant_token() \
    .channels([Channel.id("sd3b-iot-channel").read()]) \
    .authorized_uuid(user_id) \
    .ttl(60) \
    .sync()
    return envelope.result.token


def grant_write_access(user_id):
    print(f"GRANTING WRITE ACCESS {user_id}")
    envelope = pubnub.grant_token() \
    .channels([Channel.id("sd3b-iot-channel").write()]) \
    .authorized_uuid(user_id) \
    .ttl(60) \
    .sync()
    return envelope.result.token


def revoke_access(token):
    envelope = pubnub.revoke_token(token)


def parse_token(token):
    token_details = pubnub.parse_token(token)
    print("Parsing the token")
    print(token_details)
    read_access = token_details["resources"]["channels"]["sd3b-iot-channel"]["read"]
    write_access = token_details["resources"]["channels"]["sd3b-iot-channel"]["write"]
    uuid = token_details["authorized_uuid"]
    return token_details["timestamp"], token_details["ttl"], uuid, read_access, write_access



