import psycopg2

def connectsgl():
    conn = psycopg2.connect(database="postgres", user="student",\
                            password="HSDStoTestDb3711", host="database-1.czcdhgn8biyx.us-east-1.rds.amazonaws.com", port="5432")
    return conn.cursor()
