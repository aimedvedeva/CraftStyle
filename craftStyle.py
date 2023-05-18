from connect_postgre import connect_postgre
from customer import get_customer_balance, reduce_customer_balance
from picture import add_picture
from subscriptionPlan import get_subscription_plan_id, get_subscription_price


def purchase_subscription(customer_id, subscription_plan):
    cur = connect_postgre()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    try:
        # check if customer already have any type of active subscription
        current_subscription_plan = get_current_customer_subscription_plan(cur, customer_id)

        if current_subscription_plan == subscription_plan:
            raise ValueError("Customer has already have the ", subscription_plan, " subscription plan.")

        elif current_subscription_plan is not None and current_subscription_plan != subscription_plan:
            # the customer wants another type of subscription
            if subscription_plan == 'Premium':
                _process_purchase(customer_id, subscription_plan, cur)
                inactivate_customer_subscription_plan(cur, customer_id)
                # activate new subscription
                plan_id = get_subscription_plan_id('Premium', cur)
                add_customer_subscription_plan(cur, customer_id, plan_id)

            elif subscription_plan == 'Basic':
                raise ValueError("Hey, guy, there is no point to change degrade your subscription to basic one")

        elif current_subscription_plan is None:
            _process_purchase(customer_id, subscription_plan, cur)

            # add desirable subscription for the customer
            plan_id = get_subscription_plan_id(subscription_plan, cur)
            add_customer_subscription_plan(cur, customer_id, plan_id)
        cur.execute("commit")

    except Exception as e:
        # if any error occur
        cur.execute("rollback")


def _process_purchase(customer_id, subscription_plan, cur):
    # get balance
    balance = get_customer_balance(customer_id, cur)

    # get subscription price
    price = get_subscription_price(subscription_plan, cur)

    if price > balance:
        raise ValueError("There is no enough money to buy a subscription")

    # update customer's balance
    reduce_customer_balance(customer_id, balance - price, cur)
    plan_id = get_subscription_plan_id(subscription_plan, cur)
    add_customer_subscription_plan(cur, customer_id, plan_id)
    q2 = "UPDATE CraftStyle.customer SET subscriptionplanid = %s WHERE customerid = %s;"
    cur.execute(q2, (plan_id, customer_id))


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


# def createCustomerSession(customer_id, tags, picture_urls):
#     session_id = generateSessionId()
#     recommendation = None
#     number_of_pictures = len(picture_urls)
#     createSession(customer_id, session_id, recommendation, number_of_pictures, tags, date.today())

#     uploadSessionPictures(picture_urls)
#     return session_id


def upload_session_pictures(customer_id, picture_urls, tags):
    for picture_url in picture_urls:
        add_picture(customer_id, picture_url, tags)

# def processCustomerSession(customer_id, tags, picture_urls):
#     session_id = createCustomerSession(customer_id, tags, picture_urls)
#     recommendation = getRecommendation(picture_urls, tags)
#     updateSessionRecommendation(session_id, recommendation)
