from connect_postgre import connect
from customer import getCustomerBalance, reduceCustomerBalance
from picture import addPicture
from recommendation import getRecommendation
from session import createSession, generateSessionId, updateSessionRecommendation
from subscriptionPlan import getSubscriptionPrice, getSubscriptionPlanId
from datetime import date

def createCraftStyleScheme():
    cur = connect()
    cur.execute("CREATE SCHEMA if not EXISTS CraftStyle;")
    cur.execute("COMMIT")

def createCustomerPlanTable():
    cur = connect()
    cur.execute("CREATE table if not EXISTS CraftStyle.CustomerPlan(customerId INT REFERENCES CraftStyle.Customer(customerId),\
                                                                    subscriptionPlanId INT REFERENCES CraftStyle.SubscriptionPlan(planId),\
                                                                    purchaseDate date,\
                                                                    expired boolean);")
    cur.execute("commit")

def purchaseSubscription(customer_id, subscription_plan):
    cur = connect()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    try:
        # check if customer already have any type of active subscription
        current_subscription_plan = getCurrentCustomerSubscriptionPlan(cur, customer_id)

        if current_subscription_plan == subscription_plan:
            raise ValueError("Customer has already have the ", subscription_plan,  " subscription plan.")

        elif current_subscription_plan is not None and current_subscription_plan != subscription_plan:
            # the customer wants another type of subscription
            if subscription_plan == 'Premium':
                processPurchase(customer_id, subscription_plan, cur)
                inactivateCustomerSubscriptionPlan(cur, customer_id)
                # activate new subscription
                plan_id = getSubscriptionPlanId('Premium', cur)
                addCustomerSubscriptionPlan(cur, customer_id, plan_id)

            elif subscription_plan == 'Basic':
                raise ValueError("Hey, guy, there is no point to change degrade your subscription to basic one")

        elif current_subscription_plan is None:
            processPurchase(customer_id, subscription_plan, cur)

            # add desirable subscription for the customer
            plan_id = getSubscriptionPlanId(subscription_plan, cur)
            addCustomerSubscriptionPlan(cur, customer_id, plan_id)
        cur.execute("commit")

    except Exception as e:
        # if any error occur
        cur.execute("rollback")

def processPurchase(customer_id, subscription_plan, cur):
    # get balance
    balance = getCustomerBalance(customer_id, cur)

    # get subscription price
    price = getSubscriptionPrice(subscription_plan, cur)

    if price > balance:
        raise ValueError("There is no enough money to buy a subscription")

    # update customer's balance
    reduceCustomerBalance(customer_id, balance - price, cur)

def inactivateCustomerSubscriptionPlan(cur, customer_id):
    # inactivate old subscription
    inactivate_basic_query = """UPDATE CraftStyle.CustomerPlan set expired = '1' \
                                  where customerId = %s;"""
    cur.execute(inactivate_basic_query, (customer_id,))

def addCustomerSubscriptionPlan(cur, customer_id, plan_id):
    create_customer_plan_query = "INSERT INTO CraftStyle.CustomerPlan \
    (customerId, subscriptionPlanId, purchaseDate, expired) VALUES (%s, %s, current_date, '0');"
    cur.execute(create_customer_plan_query, (customer_id, plan_id))


def getCurrentCustomerSubscriptionPlan(cur, customer_id):
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

def createCustomerSession(customer_id, tags, picture_urls):
    session_id = generateSessionId()
    recommendation = None
    number_of_pictures = len(picture_urls)
    createSession(customer_id, session_id, recommendation, number_of_pictures, tags, date.today())

    uploadSessionPictures(picture_urls)
    return session_id


def uploadSessionPictures(customer_id, picture_urls, tags):
    for picture_url in picture_urls:
        addPicture(customer_id, picture_url, tags)

def processCustomerSession(customer_id, tags, picture_urls):
    session_id = createCustomerSession(customer_id, tags, picture_urls)
    recommendation = getRecommendation(picture_urls, tags)
    updateSessionRecommendation(session_id, recommendation)
