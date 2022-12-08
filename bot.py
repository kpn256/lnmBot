
from lnm_class import Trading as tr
import tracker as tracker
import time


def bot():

    while True:
        DataPrice = open("dataPrice.csv","r")             
        lastline = DataPrice.readlines()[-1].split(",")   
        DataPrice.close()                                  
        priceIndex = lastline[0]                           
        priceBid = lastline[1]
        priceOffer = lastline[2]
        changeindex = float(priceIndex) * 0.005
        indexlimitUp = changeindex + float(priceIndex)
        indexlimitDown = float(priceIndex) - changeindex

        if float(priceIndex) >= float(indexlimitUp):
            print("AHORA!!!!!!")
            
        print(f"limitdown{indexlimitDown}")
        print(f"limitUp{indexlimitUp}")
        print(f"index{priceIndex}")
        time.sleep(240)

        
index = tracker.index
bid = tracker.bid
offer = tracker.offer

def rsi():
    pass

def bollinger():
    pass

def trade():

    if bollinger == 1:
        tr.long_tp_sl

    elif bollinger == 0:
        tr.Short_tp_sl