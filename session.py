from connect import connect


def updateSessionRecommendation(session_id, recommendation):
    cur = connect()
    cur.execute("begin;")

    cur.execute("""UPDATE customerSession SET recommendation = %s WHERE custometSessionID = %s;""", \
                (recommendation, session_id))

    cur.execute("commit")