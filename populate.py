from craftStyle import purchase_subscription
from customer import add_customer
from session import create_session, get_session, delete_session
from subscriptionPlan import add_subscription_plan


def populate_postgre():
    # insert data into tables

    # SubscriptionPlan
    add_subscription_plan('Basic', 0, 5)
    add_subscription_plan('Premium', 0.99, 'Infinity')

    # Customer
    add_customer('Farh', 0)
    add_customer('Bob', 100)
    add_customer('jo', 0)
    add_customer('eli', 10)

    # CustomerPlan
    purchase_subscription(1, 'Basic')
    purchase_subscription(2, 'Premium')  # does have enough money for subscription
    purchase_subscription(3, 'Premium')  # doesn't have enough money for subscription
    purchase_subscription(4, 'Basic')
    purchase_subscription(4, 'Premium')  # upgrade his subscription plan
    purchase_subscription(4, 'Premium')  # upgrade his subscription plan
    purchase_subscription(3, 'Basic')

    # #Picture
    # addPicture(1, 'https://drive.google.com/file/d/1UytPqBiPHJE4ES5jTToOr8BRRvLi2nT1/view?usp=sharing', 'rock')
    # addPicture(2, 'https://drive.google.com/file/d/1dT8WV288nerOT8PdG2HlYJCGND-ibCeZ/view?usp=sharing', 'casual, office')
    # addPicture(3, 'https://drive.google.com/file/d/1f6pIr-1ab7T9-Rc8j37zpJ0QiRwA0nA2/view?usp=share_link', 'casual')
    # image_urls='https://media.istockphoto.com/id/1340959863/photo/blue-sweater-isolated-on-white-casual-vintage-knitted-sweater-wool-cardigan-top-view.jpg?s=1024x1024&w=is&k=20&c=4VUma3z_kofKT1qrurpkZx7DhTaMcU_QQqyjRYIiz8Q='
    # image_urls='https://media.istockphoto.com/id/1324847242/photo/pair-of-white-leather-trainers-on-white-background.jpg?s=1024x1024&w=is&k=20&c=paCekjw8iHTIKD4jpPXPdZY60gtOgbXV3pO9k1OTASo='


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
