#!/usr/bin/env python3
import sys
from nsetools import Nse
from pprint import pprint
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
from datetime import date
from datetime import datetime

nse = Nse()

print ( nse )

#q = nse.get_quote('infy')
#pprint(q)

#lst = nse.get_index_list()

#pprint(lst)

if len(sys.argv) <= 1:
    print ("No arguments provided")
    sys.exit()
if nse.is_valid_code(sys.argv[1]):
    print ( sys.argv[1] + " is correct ")
else:
    sys.exit()
lotsize = nse.get_fno_lot_sizes(cached=False)[sys.argv[1]]

print (lotsize)

day=date(datetime.now().year,datetime.now().month,datetime.now().day)
pprint(day)

stock_fut = get_history(symbol=sys.argv[1], start=date(2019,10,11), end=date(2019,10,20),futures=True,expiry_date=get_expiry_date(2019,10))


pprint(stock_fut)

print(float (stock_fut['Last'][-1]))
