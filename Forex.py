from forex_python.converter import CurrencyRates
import datetime
import pandas as pd
import matplotlib.pyplot as plt

c = CurrencyRates()

usDollar = 'USD'
canadianDollar = 'CAD'
indianRupee = 'INR'
euro = 'EUR'
britishPound = 'GBP'
japaneseYen = 'JPY'
swissFranc = 'CHF'
australianDollar = 'AUD'


start = datetime.date.today()-datetime.timedelta(weeks=48)
end = datetime.date.today()

datetimeList = pd.date_range(start,end).to_pydatetime().tolist()
dateList = []
valueList=[]

for item in datetimeList:
    dateList.append(item.date())
    valueList.append(c.get_rate(usDollar,euro,item))

fxdf = pd.DataFrame({'Date':dateList,'Value':valueList})

fxdf['MA5'] = fxdf['Value'].rolling(window=5).mean()
fxdf['MA10'] = fxdf['Value'].rolling(window=10).mean()
fxdf['MA20'] = fxdf['Value'].rolling(window=20).mean()

#fxdf.to_excel('USDINR.xls')

#plt.show()

fxdf.plot(x='Date',grid=True)
plt.show()
print('a')


