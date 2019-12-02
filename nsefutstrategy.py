#!/usr/bin/env python3
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import sys
import calendar
import requests
from nsetools import Nse
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
from pprint import pprint


nse=Nse()
totalprofit=0
# Stock options (Similarly for index options, set index = True)


def get_symbol_futures_price(sym, month_val ):
    today=date(datetime.now().year,datetime.now().month,datetime.now().day)
    day1=datetime(datetime.now().year,datetime.now().month,1) - timedelta(days=1)
    day1=get_expiry_date(datetime.now().year,day1.month)

    year_val = datetime.now().year
    if month_val == 13 :
        month_val = 1
        year_val += 1
    
    stock_fut = get_history(symbol=sym,
                        start=day1,
                        end=today,
                        futures=True,
                        expiry_date=get_expiry_date(year_val,month_val))
    
    return float(stock_fut['Last'][-1])

def get_list_of_futures_price_for_next_months(symbol):

    global totalprofit 

    if not nse.is_valid_code(symbol):
         print ("Error : " + symbol + "is not valid")
         sys.exit(-1)

    month={1:"JAN", 2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"};
    
    lot_size = nse.get_fno_lot_sizes(cached=False)[symbol]
        
    #if lot_size < 1000 or lot_size > 10000:
    #    return
    
    day_val = get_expiry_date(datetime.now().year,datetime.now().month )
    val = get_symbol_futures_price(symbol, datetime.now().month)

    val_next_month = get_symbol_futures_price(symbol, datetime.now().month + 1 )
    
    spot_price = nse.get_quote(symbol)['lastPrice']
    #pprint(nse.get_quote(symbol))
    
    diff_with_spot_price_curr_month = spot_price - val
    if diff_with_spot_price_curr_month < 0:
        diff_with_spot_price_curr_month = val - spot_price
    
    diff_with_spot_price_next_month = spot_price - val_next_month
    if diff_with_spot_price_next_month < 0:
        diff_with_spot_price_next_month = val_next_month - spot_price
    

    diff = val - val_next_month
    
    if diff < 0:
        diff = val_next_month - val
    
    expectedprofit = diff * lot_size 
    
    totalprofit += int(expectedprofit)
    print("Symbol : "+symbol + "   Lot Size : " + str(lot_size))
    print("===================")
    print("Stock Price : "+str(spot_price))
    print(month[datetime.now().month] + " Fut Price : " + str(val))
    print(month[(datetime.now() + relativedelta(months=+1)).month] + " Fut Price : " + str(val_next_month))
    print("Expected Profit: " + str(expectedprofit))
    print("********************")


if len(sys.argv) > 1 :
  get_list_of_futures_price_for_next_months(sys.argv[1])
else:
  print ("Please pass argument of scrip to search")

print("Total profit : " + str(totalprofit))

sys.exit()
