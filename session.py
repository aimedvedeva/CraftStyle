from connect_redis import connect
import uuid

def generateSessionId():
    session_id = str(uuid.uuid4())
    return session_id

def createSession(customer_id, session_id, recommendation, number_of_pictures, tags, date):
    redis_client = connect()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Store session data in Redis hash
    redis_client.hset(session_key, 'session_id', session_id)
    redis_client.hset(session_key, 'customer_id', customer_id)
    redis_client.hset(session_key, 'recommendation', recommendation)
    redis_client.hset(session_key, 'number_of_pictures', number_of_pictures)
    redis_client.hset(session_key, 'tags', tags)
    redis_client.hset(session_key, 'date', date)

def updateSessionRecommendation(session_id, new_recommendation):
    redis_client = connect()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Update the recommendation attribute
    redis_client.hset(session_key, 'recommendation', new_recommendation)

def deleteSession(session_id):
    redis_client = connect()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Delete the session data
    redis_client.delete(session_key)

