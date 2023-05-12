from craftStyle import createCraftStyleScheme, createCustomerPlanTable, purchaseSubscription
from customer import createCustomerTable, addCustomer
from picture import createPictureTable
from subscriptionPlan import createSubscriptionPlanTable, addSubscriptionPlan

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
    purchaseSubscription(1, 'Basic')
    purchaseSubscription(2, 'Premium') # does have enough money for subscription
    purchaseSubscription(3, 'Premium') # doesn't have enough money for subscription
    purchaseSubscription(4, 'Basic')
    purchaseSubscription(4, 'Premium') # upgrade his subscription plan
    purchaseSubscription(4, 'Premium') # upgrade his subscription plan

    # #Picture
    # addPicture(1, 'https://drive.google.com/file/d/1UytPqBiPHJE4ES5jTToOr8BRRvLi2nT1/view?usp=sharing', 'rock')
    # addPicture(2, 'https://drive.google.com/file/d/1dT8WV288nerOT8PdG2HlYJCGND-ibCeZ/view?usp=sharing', 'casual, office')
    # addPicture(3, 'https://drive.google.com/file/d/1f6pIr-1ab7T9-Rc8j37zpJ0QiRwA0nA2/view?usp=share_link', 'casual')
