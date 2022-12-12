
import lnm_class as tr  
import time
import tradingview_ta 
from tradingview_ta import TA_Handler, Interval, Exchange




def bot():

    user = tr.Trading(key="",
        secret="",
        passphrase="")

    bitcoin = TA_Handler(
        symbol="XBTUSD",
        screener="crypto",
        exchange="BITMEX",
        interval=Interval.INTERVAL_1_MINUTE,
        )

    while True:

        analysis = bitcoin.get_analysis()

        rsi = analysis.indicators["RSI"]
    
        bollinger_upper = analysis.indicators["BB.upper"]

        bollinger_lower = analysis.indicators["BB.lower"]

        ema20 = analysis.indicators["EMA20"]

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
        
        # aca ya empezariamos a montar la estrategia segun los datos que obtenemos 

        if (rsi >= 70) and (bid >= ema20) and (index >= bollinger_upper):

            offer_change_tp = 0.02*offer

            offer_change_sl = 0.007*offer

            short_tp = offer - offer_change_tp

            short_sl = offer + offer_change_sl

            user.Short_tp_sl(margin=100, leverage=100, type="m", tp=short_tp, sl=short_sl)

            print("short is running")

            time.sleep(900)

        elif (rsi <= 30) and (offer <= ema20) and (index <= bollinger_lower):

            bid_change_tp = 0.03*bid

            bid_change_sl = 0.007*bid

            long_tp = offer + bid_change_tp

            long_sl = offer - bid_change_sl

            user.long_tp_sl(type="m", margin=100, leverage=100, tp=long_tp, sl=long_sl)
            print("long is running")

            time.sleep(900)

        data = user.show_running_p()
        running_positions = []
        
        for items in data:
            sort_dict = {
                    'pid': items['pid'],
                    'type': items['type'],
                    'liquidation': items['liquidation'],
                    'stoploss': items['stoploss'],
                    'price': items['price']
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
                

        print(running_positions)
        time.sleep(120)
        
    



