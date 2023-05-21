from craftstyle import purchase_subscription
from customer import add_customer, launch_customer_session
from data_martdb import session_info_mart, register_info_mart
from session import create_session, get_session, delete_session
from subscription_plan import add_subscription_plan


def populate_postgre_tables():
    # insert data into tables

    # SubscriptionPlan
    add_subscription_plan('Basic', 0, 5)
    add_subscription_plan('Premium', 0.99, 'Infinity')

    # Customer
    add_customer('Farh', 0)
    add_customer('Bob', 100)
    add_customer('jo', 0)
    add_customer('eli', 10)
    add_customer('rudy', 0)
    
    register_info_mart('rudy')
    register_info_mart('Farh')
    register_info_mart('Bob')
    register_info_mart('jo')
    register_info_mart('eli')


def populate_subscriptions():
    # CustomerPlan
    purchase_subscription(9, 'Basic')
    purchase_subscription(10, 'Premium')  # does have enough money for subscription
    purchase_subscription(11, 'Premium')  # doesn't have enough money for subscription
    purchase_subscription(12, 'Basic')
    purchase_subscription(12, 'Premium')  # upgrade his subscription plan
    purchase_subscription(12, 'Premium')  # upgrade his subscription plan
    purchase_subscription(11, 'Basic')


def populate_redis_with_sessions():
    # generate / hardcode example data
    picture_urls = [
        'https://drive.google.com/your-image-url1.jpg',
        'https://drive.google.com/your-image-url2.jpg',
        'https://drive.google.com/your-image-url3.jpg'
    ]
    tags = 'casual, formal, sport'
    customer_id = 12

    # launch session
    session_id = launch_customer_session(customer_id, tags, picture_urls)
    session_data = get_session(session_id)
    print(session_data)

    # save information to datamart
    session_info_mart(customer_id, session_data)

    # delete session
    delete_session(session_id)
    session_data = get_session(session_id)
    print(session_data)
    
    


