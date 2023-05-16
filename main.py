from populate import populate
from session import *
if __name__ == '__main__':
    x=0
    populate()
    while x<10000:
         createSession(11,'rget','office')
         deleteCustomerSessions(11)
         x+=1
    

    
   