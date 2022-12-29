
from curses.ascii import isdigit
import json
from lnmarkets import rest



class User(rest.LNMarketsRest):

    def __init__(self, key, secret, passphrase):
        super().app_configuration

        self.key = key
        self.secret = secret
        self.passphrase = passphrase

        self.options = {
                'key': f'{self.key}',
                'secret': f'{self.secret}',
                'passphrase': f'{self.passphrase}'
                }

        self.status = False

        self.lnm = rest.LNMarketsRest(**self.options)
        self.lnm.futures_get_ticker()

    def login(self):

        self.status = True

    def logout(self):
        if self.status:
            self.status = False
        else:
            "go to login"

    def show_status(self):
        if self.status:
            return "user online"
        else:
            return "user offline"


class Trading(User):

    def __init__(self, key, secret, passphrase):
        super().__init__(key, secret, passphrase)

        self.margin = 500
        self.leverage = 50
        self.entryPrice = ""

    def long(self, type, margin, leverage):
        peticion = self.lnm.futures_new_position({
            'type': type,
            'side': 'b',
            'margin': margin,
            'leverage': leverage,
            })
        return self.response(peticion)

    def long_tp_sl(self, type, margin, leverage, sl, tp):
        peticion = self.lnm.futures_new_position({
            'type': type,
            'side': 'b',
            'margin': margin,
            'leverage': leverage,
            'stoploss': int(sl),
            'takeprofit': int(tp),
        })
        self.response(peticion)

    def long_sl(self, type, margin, leverage, sl):

        peticion = self.lnm.futures_new_position({
            'type': type,
            'side': 'b',
            'margin': margin,
            'leverage': leverage,
            'stoploss': int(sl),
        })
        self.response(peticion)

    def long_tp(self, type, margin, leverage, tp):

        peticion = self.lnm.futures_new_position({
            'type': type,
            'side': 'b',
            'margin': margin,
            'leverage': leverage,
            'takeprofit': int(tp),
        })
        self.response(peticion)

    def Short(self, type, margin, leverage):
        
        peticion = self.lnm.futures_new_position({
                'type': type,
                'side': 's',
                'margin': margin,
                'leverage': leverage,
                })
        return self.response(peticion)

    def Short_tp_sl(self, type, margin, leverage, sl, tp):
        peticion = self.lnm.futures_new_position({
            'type': type,
            'side': 's',
            'margin': int(margin),
            'leverage': int(leverage),
            'stoploss': int(sl),
            'takeprofit': int(tp),
            })
        return peticion

    def close_run_p(self, pid ):
    
        close = self.lnm.futures_close_position({
            'pid': pid,
            })
        peticion = json.loads(close)
        response = []
        for items in peticion.items():
            response.append(items)
            
            
        return response
        
    def close_limit_P(self, pid):
        
        cancel_p = self.lnm.futures_cancel_position({
            'pid': pid,
        })()
        peticion = json.loads(cancel_p)
        response = []
        for items in peticion.items():
            response.append(items)
        return response

    def close_all(self):
        closeP = self.lnm.futures_close_all_positions()
        return closeP

    def show_open_p(self):

        open_p = self.lnm.futures_get_positions({
                'type': 'open'
                })
        info_open = json.loads(open_p)
        result = []
        counter = 0
        for i in info_open:
            position = []
            counter += 1
            position.append(f"posicion {counter}")
            position.append(f"pid: {i['pid']}")
            position.append(f"price: {i['price']}")
            position.append(f"margin: {i['margin']}")
            position.append(f"liquidation: {i['liquidation']}")
            result.append(position)
            del position

        string = str(result)
        characters = "[]',"
        for x in range(len(characters)):
            string = string.replace(characters[x], "")
        return 

    def show_running_p(self):
        running_p = self.lnm.futures_get_positions({
                'type': 'running'
                })
        info_running = json.loads(running_p)
        '''result = []
        counter = 0
        for i in info_running:
            position = []
            counter += 1
            position.append(f"posicion {counter}")
            position.append(f"pid: {i['pid']}")
            position.append(f"price: {i['price']}")
            position.append(f"margin: {i['margin']}")
            position.append(f"liquidation: {i['liquidation']}")
            result.append(position)
            del position

        string = str(result)
        characters = "[]'"
        for x in range(len(characters)):
            string = string.replace(characters[x], "")'''

        return info_running

    def response(self, peticion):
        # crear un try exept por si la peticion falla PENDIENTE
        info = json.loads(peticion)
        position_info = info["position"]
        pid = position_info["pid"]
        liquidation = position_info["liquidation"]
        price = position_info["price"]
        leverage = position_info["leverage"]
        take_p = position_info['takeprofit']
        stop_l = position_info['stoploss']
        p_info = (
                f"position ID: {pid}\n"
                f"pid: {pid}\n"
                f"liquidation: {liquidation}\n"
                f"entry price: {price}\n"
                f"stoploss: {stop_l}\n"
                f"takeprofit: {take_p}"
                f"leverage: {leverage}")
        return info

    def price_index(self):

        index_price = self.lnm.futures_index_history({
            'limit': 2
        })
        price_requests = json.loads(index_price)
        price_index1 = price_requests[1]
        index = price_index1["index"]
        
        return index
    
    def price_bid(self):

        bid_price = self.lnm.futures_bid_offer_history({
            'limit': 2
            })

        bidOffer = json.loads(bid_price)
        bid_offer1 = bidOffer[1]
        bid = bid_offer1["bid"]
        offer = bid_offer1["offer"]
        return bid 

    def price_offer(self):

        bid_price = self.lnm.futures_bid_offer_history({
            'limit': 2
            })

        bidOffer = json.loads(bid_price)
        bid_offer1 = bidOffer[1]
        offer = bid_offer1["offer"]
        return  offer
        



