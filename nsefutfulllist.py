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
# Stock options (Similarly for index options, set index = True)


def get_symbol_futures_price(sym, month_val ):
    today=date(datetime.now().year,datetime.now().month,datetime.now().day)
    day1=date(datetime.now().year,datetime.now().month,1)

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

    if not nse.is_valid_code(symbol):
         print ("Error : " + symbol + "is not valid")
         sys.exit(-1)

    month={1:"JAN", 2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"};
    
    lot_size = nse.get_fno_lot_sizes(cached=False)[symbol]
        
    #if lot_size < 1000 or lot_size > 10000:
    #    return
    
    day_val = get_expiry_date(datetime.now().year,datetime.now().month)
    val = get_symbol_futures_price(symbol, datetime.now().month)

    val_next_month = get_symbol_futures_price(symbol, datetime.now().month + 1)
    
    spot_price = nse.get_quote(symbol)['closePrice']
    
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
    
    if expectedprofit < 5000 : 
        return 

    print("Symbol : "+symbol + "   Lot Size : " + str(lot_size))
    print("===================")
    print("Stock Price : "+str(spot_price))
    print(month[datetime.now().month] + " Fut Price : " + str(val))
    print(month[datetime.now().month + 1] + " Fut Price : " + str(val_next_month))
    print("Expected Profit: " + str(expectedprofit))
    print("********************")



fno_list = ['ACC', 'ADANIENT', 'ADANIPORTS', 'ADANIPOWER', 'AMARAJABAT', 'AMBUJACEM', 'APOLLOHOSP', 'APOLLOTYRE',
'ASHOKLEY', 'ASIANPAINT', 'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BALKRISIND',
'BANKBARODA', 'BANKINDIA', 'BATAINDIA', 'BERGEPAINT', 'BEL', 'BHARATFORG', 'BPCL', 'BHARTIARTL', 'INFRATEL', 'BHEL', 'BIOCON', 'BOSCHLTD', 'BRITANNIA', 'CADILAHC', 'CANBK', 'CASTROLIND', 'CENTURYTEX', 'CESC', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COLPAL', 'CONCOR', 'CUMMINSIND', 'DABUR', 'DISHTV', 'DIVISLAB', 'DLF', 'DRREDDY', 'EICHERMOT', 'EQUITAS', 'ESCORTS', 'EXIDEIND', 'FEDERALBNK', 'GAIL', 'GLENMARK', 'GMRINFRA', 'GODREJCP', 'GRASIM', 'HAVELLS', 'HCLTECH', 'HDFCBANK', 'HDFC', 'HEROMOTOCO', 'HEXAWARE', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'ICICIBANK', 'ICICIPRULI', 'IDEA', 'IDFCFIRSTB', 'IBULHSGFIN', 'IOC', 'IGL', 'INDUSINDBK', 'INFY', 'INDIGO', 'ITC', 'JINDALSTEL', 'JSWSTEEL', 'JUBLFOOD', 'JUSTDIAL', 'KOTAKBANK', 'L&TFH', 'LT', 'LICHSGFIN', 'LUPIN', 'M&MFIN', 'MGL', 'M&M', 'MANAPPURAM', 'MARICO', 'MARUTI', 'MFSL', 'MINDTREE', 'MOTHERSUMI', 'MRF', 'MUTHOOTFIN', 'NATIONALUM', 'NBCC', 'NCC', 'NESTLEIND', 'NIITTECH', 'NMDC', 'NTPC', 'ONGC', 'OIL', 'PAGEIND', 'PETRONET', 'PIDILITIND', 'PEL', 'PFC', 'POWERGRID', 'PNB', 'PVR', 'RBLBANK', 'RELIANCE', 'RECLTD', 'SHREECEM', 'SRTRANSFIN', 'SIEMENS', 'SRF', 'SBIN', 'SAIL', 'SUNPHARMA', 'SUNTV', 'TATACHEM', 'TCS', 'TATAELXSI', 'TATAGLOBAL', 'TATAMTRDVR', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TECHM', 'RAMCOCEM', 'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TVSMOTOR', 'UJJIVAN', 'ULTRACEMCO', 'UNIONBANK', 'UBL', 'MCDOWELL-N', 'UPL', 'VEDL', 'VOLTAS', 'WIPRO', 'YESBANK', 'ZEEL' ]
for symbol in fno_list:
    try:
        get_list_of_futures_price_for_next_months(symbol)
        #sleep(randint(1,15))
    except:
        print("Oops Couldnt get complete details. Please try after sometimei. Completed till " + symbol)
        break



sys.exit()
