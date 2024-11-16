from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.uuid import UUID
from .config import config

cipher_key = config.get("PUBNUB_CIPHER_KEY")
pn_config.publish_key = config.get("PUBNUB_PUBLISH_KEY")
pn_config.subscribe_key = config.get("PUBNUB_SUBSCRIBE_KEY")
pn_config.uuid = config.get("GOOGLE_ADMIN_ID")
pn_config.secret_key = config.get("APP_SECRET_KEY")
pn_config.cipher_key = cipher_key
pubnub = PubNub(pn_config)


def grant_read_write_access(user_id):
    envelope = pubnub.grant_token() \
    .channels([Channel.id(channel).read().write() for channel in ("sd3b-iot-channel")]) \
    .authorized_uuid(user_id) \
    .ttl(60) \
    .sync()
    return envelope.result.token