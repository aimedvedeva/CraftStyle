from datetime import date

from connect_postgre import connect_postgre
from connect_redis import connect_redis
from picture import add_picture
from recommendation import get_recommendation
from session import delete_session, update_session_recommendation, create_session
from subscriptionPlan import get_subscription_plan_allowed_sessions


def add_customer(name, money):
    cur = connect_postgre()
    cur.execute("begin;")

    create_customer_query = """INSERT INTO CraftStyle.Customer(name, sessionsNumber, subscriptionPlanId, balance, registrationDate)\
                                                                VALUES (%s, %s, NULL, %s, current_date);"""
    cur.execute(create_customer_query, (name, 0, money))
    cur.execute("commit")


def delete_customer(customer_id):
    # since customer_id is a foreign key for CustomerSession, Picture and CustomerPlan
    # firstly, we have to delete corresponding rows there
    # and finally from Customer table

    cur = connect_postgre()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    try:
        # delete all customers' pictures
        delete_customer_pictures_query = """delete from CraftStyle.Picture WHERE custometId = %s;"""
        cur.execute(delete_customer_pictures_query, (customer_id))

        # delete all customer's sessions
        delete_customer_sessions(customer_id)

        # delete all customer's subscription history
        delete_customer_subscriptions_query = """delete from CraftStyle.customerPlan WHERE custometId = %s;"""
        cur.execute(delete_customer_subscriptions_query, (customer_id))

        cur.execute("COMMIT")
    except Exception as e:
        # raise an exception if any error occur
        cur.execute("Rollback;")


def get_customer_balance(customer_id, cur):
    get_customer_balance = """select balance from CraftStyle.Customer where customerId = %s"""
    cur.execute(get_customer_balance, (customer_id,))
    balance = cur.fetchone()[0]
    balance = float(balance.replace('$', ''))
    return balance


def reduce_customer_balance(customer_id, new_balance, cur):
    update_balance_query = """UPDATE CraftStyle.Customer set balance = cast(%s as money) where customerId = %s;"""
    cur.execute(update_balance_query, (new_balance, customer_id))


def get_customer_sessions_number(customer_id):
    cur = connect_postgre()
    query = "SELECT sessionsnumber FROM CraftStyle.customer WHERE customerid = %s;"
    cur.execute(query, (customer_id,))
    sessions_number = cur.fetchone()[0]
    return sessions_number


def update_customer_sessions_number(customer_id):
    cur = connect_postgre()
    sessions_number = get_customer_sessions_number(customer_id) + 1
    q = "UPDATE CraftStyle.customer SET sessionsnumber = %s WHERE customerid = %s;"
    cur.execute(q, (sessions_number, customer_id))


def get_current_customer_subscription_plan(customer_id):
    cur = connect_postgre()
    check_active_subscription_query = """select sp."type"
    from CraftStyle.CustomerPlan cp 
    join CraftStyle.SubscriptionPlan sp on cp.subscriptionPlanId = sp.planId
    where cp.customerId = %s
    and cp.expired = '0';"""

    cur.execute(check_active_subscription_query, (customer_id,))

    current_subscription_plan = cur.fetchone()
    if current_subscription_plan is not None:
        current_subscription_plan = current_subscription_plan[0]

    return current_subscription_plan


def inactivate_customer_subscription_plan(cur, customer_id):
    # inactivate old subscription
    inactivate_basic_query = """UPDATE CraftStyle.CustomerPlan set expired = '1' \
                                  where customerId = %s;"""
    cur.execute(inactivate_basic_query, (customer_id,))


def add_customer_subscription_plan(cur, customer_id, plan_id):
    q1 = "INSERT INTO CraftStyle.CustomerPlan \
    (customerId, subscriptionPlanId, purchaseDate, expired) VALUES (%s, %s, current_date, '0');"
    cur.execute(q1, (customer_id, plan_id))
    q2 = "UPDATE CraftStyle.customer SET subscriptionplanid = %s WHERE customerid = %s;"
    cur.execute(q2, (plan_id, customer_id))


def delete_customer_sessions(customer_id):
    redis_client = connect_redis()

    # Get all session IDs for the customer
    session_ids = redis_client.zrange(f'craft_style_sessions:{customer_id}', 0, -1)

    # Delete session data and remove session IDs from the Sorted Set
    pipeline = redis_client.pipeline()
    for session_id in session_ids:
        delete_session(session_id)
    pipeline.delete(f'craft_style_sessions:{customer_id}')
    pipeline.execute()


# just create empty session
def _create_customer_session(customer_id, tags, picture_urls):
    session_id = create_session(customer_id, picture_urls, tags, date.today())
    _upload_customer_session_pictures(customer_id, picture_urls, tags)
    return session_id


def _upload_customer_session_pictures(customer_id, picture_urls, tags):
    for picture_url in picture_urls:
        add_picture(customer_id, picture_url, tags)


# just process the lifecycle of normal session: create, generate recommendation
def _process_customer_session(customer_id, tags, picture_urls):
    session_id = _create_customer_session(customer_id, tags, picture_urls)
    recommendation = get_recommendation(picture_urls, tags)
    update_session_recommendation(session_id, recommendation)


def launch_customer_session(customer_id, tags, picture_urls):
    customer_subscription_plan = get_current_customer_subscription_plan(customer_id)

    if customer_subscription_plan == 'Premium':
        _process_customer_session(customer_id, tags, picture_urls)

    elif customer_subscription_plan == 'Basic':
        sessions_number = get_customer_sessions_number(customer_id)
        allowed_sessions = get_subscription_plan_allowed_sessions(customer_subscription_plan)

        if sessions_number < allowed_sessions:
            _process_customer_session(customer_id, tags, picture_urls)
        else:
            raise ValueError("You reached maximum allowed sessions for basic plan. Please, upgrade your plan")

    else:
        raise ValueError("Please, purchase a subscription plan")
