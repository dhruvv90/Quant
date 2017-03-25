# -*- coding: utf-8 -*-

"""
Created on Sat Mar 19 02:43:33 2016

@author: Verma


# Fetches data for equities from Yahoo finance
# Generates and plots series of returns and basic performance
# Generates basic technical analysis to demonstrate trends


"""

import matplotlib.pyplot as plt
from xlrd import open_workbook
import xlwt
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
from dateutil import parser
from datetime import datetime,timedelta
from yahoo_finance import Share
from pandas.io.data import DataReader as dr
import webbrowser as wb
#today = pd.datetime.date(today)
today = parser.parse("2016-3-18").date()

# yahoo_finance obsolete / non supportive for NSE , BSE



exchangeHols = ["26/01/2016","07/03/2016","24/03/2016","25/03/2016",
            "14/04/2016","15/04/2016","19/04/2016",
            "06/07/2016","15/08/2016","05/09/2016","13/09/2016",
            "11/10/2016","12/10/2016","31/10/2016","14/11/2016"]


#######
#
##   Note:-  All Dates passed in below functions are in datetime Format
##    and not String
#
####


#  Returns DataFrame on Ticker within specified dates
def fetchData(ticker,startDate,endDate):
    try:
        frame=dr(ticker,'yahoo',start = str(startDate), end = str(endDate))        
    except:
        raise Exception ("Unable to fetch ticker")        

    frame.index = frame.index.date
        
    frame.index.name = "Date"
    return frame

# Outdated function
## TO BE KEPT AS THIS CONTAINS SOME USEFUL SYNTAX


'''
def MA(frame,period,col='Adj Close',queryDate=today):
    if period > len(frame) :
        raise LookupError("Moving Average period must me less than number of rows in data frame")
    try:
        frame.ix[queryDate]
    except:
        raise LookupError("Current date not found in data")
    dateList=[]
    for key,values in frame.iterrows():
        dateList.append(key.to_datetime())
    queryDateIdx = dateList.index(queryDate)
    startDateIdx = queryDateIdx - period +1
    if startDateIdx < -1 :
        raise LookupError("MA period is beyond specified dates")
    maList = frame[col][startDateIdx:queryDateIdx+1]        
    return np.average(maList)
  
  '''
  

def MA(frame,period,col='Adj Close'):
    result =  pd.rolling_mean(frame[col],period)
    return result
    
def Returns(frame,period,col='Adj Close'):
    result = frame[col].pct_change(period)
    return result
    
    
def Analyze(ticker,start_date,end_date,period):
    security = ticker    
    
    if isinstance(security,basestring):    
        myFrame = fetchData(security,start_date,end_date)
            
        Price = myFrame['Adj Close']
        MAx = MA(myFrame,period)
        ret = Returns(myFrame,10)
                
        customFrame = pd.DataFrame({'Adj Close':Price , 'MA':MAx})

        try:
            customFrame.to_excel("test.xls","Sheet2")
        
            wb.open('test.xls')
        except:
            pass
        
        plt.subplot(211)
        plt.plot(customFrame)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price and MA')
        
        
        plt.subplot(212)
        plt.plot(ret)
        plt.axhline()
        returnFrame = pd.DataFrame({'Returns':ret})
        plt.plot(MA(returnFrame,200,col='Returns'))

    else:
        for tick in ticker:
            Analyze(tick,period)            

    
start_date = parser.parse("2013-3-20").date()
end_date = parser.parse("2016-4-13").date()    

list = ['hdfc.ns','JUSTDIAL.NS']

Analyze('hdfc.NS',start_date,end_date,200)
    