
import lnm_class as tr  # acá traemos la clase Trading del modulo lnm_class
import time
import tradingview_ta 
from tradingview_ta import TA_Handler, Interval, Exchange



def bot():


    bitcoin = TA_Handler(
    symbol="XBTUSD",
    screener="crypto",
    exchange="BITMEX",
    interval=Interval.INTERVAL_1_MINUTE,
    )

    # en esta line estoy creando el objeto user con todos los metodos de la clase Trading del lnm_class
    # los parametros que necesita esta clase para funcionar es la apikey
    # esta clase tambien nos permite utilizar los metodos directamente de lnm Api

    user = tr.Trading(
        key="",
        secret="", 
        passphrase="")

    # de la misma manera creamos el objeto analysis que tiene los metodos de tradingview_ta
    analysis = bitcoin.get_analysis()
    
    while True: #creamos un bucle para que cada x tiempo pida los datos y revise si se cumplen las condiciones


        # de esta manera obtenemos los datos que queremos de tradingview_ta, estos estan alojados en un diccionario 

        rsi = analysis.indicators["RSI"]
    
        bollinger_upper = analysis.indicators["BB.upper"]

        bollinger_lower = analysis.indicators["BB.lower"]

        ema20 = analysis.indicators["EMA20"]

        # aca obtenemos el precio de lnm


        index = user.price_index()

        bid = user.price_bid()

        offer = user.price_offer()

        


        # hago el print para verificar que me entrega los datos que quiero

        print(f"rsi: {rsi}")
        print(f"BB.lower: {bollinger_lower}")
        print(f"BB.upper: {bollinger_upper}")
        print(f"ema20: {ema20}")
        print(f"index: {index}")
        print(f"bid: {bid}")
        print(f"offer: {offer}")
        
        # print(f"tp: {tp}")
        # print(f"sl: {sl}\n")
        

        # aca ya empezariamos a montar la estrategia segun los datos que obtenemos 

        if (rsi >= 70) and (offer >= ema20) or (index >= bollinger_upper):

            # declarando estas variables calculo tp y sl ?¿

            offer_change_tp = 0.03*offer

            offer_change_sl = 0.007*offer

            short_tp = offer - offer_change_tp

            short_sl = offer + offer_change_sl

            user.Short_tp_sl(margin=100, leverage=100, type="m", tp=short_tp, sl=short_sl)

            print("short is running")

            time.sleep(900)

        elif (rsi <= 30) and (bid >= ema20) or (index <= bollinger_lower):

            bid_change_tp = 0.03*bid

            bid_change_sl = 0.007*bid

            long_tp = offer + bid_change_tp

            long_sl = offer - bid_change_sl

            user.long_tp_sl(type="m", margin=1000, leverage=100, tp=long_tp, sl=long_sl)

            time.sleep(900)

        time.sleep(120)
  
    