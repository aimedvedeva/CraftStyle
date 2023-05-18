from connect_postgre import connect_postgre


def create_scheme():
    _create_craftStyle_scheme()


def create_tables():
    # create tables
    _create_subscription_plan_table()
    _create_customer_table()
    _create_customer_plan_table()
    _create_picture_table()


def _create_craftStyle_scheme():
    cur = connect_postgre()
    cur.execute("CREATE SCHEMA if not EXISTS CraftStyle;")
    cur.execute("COMMIT")


def _create_customer_plan_table():
    cur = connect_postgre()
    cur.execute("CREATE table if not EXISTS CraftStyle.CustomerPlan(customerId INT REFERENCES CraftStyle.Customer(customerId),\
                                                                    subscriptionPlanId INT REFERENCES CraftStyle.SubscriptionPlan(planId),\
                                                                    purchaseDate date,\
                                                                    expired boolean);")
    cur.execute("commit")


def _create_customer_table():
    cur = connect_postgre()
    cur.execute(
        "CREATE table if not EXISTS CraftStyle.Customer(customerId INT primary key GENERATED ALWAYS AS IDENTITY, \
                                                        name varchar not null,\
                                                        sessionsNumber INT,\
                                                        subscriptionPlanId INT REFERENCES CraftStyle.SubscriptionPlan(planId),\
                                                        balance money,\
                                                        registrationDate date);")
    cur.execute("COMMIT")


def _create_subscription_plan_table():
    cur = connect_postgre()
    cur.execute(
        "CREATE table if not EXISTS \
        CraftStyle.SubscriptionPlan(planId INT primary key GENERATED ALWAYS AS IDENTITY,\
                                    type varchar, \
                                    price money not null,\
                                    allowedSessions float, \
                                    launchDate date);")
    cur.execute("COMMIT")


def _create_picture_table():
    cur = connect_postgre()
    cur.execute(
        "CREATE table if not EXISTS CraftStyle.Picture(pictureId INT primary key GENERATED ALWAYS AS IDENTITY,\
        customerId INT REFERENCES CraftStyle.Customer(customerId),\
        pictureUrl varchar,\
        tags varchar,\
        uploadDate date);")
    cur.execute("COMMIT")
