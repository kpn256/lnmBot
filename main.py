'''el main es desde donde se ejecutará el código, todo lo que esté despues del if
 es lo que se ejecutara, de esta manera podemos hacer un codigo modular con varios analisis 
 y estrategias y lograr que sea escalable y mantenible
 '''

from lnm_class import Trading
import bot 


if __name__=="__main__":
   bot.rsi_strategy()
