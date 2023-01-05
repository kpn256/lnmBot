
import lnm_class as tr
import time
from tradingview_ta import TA_Handler, Interval
from constants import options

# create a object for use lnm_class

user = tr.Trading(**options)

#create objet for use tradingview_ta

bitcoin = TA_Handler(
    symbol="XBTUSD",
    screener="crypto",
    exchange="BITMEX",
    interval=Interval.INTERVAL_1_MINUTE,
    )
   

def stoploss_manager(bid, offer):

# this funtion check our positions stop loss and update stoploss

    data = user.show_running_p()
    running_positions = []

    for items in data:
        
        sort_dict = {
            'pid': items['pid'],
            'side': items['side'],
            'liquidation': items['liquidation'],
            'stoploss': items['stoploss'],
            'price': items['price'],
            'pl': items['pl']
            }

        running_positions.append(sort_dict)
        del sort_dict

        if (items['side'] == 'b') and (items['pl'] > (items['margin']/2)):

            change = items['stoploss'] + (items['price'] - items['liquidation'])
            new_sl = bid + change
            user.futures_update_position({
                'pid': items['pid'],
                'type': 'stoploss',
                'value': new_sl
                })
            print(f"stoploss was change new sl is {new_sl} in {items['pid']} position")


        elif(items['side'] == "s") and (items['pl'] > (items['margin']/2)):

            change = items['stoploss'] + (items['price'] - items['liquidation'])
            new_sl = offer + change
            user.futures_update_position({
                'pid': items['pid'],
                'type': 'stoploss',
                'value': new_sl
                })
            print("stoploss was change")

    return running_positions

def recomendations():

    # this funtion compare ema20 and ema50 recomendation and return a solid recomendation

    analysis = bitcoin.get_analysis()
    recomendation = analysis.moving_averages['COMPUTE']
    ema20_recom = recomendation['EMA20']
    ema50_recom = recomendation['EMA50']

    if ema20_recom == 'SELL' and ema50_recom == 'SELL':
        return 'SELL'

    elif ema20_recom == 'BUY' and ema50_recom == 'BUY':
        return 'BUY'

    else:
        return 'NEUTRAL'


def rsi_strategy():

# this funtion analize rsi and bollinger bands and open positions

    while True:

        analysis = bitcoin.get_analysis()
        rsi = round(analysis.indicators["RSI"], 2)
        bollinger_upper = round(analysis.indicators["BB.upper"], 2)
        bollinger_lower = round(analysis.indicators["BB.lower"], 2)
        ema20 = round(analysis.indicators["EMA20"], 2)
        index = user.price_index()
        bid = user.price_bid()
        offer = user.price_offer()

        print(f"rsi: {rsi}")
        print(f"BB.lower: {bollinger_lower}")
        print(f"BB.upper: {bollinger_upper}")
        print(f"ema20: {ema20}")
        print(f"index: {index}")
        print(f"bid: {bid}")
        print(f"offer: {offer}")
        print(analysis.time)
        print(recomendations()) 


        if (rsi >= 70) and (index >= ema20) and (offer >= bollinger_upper) and (recomendations() == 'SELL'):
            
            offer_change_tp = 0.02*offer
            offer_change_sl = 0.005*offer
            short_tp = offer - offer_change_tp
            short_sl = offer + offer_change_sl

            print(user.Short_tp_sl(margin=100, leverage=100, type="m", tp=short_tp, sl=short_sl))
            print("short is running")

            time.sleep(900)

        elif (rsi <= 30) and (index <= ema20) and (bid <= bollinger_lower) and (recomendations() == 'BUY'):
 
            bid_change_tp = 0.03*bid
            bid_change_sl = 0.007*bid
            long_tp = offer + bid_change_tp
            long_sl = offer - bid_change_sl

            print(user.long_tp_sl(type="m", margin=100, leverage=60, tp=long_tp, sl=long_sl))
            print("long is running")

            time.sleep(900)

        
        print(stoploss_manager(bid, offer))
        time.sleep(120)
