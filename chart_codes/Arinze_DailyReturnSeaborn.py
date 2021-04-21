# Created by Arinze David Nwanna

import seaborn as sns
from datetime import datetime
import pandas_datareader.data as pdr

#Outline a list of tech stocks
tech_list = ['AAPL','GOOG','MSFT','AMZN','YHOO']

#Time fram - Start date set to 1 year back
end = datetime.now()
start = datetime(end.year-1,end.month,end.day)

#Call data from API or database
for stock in tech_list:
    globals()[stock] = pdr.DataReader(stock,'yahoo',start,end) #The globals method sets

#Calculate daily return formula
AAPL['Daily Return'] = AAPL['Adj Close'].pct_change()
dRA = AAPL['Daily Return'].plot(figsize=(14,5),legend=True,linestyle='--',marker='o')

#format figure
dRA.set_title('Daily Return of AAPL over 1 year')
dRA.set_ylabel('%Change')
dRA.grid()
fig = dRA.get_figure()

#Daily Returns Density plot
dR = sns.distplot(AAPL['Daily Return'].dropna(),bins=100,color='red')
dR.grid()
dR.set_title('Daily Return density distribution of AAPL over 1 year')
fig1 = dR.get_figure()

#Caluculate a daily returns dataframe 
close_df = pdr.DataReader(tech_list,'yahoo',start,end)['Adj Close']
close_df.tail()
rets_df = close_df.pct_change()

#Joint plot for Google and AAPL
figG = sns.jointplot('GOOG','AAPL',rets_df,kind='hex')
figG.fig.suptitle('Correlation between Daily returns of Google and AAPL ',x=0.5 ,y= 1.01)

#Savefigures
fig.savefig('DailyReturns.png')
fig1.savefig('DailyReturns1.png')
figG.savefig('DailyReturnsandCorelation.png')
