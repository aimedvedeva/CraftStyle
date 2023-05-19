import uuid
from datetime import date

from connect_redis import connect_redis

def _generate_picture_id():
    session_id = str(uuid.uuid4())
    return session_id

def add_picture(customer_id, tags, picture_link):
    picture_id = _generate_picture_id()
    redis_client = connect_redis()

    # Create a hash key for the picture
    picture_key = f'craft_style_picture:{picture_id}'

    # Add the picture data as hash fields
    redis_client.hset(picture_key, 'upload_date', str(date.today()))
    redis_client.hset(picture_key, 'customer_id', customer_id)
    redis_client.hset(picture_key, 'tags', tags)
    redis_client.hset(picture_key, 'picture_link', picture_link)


def delete_picture(picture_id):
    redis_client = connect_redis()

    # Create a hash key for the picture
    picture_key = f'craft_style_picture:{picture_id}'

    # Delete the picture data
    redis_client.delete(picture_key)
