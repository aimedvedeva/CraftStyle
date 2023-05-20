import psycopg2
from customer import *


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


def register_info_mart(name):
    cur = connect_postgre()
    cur.execute("SELECT customerId FROM CraftStyle.Customer WHERE name = %s;", (name,))
    customer_id = cur.fetchone()[0]  # Get the customer ID after insertion
    activity = 'customer registered'
    insert_query = "INSERT INTO CraftStyle.DataMart (customerId, activityDate, activity, " \
                   "sessionNumber, topTags, subscriptionPlanId) " \
                   "VALUES (%s, %s, %s, NULL, NULL, NULL);"
    cur.execute(insert_query, (customer_id, date.today(), activity))
    cur.execute("COMMIT")


def deactivat_info_mart(customer_id):
    cur = connect_postgre()
    # If customer deleted insert data into the DataMart table

    activity = 'customer deactivated'
    insert_query = "INSERT INTO CraftStyle.DataMart (customerId, activityDate, activity, " \
                   "sessionNumber, topTags, subscriptionPlanId) " \
                   "VALUES (%s, %s, %s, NULL, NULL, NULL);"
    cur.execute(insert_query, (customer_id, date.today(), activity))
    cur.execute("COMMIT")


def purchased_info_mart(customer_id, plan_id):
    cur = connect_postgre()
    activity = 'customer purchased a subscription plan'
    insert_query = "INSERT INTO CraftStyle.DataMart (customerId, activityDate, activity, " \
                   "sessionNumber, topTags, subscriptionPlanId) " \
                   "VALUES (%s, %s, %s, %s, NULL, %s);"
    cur.execute(insert_query, (customer_id, date.today(), activity, 0, plan_id))
    cur.execute("COMMIT")
