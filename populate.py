from craftStyle import *
from customer import *
from picture import *
from subscriptionPlan import *
from  session import *
from  recommendation import *



def populate():
    # create scheme
    createCraftStyleScheme()

    # create tables
    createSubscriptionPlanTable()
    createCustomerTable()
    createCustomerPlanTable()
    createPictureTable()

    #insert data into tables

    #SubscriptionPlan
    addSubscriptionPlan('Basic', 0, 5)
    addSubscriptionPlan('Premium', 0.99, 'Infinity')

    #Customer
    addCustomer('Farh', 0)
    addCustomer('Bob', 100)
    addCustomer('jo', 0)
    addCustomer('eli', 10)

    #CustomerPlan
    cur = connectsgl()
    purchaseSubscription(1, 'Basic')
    purchaseSubscription(2, 'Premium') # does have enough money for subscription
    purchaseSubscription(3, 'Premium') # doesn't have enough money for subscription
    purchaseSubscription(4, 'Basic')
    purchaseSubscription(4, 'Premium') # upgrade his subscription plan
    purchaseSubscription(4, 'Premium') # upgrade his subscription plan
    purchaseSubscription(3, 'Basic')
    processPurchase(1, 'Basic',cur)
    processPurchase(2, 'Premium',cur)
    processPurchase(4, 'Premium',cur)
    processPurchase(3, 'Basic',cur)
    # #Picture
    # addPicture(1, 'https://drive.google.com/file/d/1UytPqBiPHJE4ES5jTToOr8BRRvLi2nT1/view?usp=sharing', 'rock')
    # addPicture(2, 'https://drive.google.com/file/d/1dT8WV288nerOT8PdG2HlYJCGND-ibCeZ/view?usp=sharing', 'casual, office')
    # addPicture(3, 'https://drive.google.com/file/d/1f6pIr-1ab7T9-Rc8j37zpJ0QiRwA0nA2/view?usp=share_link', 'casual')
    #image_urls='https://media.istockphoto.com/id/1340959863/photo/blue-sweater-isolated-on-white-casual-vintage-knitted-sweater-wool-cardigan-top-view.jpg?s=1024x1024&w=is&k=20&c=4VUma3z_kofKT1qrurpkZx7DhTaMcU_QQqyjRYIiz8Q='
    #image_urls='https://media.istockphoto.com/id/1324847242/photo/pair-of-white-leather-trainers-on-white-background.jpg?s=1024x1024&w=is&k=20&c=paCekjw8iHTIKD4jpPXPdZY60gtOgbXV3pO9k1OTASo='


#-------------------------------------------------------------------------------------------------------------------
#Populate redis



image_urls='https://media.istockphoto.com/id/1324847242/photo/pair-of-white-leather-trainers-on-white-background.jpg?s=1024x1024&w=is&k=20&c=paCekjw8iHTIKD4jpPXPdZY60gtOgbXV3pO9k1OTASo='
style_tags='casual'

customer_id=3

session_id=createSession(customer_id, image_urls, style_tags)
session_data = getSession(session_id)
print(session_data)
deleteSession(session_id)
session_data = getSession(session_id)
print(session_data)