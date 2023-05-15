from connect_redis import *
import uuid
from  recommendation import *
from  picture import *
from datetime import date as dt

def generateSessionId():
    session_id = str(uuid.uuid4())
    return session_id

def createSession(customer_id, picture_url, tags):
    redis_client = connectredis()
    session_id=generateSessionId()
    addPicture(customer_id, picture_url, tags)
    date=dt.today() 
    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'
    date=date.today()
    recommendation=getRecommendation(picture_url, tags)
    # Store session data in Redis hash
    redis_client.hset(session_key, 'session_id', session_id)
    redis_client.hset(session_key, 'customer_id', customer_id)
    redis_client.hset(session_key, 'recommendation', recommendation)
  # redis_client.hset(session_key, 'number_of_pictures', number_of_pictures)
    redis_client.hset(session_key, 'tags', tags)
    redis_client.hset(session_key, 'date', date.isoformat())
    return session_id

def updateSessionRecommendation(session_id, new_recommendation):
    redis_client = connectredis()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Update the recommendation attribute
    redis_client.hset(session_key, 'recommendation', new_recommendation)

def deleteCustomerSessions(customer_id):
    redis_client = connectredis()

    # Get all session IDs for the customer
    session_ids = redis_client.zrange(f'craft_style_sessions:{customer_id}', 0, -1)

    # Delete session data and remove session IDs from the Sorted Set
    pipeline = redis_client.pipeline()

    for session_id in session_ids:
        session_key = f'craft_style_session:{session_id}'
        pipeline.delete(session_key)

    pipeline.delete(f'craft_style_sessions:{customer_id}')
    pipeline.execute()
    
    
def getSession(session_id):
    redis_client = connectredis()
    session_key = f'craft_style_session:{session_id}'
    session_data = redis_client.hgetall(session_key)
    return session_data

