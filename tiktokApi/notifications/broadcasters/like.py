from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_like_notification(post_id, liker_id, liked=True):
    channel_layer = get_channel_layer()
    action = "liked" if liked else "unliked"

    async_to_sync(channel_layer.group_send)(
        f"post_{post_id}",
        {
            "type": "send_like",
            "data": {"post_id": post_id, "liker_id": liker_id, "action": action},
        },
    )
