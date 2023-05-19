from populate import populate_redis_with_sessions

if __name__ == '__main__':
    # create_scheme()
    # create_tables()
    # populate_postgre_tables()
    # populate_subscriptions()

    # 1. Smart cache. Keep copies of entities from PostgreSQL database in Redis + calculate / check counters.
    # (like an active sessions count).

    sessions_number = 0
    while sessions_number < 10:
        populate_redis_with_sessions()
        sessions_number += 1