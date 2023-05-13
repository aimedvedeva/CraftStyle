from connect import connect
from customer import getCustomerBalance, reduceCustomerBalance
from subscriptionPlan import getSubscriptionPrice, getSubscriptionPlanId


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

# def createCustomerSessionTable():
#     cur = connect()
#     cur.execute(
#         "CREATE table if not EXISTS CraftStyle.CustomerSession(customerSessionId INT primary key GENERATED ALWAYS AS IDENTITY,\
#         customerId INT REFERENCES CraftStyle.Customer(customerId),\
#         recommendation text,\
#         pucturesNumber INT,\
#         tags varchar,\
#         sessionDate date);")
#     cur.execute("commit")


# def createPictureSessionTable():
#     cur = connect()
#     cur.execute(
#         "CREATE table if not EXISTS CraftStyle.SessionPicture(sessionId INT REFERENCES CraftStyle.CustomerSession(customerSessionId),\
#         pictureId INT REFERENCES CraftStyle.Picture(pictureId));")
#     cur.execute("COMMIT")

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

# def createCustomerSession(customer_id, pictures, picure_links, tags):
#     cur = connect()
#     cur.execute("set transaction isolation level serializable;")
#     cur.execute("begin;")
#
#     try:
#         # get allowed_sessions of a customer's subscription plan
#         cur.execute("""select s.allowedsessions \
#                        from subscriptionplan s \
#                        join customerplan c on s.planid = c.subscriptionplanid where customerID = %s""", (customer_id))
#         allowed_sessions = cur.fetchone()[0]
#
#         # get number of sessions that the customer has already had
#         cur.execute("""select c.sessionsnumber from customer c where c.customerid = %s;""", (customer_id))
#         done_sessions = cur.fetchone()[0]
#
#         # check if the customer doesn't exceed the limit according to his subscription plan
#         if done_sessions >= allowed_sessions:
#             raise ValueError("Unfortunately, all you free sessions have already used. You can upgrade you subscription plan.")
#
#         update_sessions_number_query = """UPDATE customer SET sessionsnumber = sessionsnumber + 1 WHERE custometID = %s;"""
#
#         cur.execute(update_sessions_number_query, (customer_id))
#
#         # save data about the session
#         cur.execute("""INSERT INTO CustomerSession(customerID, Recommendation, pucturesNumber, tags, sessionDate)
#         VALUES(%s, NULL, %s, %s, current_date);""", (customer_id, len(pictures), tags))
#
#         # save pictures
#         for picture, link in zip(pictures, picure_links):
#             cur.execute("""INSERT INTO Picture(customerID, pictureUrl, tags) VALUES(%s, %s, %s);""",\
#                         (customer_id, link, tags))
#         cur.execute("COMMIT")
#
#     except Exception as e:
#         # raise an exception if any error occur
#         cur.execute("Rollback;")
