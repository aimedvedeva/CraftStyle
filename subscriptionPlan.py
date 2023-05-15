from connect_postgre import *


def createSubscriptionPlanTable():
    cur = connectsgl()
    cur.execute(
        "CREATE table if not EXISTS \
        CraftStyle.SubscriptionPlan(planId INT primary key GENERATED ALWAYS AS IDENTITY,\
                                    type varchar, \
                                    price money not null,\
                                    allowedSessions float, \
                                    launchDate date);")
    cur.execute("COMMIT")

def addSubscriptionPlan(subscription_plan, money, sessions_num, cur):
    q="INSERT INTO CraftStyle.SubscriptionPlan (type, price, allowedSessions, launchDate) VALUES (%s, %s, %s, current_date);"
    cur.execute(q, (subscription_plan, money, sessions_num))
    cur.execute("COMMIT")

def getSubscriptionPrice(subscription_plan, cur):
    get_subscription_price = """select price from CraftStyle.SubscriptionPlan where type = %s"""
    cur.execute(get_subscription_price, (subscription_plan,))
    price = cur.fetchone()[0]
    price = float(price.replace('$', ''))
    return price

def getSubscriptionPlanId(subscription_plan, cur):
    get_subscription_plan_id = """select planId from CraftStyle.SubscriptionPlan where type = %s"""
    cur.execute(get_subscription_plan_id, (subscription_plan,))
    plan_id = cur.fetchone()[0]
    return plan_id

def deleteSubscriptionPlan(plan_id):
    cur = connectsgl()
    cur.execute("set transaction isolation level serializable;")
    cur.execute("begin;")

    try:
        delete_subscription_plan_query = """delete from CraftStyle.SubscriptionPlan WHERE planId = %s;"""
        cur.execute(delete_subscription_plan_query, (plan_id,))
        cur.execute("COMMIT")

    except Exception as e:
        # raise an exception if any error occur
        cur.execute("Rollback;")