from connect_postgre import connect_postgre


def add_picture(customer_id, picture_url, tags):
    cur = connect_postgre()
    add_picture_query = "INSERT INTO CraftStyle.Picture(customerID, pictureUrl, tags, uploaddate) VALUES (%s, %s, %s, current_date);"
    cur.execute(add_picture_query, (customer_id, picture_url, tags))
    cur.execute("COMMIT")


def delete_picture(picture_id):
    cur = connect_postgre()
    delete_picture_query = """delete from CraftStyle.Picture WHERE pictureId = %s;"""
    cur.execute(delete_picture_query, (picture_id,))
    cur.execute("COMMIT")
