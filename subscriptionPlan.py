from connect_postgre import connect_postgre


def add_subscription_plan(subscription_plan, money, sessions_num):
    cur = connect_postgre()
    q = "INSERT INTO CraftStyle.SubscriptionPlan (type, price, allowedSessions, launchDate) VALUES (%s, %s, %s, current_date);"
    cur.execute(q, (subscription_plan, money, sessions_num))
    cur.execute("COMMIT")


def get_subscription_price(subscription_plan, cur):
    get_subscription_price = """select price from CraftStyle.SubscriptionPlan where type = %s"""
    cur.execute(get_subscription_price, (subscription_plan,))
    price = cur.fetchone()[0]
    price = float(price.replace('$', ''))
    return price


def get_subscription_plan_id(subscription_plan, cur):
    get_subscription_plan_id = """select planId from CraftStyle.SubscriptionPlan where type = %s"""
    cur.execute(get_subscription_plan_id, (subscription_plan,))
    plan_id = cur.fetchone()[0]
    return plan_id


def delete_subscription_plan(plan_id):
    cur = connect_postgre()
    delete_subscription_plan_query = """delete from CraftStyle.SubscriptionPlan WHERE planId = %s;"""
    cur.execute(delete_subscription_plan_query, (plan_id,))
    cur.execute("COMMIT")
