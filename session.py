from connect_redis import connect_redis
import uuid


def _generate_session_id():
    session_id = str(uuid.uuid4())
    return session_id


def update_session_recommendation(session_id, new_recommendation):
    redis_client = connect_redis()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Update the recommendation attribute
    redis_client.hset(session_key, 'recommendation', new_recommendation)


def delete_session(session_id):
    redis_client = connect_redis()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Delete the session data
    redis_client.delete(session_key)


def get_session(session_id):
    redis_client = connect_redis()
    session_key = f'craft_style_session:{session_id}'
    session_data = redis_client.hgetall(session_key)
    return session_data


def create_session(customer_id, picture_urls, tags, date):
    redis_client = connect_redis()

    # generate session_id
    session_id = _generate_session_id()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Store session data in Redis hash
    redis_client.hset(session_key, 'session_id', session_id)
    redis_client.hset(session_key, 'customer_id', customer_id)
    redis_client.hset(session_key, 'recommendation', '')
    redis_client.hset(session_key, 'number_of_pictures', len(picture_urls))
    for idx, picture_url in enumerate(picture_urls):
        redis_client.hset(session_key, 'number_of_pictures_' + str(idx), picture_url)
    redis_client.hset(session_key, 'tags', tags)
    redis_client.hset(session_key, 'date', str(date))

    return session_id
