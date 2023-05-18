from connect_postgre import connect_postgre
from customer import get_customer_balance, reduce_customer_balance, get_current_customer_subscription_plan, \
    inactivate_customer_subscription_plan, add_customer_subscription_plan
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