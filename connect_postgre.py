import psycopg2


def connect_postgre():
    conn = psycopg2.connect()
    return conn.cursor()
