from pinance import Pinance
import pandas as pd


stock1='HDFC'
stock2='HDFC.NS'

first = Pinance(stock1)
second = Pinance(stock2)

first.get_quotes()
second.get_quotes()

second.get_news()

df1 = pd.DataFrame(data=first.quotes_data,index=[0])
df2 = pd.DataFrame(data=second.quotes_data,index=[0])
df1=(df1.T)
df2=(df2.T)
df1.to_excel("DataQuality\hdfc.xls")
df2.to_excel("DataQuality\hdfcNS.xls")

df3 = pd.DataFrame(data=second.news_data,index=[0])
df3=(df3.T)

df3.to_excel(r"DataQuality\news.xls")
