#!/usr/bin/env python3
from datetime import date
from datetime import datetime
from dateutil.relativedelta import *
import sys
import calendar
import requests
from nsetools import Nse
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
from random import randint
from time import sleep


nse=Nse()

fo_stocks_dict = nse.get_fno_lot_sizes(cached=False)
fo_stocks_list = fo_stocks_dict.keys()

for x in fo_stocks_list:
    try:  
      currentprice = nse.get_quote(x)['lastPrice']
    except IndexError:
      currentprice = 0
    value = fo_stocks_dict[x] * currentprice 
    tickvalue = fo_stocks_dict[x] * .05
    #print ( "Stock :  {}, Lot : {}, Value: {} \n".format( x , str(fo_stocks_dict[x]) , str(round(value,2) ))
    print ( "{}, {}, {}, {}, {}".format( x , str(currentprice), str(fo_stocks_dict[x]) , str(round (value,2)),str(tickvalue) ))
