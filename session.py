from connect_redis import connectredis
import uuid
from  recommendation import *
from  picture import *
from datetime import date as dt
from craftStyle import * #getCurrentCustomerSubscriptionPlan
#from customer import *
def generateSessionId():
    session_id = str(uuid.uuid4())
    return session_id

def createSession(customer_id, picture_url, tags):
    #connections
    redis_client = connectredis()
    
     
    #Add row to table Picture in postSQL
    addPicture(customer_id, picture_url, tags)
    
    
    #define variables 
    date=dt.today() 
    plan= getCurrentCustomerSubscriptionPlan(customer_id)
    Num_of_session=getCustomerSessionsNumber(customer_id)
    
    if plan=='Basic' and Num_of_session <= 5 or plan=='Premium' :
        #generate a Session Id
        session_id=generateSessionId()
    
        # Create a hash key for the session
        session_key = f'craft_style_session:{session_id}'
        recommendation=getRecommendation(picture_url, tags)
        
        # Store session data in Redis hash
        redis_client.hset(session_key, 'session_id', session_id)
        redis_client.hset(session_key, 'customer_id', customer_id)
        redis_client.hset(session_key, 'recommendation', recommendation)
        redis_client.hset(session_key, 'tags', tags)
        redis_client.hset(session_key, 'date', date.isoformat())
        
        #add 1 to number of session
        updateSessionsNumber(customer_id)
        
        return session_id
    elif plan != 'Basic' and plan !='Premium':
        print('You need to purchase a subscription plan')
        
    else:
        print('You reached maximum allowed sessions for basic plan')
    
        

def updateSessionRecommendation(session_id, new_recommendation):
    redis_client = connectredis()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Update the recommendation attribute
    redis_client.hset(session_key, 'recommendation', new_recommendation)

def deleteSession(session_id):
    redis_client = connectredis()

    # Create a hash key for the session
    session_key = f'craft_style_session:{session_id}'

    # Delete the session data
    redis_client.delete(session_key)


def deleteCustomerSessions(customer_id):
    redis_client = connectredis()

    # Get all session IDs for the customer
    session_ids = redis_client.zrange(f'craft_style_sessions:{customer_id}', 0, -1)

    # Delete session data and remove session IDs from the Sorted Set
    pipeline = redis_client.pipeline()
    for session_id in session_ids:
        deleteSession(session_id)
    pipeline.delete(f'craft_style_sessions:{customer_id}')
    pipeline.execute()
    
def getSession(session_id):
    redis_client = connectredis()
    session_key = f'craft_style_session:{session_id}'
    session_data = redis_client.hgetall(session_key)
    return session_data

def getCustomerSessionsNumber(customer_id):
    cur=connectsgl()
    query = "SELECT sessionsnumber FROM CraftStyle.customer WHERE customerid = %s;"
    cur.execute(query, (customer_id,))
    sessions_number = cur.fetchone()[0]
    return sessions_number 

def updateSessionsNumber(customer_id):
    cur=connectsgl()
    n=getCustomerSessionsNumber(customer_id)+1
    q = "UPDATE CraftStyle.customer SET sessionsnumber = %s WHERE customerid = %s;"
    cur.execute(q, (n, customer_id))

