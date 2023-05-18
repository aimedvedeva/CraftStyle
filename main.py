from populate import populate_postgre

if __name__ == '__main__':
    populate_postgre()

    # 1. Smart cache. Keep copies of entities from PostgreSQL database in Redis + calculate / check counters.
    # (like an active sessions count).

    # sessions_number = 0
    # while sessions_number < 10000:
    #      createSession(11, 'rget' , 'office')
    #      deleteCustomerSessions(11)
    #      sessions_number += 1
