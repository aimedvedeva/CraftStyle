from connect_postgre import connect

def createPictureTable():
    cur = connect()
    cur.execute(
        "CREATE table if not EXISTS CraftStyle.Picture(pictureId INT primary key GENERATED ALWAYS AS IDENTITY,\
        customerId INT REFERENCES CraftStyle.Customer(customerId),\
        pictureUrl varchar,\
        tags varchar,\
        uploadDate date);")
    cur.execute("COMMIT")

def addPicture(customer_id, picture_url, tags):
    cur = connect()
    q="INSERT INTO CraftStyle.Picture(customerID,pictureUrl,tags, upload_date) VALUES (%s, %s, %s, current_date);"
    cur.execute(q, (customer_id, picture_url, tags))
    cur.execute("COMMIT")

def deletePicture(picture_id):
    cur = connect()
    delete_picture_query = """delete from CraftStyle.Picture WHERE pictureId = %s;"""
    cur.execute(delete_picture_query, (picture_id,))
    cur.execute("COMMIT")



