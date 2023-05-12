from connect import connect

def createPictureTable():
    cur = connect()
    cur.execute(
        "CREATE table if not EXISTS CraftStyle.Picture(pictureId INT primary key GENERATED ALWAYS AS IDENTITY,\
        customerId INT REFERENCES CraftStyle.Customer(customerId),\
        pictureUrl varchar,\
        tags varchar,\
        uploadDate date);")
    cur.execute("COMMIT")

def addPicture(customer_id, URL, Tag):
    cur = connect()
    q="INSERT INTO CraftStyle.Picture(customerID,pictureUrl,tags, upload_date) VALUES (%s, %s, %s, current_date);"
    cur.execute(q, (customer_id, URL, Tag))
    cur.execute("COMMIT")

