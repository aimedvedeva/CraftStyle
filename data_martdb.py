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




#------------------------------------------------------------
#Analtical methodes 

import matplotlib.pyplot as plt
from collections import Counter


def plot_customer_funnel():
    # Retrieve the necessary data from the data mart table
    registered_count = get_count_by_activity('customer registered')
    purchased_count = get_count_by_activity('customer purchased a subscription plan')
    started_count = get_count_by_activity('customer started a session')
    deactivated_count = get_count_by_activity('customer deactivated')

    # Plot the customer funnel
    activities = ['Registered', 'Purchased Subscription', 'Started Session', 'Deactivated']
    counts = [registered_count, purchased_count, started_count, deactivated_count]

    plt.bar(activities, counts)
    plt.xlabel('Activity')
    plt.ylabel('Count')
    plt.title('Customer Funnel')
    plt.show()



def get_count_by_activity(activity):
    cur = connect_postgre()
    query = "SELECT COUNT(*) FROM CraftStyle.DataMart WHERE activity = %s;"
    cur.execute(query, (activity,))
    count = cur.fetchone()[0]
    return count




def plot_customer_status():
    # Retrieve the necessary data from the data mart table
    active_count = get_count_by_activity('customer started a session')
    non_active_count = get_count_by_activity('customer registered') + get_count_by_activity('customer purchased a subscription plan')

    # Create labels and sizes for the pie chart
    labels = ['Active Customers', 'Non-Active Customers']
    sizes = [active_count, non_active_count]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle
    ax.set_title('Customer Status')

    # Display the pie chart
    plt.show()



def get_top_tags():
    cur = connect_postgre()
    cur.execute("SELECT topTags FROM CraftStyle.DataMart")
    tags = cur.fetchall()
    # Collect tags and count their occurrences
    tags_counter = Counter()
    for tag in tags:
        top_tag = tag[0]
        if top_tag:
            tags_counter.update([top_tag])

    # Get the three most popular tags
    popular_tags = tags_counter.most_common(3)

    return popular_tags





def plot_session_frequencies_by_day(day):
    cur = connect_postgre()
    cur.execute("SELECT customerId FROM CraftStyle.DataMart WHERE activity = 'customer started a session' AND activityDate = %s", (day,))
    rows = cur.fetchall()

    # Count the frequency of sessions per customer
    session_counts = {}
    for row in rows:
        customer_id = row[0]
        session_counts[customer_id] = session_counts.get(customer_id, 0) + 1

    # Create histogram data
    frequencies = list(session_counts.values())

    # Plot the histogram
    plt.hist(frequencies, bins=range(min(frequencies), max(frequencies)+2), edgecolor='black')

    # Set labels and title
    plt.xlabel('Number of Sessions')
    plt.ylabel('Number of Customers')
    plt.title(f'Session Frequency Distribution on {day}')

    # Show the plot
    plt.show()




# Call the functions 
plot_customer_status()
plot_customer_funnel()
plot_session_frequencies_by_day('2023-05-21')
popular_tags = get_top_tags()
print('Three most popular tags among customer :')
for tag, count in popular_tags:
    print(f'Tag: {tag}, Count: {count}')