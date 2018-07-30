# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 03:04:28 2016


# An Experimental module which generates simulated values of the stock
# May come in handy to price any derivative if required

"""

import numpy as np
import math
import matplotlib.pyplot as plt
import time


######  STANDARD PARAMS   ######

start_time = time.time()
stepsPerYear = 250
timeStep = 1/float(stepsPerYear)
nbDays = 250


######  MC PARAMS ##############

nbIter = 100

########  EQUITY PARAMS - To be taken from Equity module later on

stockInit = 100.0
mean = 0.2
vol = 0.3

#################################



## GBM is sum of drift and diffusion. Written seperately to model drift/diffusion later on
def gbmDrift(timeStep,mean):
    return timeStep * mean


def gbmDiffusion(timeStep,vol):
    return vol * np.random.normal(loc=0.0, scale= math.sqrt(timeStep))

def gbm(stockInit,timeStep,mean,vol):    
    myarr=[stockInit]
    stockFinal = 0.0
    for x in range(nbDays):
        stockFinal = stockInit * (1+gbmDrift(timeStep,mean)+gbmDiffusion(timeStep,mean))
        myarr.append(stockFinal)
        stockInit = stockFinal    
    plt.plot(myarr)
    return stockFinal

resultArray = []
for x in range(nbIter):
    res = gbm(stockInit,timeStep,mean,vol)
    resultArray.append(res)
print (np.average(resultArray))
print (time.time()-start_time)