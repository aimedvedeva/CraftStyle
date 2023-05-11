from Customer import *

#Creat schema and tables 
cur = connect()
cur.execute("CREATE SCHEMA if not EXISTS CraftStyle;")
cur.execute("COMMIT")

cur = connect()
cur.execute("CREATE table if not EXISTS CraftStyle.SubscriptionPlan(PlanID INT primary key GENERATED ALWAYS AS IDENTITY,Type varchar,price money not null,AllowedSessions float);")
cur.execute("COMMIT")

cur.execute("CREATE table if not EXISTS CraftStyle.Customer(CustomerID INT primary key GENERATED ALWAYS AS IDENTITY,Name varchar not null,sessionsNumber INT,subscriptionPlanID INT REFERENCES CraftStyle.SubscriptionPlan(planID), balance INT);")
cur.execute("COMMIT")

cur.execute("CREATE table if not EXISTS CraftStyle.CustomerPlan(CustomerID INT REFERENCES CraftStyle.Customer(customerID),subscriptionPlanID INT REFERENCES CraftStyle.SubscriptionPlan(planID),purchaseDate date);")
cur.execute("CREATE table if not EXISTS CraftStyle.CustomerSession(CustomerSessionID INT primary key GENERATED ALWAYS AS IDENTITY,CustomerID INT REFERENCES CraftStyle.Customer(customerID),Recommendation text,pucturesNumber INT,tags varchar,sessionDate date);")
cur.execute("CREATE table if not EXISTS CraftStyle.Picture(pictureID INT primary key GENERATED ALWAYS AS IDENTITY,customerID INT REFERENCES CraftStyle.Customer(customerID),pictureUrl varchar,tags varchar);")
cur.execute("COMMIT")

cur.execute("CREATE table if not EXISTS CraftStyle.SessionPicture(SessionID INT REFERENCES CraftStyle.CustomerSession(customerSessionID),PictureID INT REFERENCES CraftStyle.Picture(pictureID));")
cur.execute("COMMIT")

#-----------------------------------------------------
#add rows to the tables 

#SubscriptionPlan
'''
addSubscriptionPlan('Basic', 0, 5)
addSubscriptionPlan('Advanced', 0.99, 'Infinity')
'''
 
#Customer
'''
addCustomer('Farh',0)
addCustomer('Bob',100)
addCustomer('jo',250)
addCustomer('eli',10)
purchaseSubscription(6, 'Basic')
purchaseSubscription(7, 'Basic')
purchaseSubscription(8, 'Advanced')
purchaseSubscription(9, 'Basic')
'''

#Picture
'''
addPicture(1, 'https://drive.google.com/file/d/1UytPqBiPHJE4ES5jTToOr8BRRvLi2nT1/view?usp=sharing', 'rock')
addPicture(2, 'https://drive.google.com/file/d/1dT8WV288nerOT8PdG2HlYJCGND-ibCeZ/view?usp=sharing', 'casual, office')
addPicture(3, 'https://drive.google.com/file/d/1f6pIr-1ab7T9-Rc8j37zpJ0QiRwA0nA2/view?usp=share_link', 'casual')
'''


    