#!/usr/bin/env python3
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import sys
import calendar
import requests
#from nsetools import Nse
#from nsepy import get_history
#from nsepy.derivatives import get_expiry_date
from nsepython import *
from pprint import pprint


#nse=Nse()
totalprofit=0
# Stock options (Similarly for index options, set index = True)

def get_expiry_date(symb):
    payload=nse_optionchain_scrapper(symb)
    currentExpiry,dte=nse_expirydetails(payload,1)
    return currentExpiry

def get_symbol_futures_price(sym, month_val ):
    today=date(datetime.now().year,datetime.now().month,datetime.now().day)
    day1=datetime(datetime.now().year,datetime.now().month,1) - timedelta(days=1)
    day1=get_expiry_date(datetime.now().year,day1.month)

    year_val = datetime.now().year
    if month_val == 13 :
        month_val = 1
        year_val += 1
    
    """stock_fut = get_history(symbol=sym,
                        start=day1,
                        end=today,
                        futures=True,
                        expiry_date=get_expiry_date(year_val,month_val))
    """
    stock_fut = nse_quote_ltp(sym,"latest","Fut")
    return float(stock_fut)

def get_list_of_futures_price_for_next_months(symbol):

    global totalprofit 

    lot_size = int(nse_get_fno_lot_sizes(symbol))
    val = float(nse_quote_ltp(symbol,"latest","Fut"))

    val_next_month = float(nse_quote_ltp(symbol,"next","Fut"))
    
    spot_price = float(nsetools_get_quote(symbol)['lastPrice'])
    
    diff_with_spot_price_curr_month = val - spot_price 
    diff_with_spot_price_next_month = val_next_month - spot_price
    
    expectedprofit_curr = round(diff_with_spot_price_curr_month * lot_size ,2)
    expectedprofit_next = round(diff_with_spot_price_next_month * lot_size ,2)
   
    '''
    print("Symbol : "+symbol + "   Lot Size : " + str(lot_size))
    print("===================")
    print("Stock Price : "+str(spot_price))
    print( "Current Month Fut Price : " + str(val))
    print("Next Month Fut Price : " + str(val_next_month))
    print("Expected Profit: " + str(expectedprofit_curr))
    print("Expected ProfitNext : " + str(expectedprofit_next))
    print("********************")
    '''
    print(f"{symbol},{spot_price},{lot_size},{val},{val_next_month},{expectedprofit_curr},{expectedprofit_next}",flush=True)

exception_list = ['NIFTY','NIFTYIT','BANKNIFTY','FINNIFTY','MIDCPNIFTY']
fno_full_list = ['NIFTY', 'NIFTYIT', 'BANKNIFTY', 'AUBANK', 'INDIAMART', 'APOLLOHOSP', 'DEEPAKNTR', 'CUB', 'ESCORTS', 'EICHERMOT', 'DIXON', 'COFORGE', 'HDFCAMC', 'ALKEM', 'MFSL', 'ATUL', 'POWERGRID', 'ICICIPRULI', 'GNFC', 'HDFCLIFE', 'METROPOLIS', 'SBICARD', 'AUROPHARMA', 'BAJAJFINSV', 'TATACOMM', 'ONGC', 'HINDUNILVR', 'JUBLFOOD', 'WHIRLPOOL', 'NESTLEIND', 'TORNTPHARM', 'CHAMBLFERT', 'PNB', 'RAIN', 'CANBK', 'SIEMENS', 'MCX', 'AARTIIND', 'SBILIFE', 'DALBHARAT', 'RELIANCE', 'PETRONET', 'ASTRAL', 'MGL', 'CHOLAFIN', 'GODREJCP', 'ABB', 'MARUTI', 'BAJFINANCE', 'GMRINFRA', 'IDFCFIRSTB', 'BEL', 'VEDL', 'SRF', 'SBIN', 'PIDILITIND', 'IEX', 'ASIANPAINT', 'M&MFIN', 'COROMANDEL', 'ITC', 'HAVELLS', 'POLYCAB', 'ICICIBANK', 'TATACONSUM', 'IRCTC', 'AXISBANK', 'TVSMOTOR', 'COALINDIA', 'IDFC', 'UBL', 'HDFCBANK', 'ULTRACEMCO', 'FEDERALBNK', 'TRENT', 'HDFC', 'TITAN', 'TATACHEM', 'VOLTAS', 'ABFRL', 'BATAINDIA', 'GAIL', 'DELTACORP', 'SHREECEM', 'ASHOKLEY', 'OBEROIRLTY', 'DLF', 'UPL', 'HINDALCO', 'TATAMOTORS', 'JSWSTEEL', 'ICICIGI', 'HAL', 'BERGEPAINT', 'BAJAJ-AUTO', 'NAVINFLUOR', 'BHEL', 'MRF', 'CONCOR', 'BRITANNIA', 'HINDCOPPER', 'PVR', 'M&M', 'PAGEIND', 'INDIGO', 'BOSCHLTD', 'BANKBARODA', 'PEL', 'COLPAL', 'GLENMARK', 'MARICO', 'ACC', 'ABCAPITAL', 'SHRIRAMFIN', 'GODREJPROP', 'JINDALSTEL', 'RBLBANK', 'ZYDUSLIFE', 'BALKRISIND', 'MUTHOOTFIN', 'INDHOTEL', 'CIPLA', 'RAMCOCEM', 'MCDOWELL-N', 'MOTHERSON', 'OFSS', 'HONAUT', 'BHARTIARTL', 'IBULHSGFIN', 'MANAPPURAM', 'INTELLECT', 'GUJGASLTD', 'JKCEMENT', 'NAUKRI', 'ADANIPORTS', 'SAIL', 'PIIND', 'APOLLOTYRE', 'INDUSTOWER', 'TATASTEEL', 'KOTAKBANK', 'NTPC', 'BIOCON', 'LTTS', 'NATIONALUM', 'ABBOTINDIA', 'GRASIM', 'SUNPHARMA', 'LICHSGFIN', 'ZEEL', 'TATAPOWER', 'L&TFH', 'IGL', 'ADANIENT', 'HEROMOTOCO', 'DABUR', 'LT', 'CANFINHOME', 'IOC', 'LALPATHLAB', 'DRREDDY', 'BHARATFORG', 'CUMMINSIND', 'RECLTD', 'IPCALAB', 'NMDC', 'BPCL', 'EXIDEIND', 'BALRAMCHIN', 'INDIACEM', 'AMBUJACEM', 'CROMPTON', 'SUNTV', 'LUPIN', 'IDEA', 'BSOFT', 'WIPRO', 'DIVISLAB', 'MPHASIS', 'LAURUSLABS', 'SYNGENE', 'GRANULES', 'BANDHANBNK', 'INDUSINDBK', 'TECHM', 'TCS', 'INFY', 'HCLTECH', 'PFC', 'HINDPETRO', 'PERSISTENT', 'LTIM']
for item in fno_full_list:
    try:  
        if not item in exception_list:
           get_list_of_futures_price_for_next_months(item)
    except:
        print(f"{item},,,,,,",flush=True)
        continue

sys.exit()
