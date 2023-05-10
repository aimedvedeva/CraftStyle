import psycopg2, random, timeit
from timeit import default_timer as timer
from datetime import timedelta

def connect():
    conn = psycopg2.connect(database="postgres", user="student",\
                            password="HSDStoTestDb3711", host="database-1.czcdhgn8biyx.us-east-1.rds.amazonaws.com", port="5432")
    return conn.cursor()

def addCustomer(name):
    cur = connect()
    cur.execute("begin;")

    # create a new customer
    create_customer_query = """INSERT INTO CraftStyle.Customer(Name,sessionsNumber,subscriptionPlanID) VALUES (%s, %s, NULL);"""
    cur.execute(create_customer_query, (name, 0))

    cur.execute("commit")

def purchaseSubscription(customer_id, subscription_plan):
    cur = connect()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    # get id of a requested subscription plan
    cur.execute("select s.planid from subscriptionplan s where s.type = %s", (subscription_plan))
    subscription_plan_id = cur.fetchone()[0]

    if subscription_plan == 'Basic':
        create_customer_plan_query = """INSERT INTO CustomerPlan \ 
                                        (customerID,subscriptionPlanID,purchaseDate) VALUES (%s, %s, current_date);"""

        cur.execute(create_customer_plan_query, (customer_id, subscription_plan_id))
    elif subscription_plan == 'Advanced':
        try:
            # process_transaction()
            create_customer_query = """INSERT INTO CustomerPlan (customerID,subscriptionPlanID,purchaseDate) VALUES (%s, %s, current_date);"""
            cur.execute(create_customer_query, (customer_id, subscription_plan_id))
            cur.execute("commit")
        except:
            cur.execute("rollback")

def addCustomerSession(customer_id, pictures, picure_links, tags):
    cur = connect()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    try:
        # get id of a requested subscription plan
        cur.execute("""select s.allowedsessions \
                       from subscriptionplan s \ 
                       join customerplan c on s.planid = c.subscriptionplanid where customerID = %s""", (customer_id))
        allowed_sessions = cur.fetchone()[0]

        # get number of sessions that the customer has already had
        cur.execute("""select c.sessionsnumber from customer c where c.customerid = %s;""", (customer_id))
        done_sessions = cur.fetchone()[0]

        # check if the customer doesn't exceed the limit according to his subscription plan
        if done_sessions == allowed_sessions:
            raise ValueError("Unfortunately, all you free sessions have already used. You can upgrade you subscription plan.")

        update_sessions_number_query = """UPDATE customer SET sessionsnumber = sessionsnumber + 1 WHERE custometID = %s;"""

        cur.execute(update_sessions_number_query, (customer_id))

        # save data about the session
        cur.execute("""INSERT INTO CustomerSession(customerID, Recommendation, pucturesNumber, tags, sessionDate)
        VALUES(%s, NULL, %s, %s, current_date);""", (customer_id, len(pictures), tags))

        # save pictures
        for picture, link in zip(pictures, picure_links):
            cur.execute("""INSERT INTO Picture(customerID, pictureUrl, tags) VALUES(%s, %s, %s);""",\
                        (customer_id, link, tags))
        cur.execute("COMMIT")

    except Exception as e:
        # raise an exception if any error occur
        cur.execute("Rollback;")

def updateSessionRecommendation(session_id, recommendation):
    cur = connect()
    cur.execute("begin;")

    cur.execute("""UPDATE customerSession SET recommendation = %s WHERE custometSessionID = %s;""", \
                (recommendation, session_id))

    cur.execute("commit")

def deleteCustomer(customer_id):
    # since customer_id is a foreign key for CustomerSession, Picture and CustometPlan
    # firstly, we have to delete corresponding rows there
    # and finally from Customer table

    cur = connect()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    try:
        # delete all customers' pictures
        delete_customer_pictures_query = """delete from Picture WHERE custometID = %s;"""
        cur.execute(delete_customer_pictures_query, (customer_id))
        cur.execute("COMMIT")

        # delete all customer's sessions
        delete_customer_sessions_query = """delete from CustomerSession WHERE custometID = %s;"""
        cur.execute(delete_customer_sessions_query, (customer_id))
        cur.execute("COMMIT")

        # delete all customer's subscription history
        delete_customer_subscriptions_query = """delete from customerPlan WHERE custometID = %s;"""
        cur.execute(delete_customer_subscriptions_query, (customer_id))
        cur.execute("COMMIT")

    except Exception as e:
        # raise an exception if any error occur
        cur.execute("Rollback;")
        
def addSubscriptionPlan(subscription_plan,money,num_Sessions):
    cur = connect()
    q="INSERT INTO CraftStyle.SubscriptionPlan (Type, price, AllowedSessions) VALUES (%s, %s, %s);"
    cur.execute(q, (subscription_plan, money, num_Sessions))
    cur.execute("COMMIT")
    
def addPicture(customer_id,URL,Tag):
    cur = connect()
    q="INSERT INTO CraftStyle.Picture(customerID,pictureUrl,tags) VALUES (%s, %s, %s);"
    cur.execute(q, (customer_id,URL,Tag))
    cur.execute("COMMIT")
    
#------------------------------------------------------------------------------
#Creat schema and tables 
cur = connect()
cur.execute("CREATE SCHEMA if not EXISTS CraftStyle;")
cur.execute("COMMIT")

cur = connect()
cur.execute("CREATE table if not EXISTS CraftStyle.SubscriptionPlan(PlanID INT primary key GENERATED ALWAYS AS IDENTITY,Type varchar,price money not null,AllowedSessions float);")
cur.execute("COMMIT")

cur.execute("CREATE table if not EXISTS CraftStyle.Customer(CustomerID INT primary key GENERATED ALWAYS AS IDENTITY,Name varchar not null,sessionsNumber INT,subscriptionPlanID INT REFERENCES CraftStyle.SubscriptionPlan(planID));")
cur.execute("COMMIT")

cur.execute("CREATE table if not EXISTS CraftStyle.CustomerPlan(CustomerID INT REFERENCES CraftStyle.Customer(customerID),subscriptionPlanID INT REFERENCES CraftStyle.SubscriptionPlan(planID),purchaseDate date);")
cur.execute("CREATE table if not EXISTS CraftStyle.CustomerSession(CustomerSessionID INT primary key GENERATED ALWAYS AS IDENTITY,CustomerID INT REFERENCES CraftStyle.Customer(customerID),Recommendation text,pucturesNumber INT,tags varchar,sessionDate date);")
cur.execute("CREATE table if not EXISTS CraftStyle.Picture(pictureID INT primary key GENERATED ALWAYS AS IDENTITY,customerID INT REFERENCES CraftStyle.Customer(customerID),pictureUrl varchar,tags varchar);")
cur.execute("COMMIT")

cur.execute("CREATE table if not EXISTS CraftStyle.SessionPicture(SessionID INT REFERENCES CraftStyle.CustomerSession(customerSessionID),PictureID INT REFERENCES CraftStyle.Picture(pictureID));")
cur.execute("COMMIT")

#-----------------------------------------------------
#add rows to the tables 

#SubscriptionPlan
'''
addSubscriptionPlan('Basic', 0, 0)
addSubscriptionPlan('Advanced', 0.99, 'Infinity')
'''
 
#Customer
addCustomer('Farh')
addCustomer('Bob')
addCustomer('jo')
addCustomer('eli')
purchaseSubscription(1, 'Basic')
purchaseSubscription(2, 'Basic')
purchaseSubscription(2, 'Advanced')
purchaseSubscription(4, 'Basic')

#Picture
addPicture(1, 'https://drive.google.com/file/d/1UytPqBiPHJE4ES5jTToOr8BRRvLi2nT1/view?usp=sharing', 'rock')
addPicture(2, 'https://drive.google.com/file/d/1dT8WV288nerOT8PdG2HlYJCGND-ibCeZ/view?usp=sharing', 'casual, office')
addPicture(3, 'https://drive.google.com/file/d/1f6pIr-1ab7T9-Rc8j37zpJ0QiRwA0nA2/view?usp=share_link', 'casual')



    