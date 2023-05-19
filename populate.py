from craftStyle import purchase_subscription
from customer import add_customer
from session import create_session, get_session, delete_session
from subscriptionPlan import add_subscription_plan


def populate_postgre_tables():
    # insert data into tables

    # SubscriptionPlan
    #add_subscription_plan('Basic', 0, 5)
    #add_subscription_plan('Premium', 0.99, 'Infinity')

    # Customer
    add_customer('Farh', 0)
    add_customer('Bob', 100)
    add_customer('jo', 0)
    add_customer('eli', 10)

def populate_subscriptions():
    # CustomerPlan
    purchase_subscription(9, 'Basic')
    purchase_subscription(10, 'Premium')  # does have enough money for subscription
    purchase_subscription(11, 'Premium')  # doesn't have enough money for subscription
    purchase_subscription(12, 'Basic')
    purchase_subscription(12, 'Premium')  # upgrade his subscription plan
    purchase_subscription(12, 'Premium')  # upgrade his subscription plan
    purchase_subscription(11, 'Basic')

def populate_redis():
    # generate / hardcode example data
    image_urls = [
        'https://drive.google.com/your-image-url1.jpg',
        'https://drive.google.com/your-image-url2.jpg',
        'https://drive.google.com/your-image-url3.jpg'
    ]
    style_tags = ['casual', 'formal', 'sporty']
    customer_id = 3

    # create session
    session_id = create_session(customer_id, image_urls, style_tags)
    session_data = get_session(session_id)
    print(session_data)

    # delete session
    delete_session(session_id)
    session_data = get_session(session_id)
    print(session_data)
