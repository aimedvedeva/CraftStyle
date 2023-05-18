from connect_postgre import connect_postgre
from session import delete_customer_sessions


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
