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
    session_number = get_customer_sessions_number(cur, customer_id)
    # get the most frequent tag
    tags_statistics = get_customer_tags_statistics(customer_id)
    top_tags = tags_statistics.most_common(1)[0][0]

    # Insert data into the DataMart table
    insert_query = "INSERT INTO CraftStyle.DataMart (customerId, activityDate, activity, " \
                   "sessionNumber, topTags, subscriptionPlanId) " \
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


def deactivate_info_mart(customer_id):
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
