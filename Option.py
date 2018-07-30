'''

Option Pricing module

Takes Equity prices and prices vanilla options using BS
Along with price - Gives out basic greeks and implied vol values

'''
from datetime import datetime
start = datetime.now()
import numpy as np
import scipy as sp
import scipy.stats
import math
import pandas as pd
import pandas_datareader.data  as web

import nsepy as nse

#nse.get_history("^NSEI",datetime(2016,2,1) , datetime(2016,2,5))
#
#stock_opt = nse.get_history(symbol="NIFTY",
#                        start=datetime(2016,2,12), 
#                        end=datetime(2016,2,15),
#                        option_type="CE",
#                        strike_price=5500,
#                        index=True,
#                        expiry_date=datetime(2016,2,25))
#                        

#print stock_opt
#print web.DataReader("^NSEI","yahoo", datetime(2016,1,1),datetime(2016,2,2))
#x= web.Options("aapl","yahoo")
#data = aapl.get_call_data(expiry=aapl.expiry_dates[0])

#print dir(x)


#using s as self
class Option:
#    print "first line inside class"
    def __init__(s,type,S,K,t,r,vol):
#        print "class init"
        s.type = type
        s.S = S
        s.K = K
        s.r = r
        s.t = t
        s.vol = vol
        s.type = type
        if s.type not in ("c","p"):
            raise Exception("Option type should be 'c' or 'p'")
        s.d1 = ( math.log(s.S / s.K) + (s.r + s.vol**2 *0.5)*s.t )/(s.vol * math.sqrt(s.t))
        s.d2 = s.d1 - s.vol * math.sqrt(s.t)


# Option vol parameter for implied vol calculation
    def priceBS(s, vol = None ):
        if vol:
            s.vol = vol
            s.d1 = ( math.log(s.S / s.K) + (s.r + s.vol**2 *0.5)*s.t )/(s.vol * math.sqrt(s.t))
            s.d2 = s.d1 - s.vol * math.sqrt(s.t)
        perf = s.Nd1() * s.S - s.Nd2() * s.K * math.exp(-s.r*s.t)
        if s.type is "c":
            return perf
        else:
            return s.K * math.exp(-s.r*s.t) - s.S + perf

    def Nd1(s):
        return sp.stats.norm.cdf(s.d1)

    def Nd2(s):
        return sp.stats.norm.cdf(s.d2)

    def delta(s):
        if s.type is "c":
            return s.Nd1()
        else:
            return s.Nd1() -1.0

    def gamma(s):
        return normDist(s.d1) / ( s.S * s.vol * math.sqrt(s.t))
    
# Vega calculated in Vol point terms
    def vega(s):
        return s.S * normDist(s.d1) * math.sqrt(s.t) / 100.0

# Theta output is per DAY
    def theta(s):
        fact1 =   s.S * normDist(s.d1) * s.vol / ( 2.0 * math.sqrt(s.t))
        fact2 =  s.r * s.K * math.exp(-s.r * s.t) * s.Nd2()
        if s.type is "c":
            return  (-fact1 -s.r * s.K * math.exp(-s.r * s.t) * s.Nd2())/365.0
        else:
            return (-fact1 + s.r * s.K * math.exp(-s.r * s.t) * (1-s.Nd2()))/365.0

    def rho(s):
        if s.type is "c":
            return s.K * s.t * math.exp( - s.r * s.t) * s.Nd2()
        else:
            return -s.K * s.t * math.exp(-s.r*s.t) * (1.0 - s.Nd2()) 

#Display stats
    def stats(s):
        print ("Option type : %d "%("Call" if s.type == "c" else "Put"))
        print ("Option Price : " , s.priceBS())
        print ("Delta : ", s.delta())
        print ("Gamma : ", s.gamma())
        print ("Vega : ", s.vega())
        print ("Theta : ", s.theta())
    
# Using Newton-Ralphson method for convergence        
    def impliedVol(s, marketPrice):
        trial = 1000
        accuracy = 1.0e-6
        t_sqrt = math.sqrt(s.t)

        s.vol = (marketPrice / s.S) / ( t_sqrt * 1 / math.sqrt(2*math.pi))
        test2 = s.vol
        for i in range(trial):
            
            price = s.priceBS(test2)
            diff = marketPrice - price
            if abs(diff) < accuracy:
                return s.vol
            vega = s.S * t_sqrt * s.Nd1()
            s.vol = s.vol + diff / vega
            test2 = s.vol
        raise Exception("Failed to converge at %d iteration"%(i))
    

#print "first line outside class"
def normDist(x):
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5*x*x)
    

myOption = Option("c",6980.95,6950.0,0.0361111,0.1,0.2005)

myOption.stats()

print (myOption.impliedVol(122.0))
print ("Ending at ")
x = datetime.now()-start

print (x.total_seconds())



