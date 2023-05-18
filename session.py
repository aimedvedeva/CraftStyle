from datetime import datetime
from connect_postgre import connect_postgre
from connect_redis import connect_redis
import uuid
from recommendation import get_recommendation
from craftStyle import add_picture, get_current_customer_subscription_plan


def _generate_session_id():
    session_id = str(uuid.uuid4())
    return session_id


def create_session(customer_id, picture_url, tags):
    # connections
    redis_client = connect_redis()

    # Add row to table Picture in postgreSQL
    add_picture(customer_id, picture_url, tags)

    # define variables
    date = datetime.today()
    plan = get_current_customer_subscription_plan(customer_id)
    sessions_number = get_customer_sessions_number(customer_id)

    if plan == 'Basic' and sessions_number <= 5 or plan == 'Premium':
        # generate a Session Id
        session_id = _generate_session_id()

        # Create a hash key for the session
        session_key = f'craft_style_session:{session_id}'
        recommendation = get_recommendation(picture_url, tags)

        # Store session data in Redis hash
        redis_client.hset(session_key, 'session_id', session_id)
        redis_client.hset(session_key, 'customer_id', customer_id)
        redis_client.hset(session_key, 'recommendation', recommendation)
        redis_client.hset(session_key, 'tags', tags)
        redis_client.hset(session_key, 'date', date.isoformat())

        # add 1 to number of session
        update_customer_sessions_number(customer_id)

        return session_id
    elif plan != 'Basic' and plan != 'Premium':
        print('You need to purchase a subscription plan')

    else:
        print('You reached maximum allowed sessions for basic plan')


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


def delete_customer_sessions(customer_id):
    redis_client = connect_redis()

    # Get all session IDs for the customer
    session_ids = redis_client.zrange(f'craft_style_sessions:{customer_id}', 0, -1)

    # Delete session data and remove session IDs from the Sorted Set
    pipeline = redis_client.pipeline()
    for session_id in session_ids:
        delete_session(session_id)
    pipeline.delete(f'craft_style_sessions:{customer_id}')
    pipeline.execute()


def get_session(session_id):
    redis_client = connect_redis()
    session_key = f'craft_style_session:{session_id}'
    session_data = redis_client.hgetall(session_key)
    return session_data


def get_customer_sessions_number(customer_id):
    cur = connect_postgre()
    query = "SELECT sessionsnumber FROM CraftStyle.customer WHERE customerid = %s;"
    cur.execute(query, (customer_id,))
    sessions_number = cur.fetchone()[0]
    return sessions_number


def update_customer_sessions_number(customer_id):
    cur = connect_postgre()
    sessions_number = get_customer_sessions_number(customer_id) + 1
    q = "UPDATE CraftStyle.customer SET sessionsnumber = %s WHERE customerid = %s;"
    cur.execute(q, (sessions_number, customer_id))
