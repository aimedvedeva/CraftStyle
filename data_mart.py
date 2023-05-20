import psycopg2
from customer import *

def connect_postgre():
    conn = psycopg2.connect(database="postgres", user="student",
                            password="HSDStoTestDb3711",
                            host="database-1.czcdhgn8biyx.us-east-1.rds.amazonaws.com",
                            port="5432")
    return conn.cursor()


def data_mart_table():
    cur = connect_postgre()
    cur.execute("CREATE TABLE IF NOT EXISTS CraftStyle.DataMart ("
                "customerId INT REFERENCES CraftStyle.Customer(customerId),"
                "activityDate DATE,"
                "activity VARCHAR,"
                "sessionNumber INT,"
                "topTags VARCHAR,"
                "subscriptionPlanId INT REFERENCES CraftStyle.SubscriptionPlan(planId)"
                ");")
    cur.execute("COMMIT")


def session_info_mart(customer_id, activity_date):
    cur = connect_postgre()

    # Retrieve remaining values from other functions
    subscription_plan_id = get_current_customer_subscription_plan(cur, customer_id)
    activity = 'customer started a session'
    session_number = get_current_customer_subscription_plan(customer_id)
    # Determine the most frequent tag
    customer_tags = get_customer_tags(customer_id)
    tag_counter = Counter(customer_tags)
    top_tags = tag_counter.most_common(1)[0][0]

    # Insert data into the DataMart table
    insert_query = "INSERT INTO CraftStyle.DataMart (customerId, activityDate, activity, sessionNumber, topTags, subscriptionPlanId) " \
                   "VALUES (%s, %s, %s, %s, %s, %s);"
    cur.execute(insert_query, (customer_id, activity_date, activity, session_number, top_tags, subscription_plan_id))
    cur.execute("COMMIT")

data_mart_table()

