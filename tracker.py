
import json
from lnmarkets import rest
import time


key = ""
secret = ""
passphrase = ""
options = {'key': f'{key}',
           'secret': f'{secret}',
           'passphrase': f'{passphrase}'}
lnm = rest.LNMarketsRest(**options)
lnm.futures_get_ticker()


def price_scrapper():

    while True:                                 
        indexP = lnm.futures_index_history({   
            'limit': 2
        })
        bidP = lnm.futures_bid_offer_history({  
            'limit': 2
        })
        priceRequests = json.loads(indexP)  
        bidOffer = json.loads(bidP)        
        priceIndex1 = priceRequests[1]    
        bidOffer1 = bidOffer[1]
        index = priceIndex1["index"]    
        bid = bidOffer1["bid"]
        offer = bidOffer1["offer"]

        with open("dataPrice.csv","a") as dataPrice:     
            dataPrice.write(f"{index},{bid},{offer}\n")   
            dataPrice.close()  
        
        time.sleep(30)
             
            

