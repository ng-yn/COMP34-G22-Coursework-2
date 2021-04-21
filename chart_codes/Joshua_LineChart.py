# Created by Joshua Ng
# This code is for the 30 day moving average for the NVDA stock using matplotlib

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Importing data set
connection = sqlite3.connect('../my_app/data/FinancialDatabase.db')
sql_query = pd.read_sql_query('SELECT timestamp, close FROM NVDA', connection)
df = pd.DataFrame(sql_query, columns=['timestamp', 'close'])

# Creating a dataframe for the dates
df2 = df.loc[:,['timestamp']]
df2 = df2.iloc[::-1] #reverse the data frame
df2['timestamp'] = pd.to_datetime(df2['timestamp'])

# Creating dataframe for 30 day moving average (closing price)
df3 = df.loc[:,['close']]
df3 = df3.iloc[::-1]
df3['MA'] = df3.rolling(window=30).mean()

close = pd.concat([df2,df3], axis=1)
#close = close.dropna() # Removing N/A values

# Creating Line Graph
plt.plot(df2, df3['close'],
         label='Close Price',
         color='red')
plt.plot(df2, df3['MA'],
         label = '30 Day Moving Average',
         color='blue')
plt.ylim(ymin=0)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('Closing price of NVDA stock')

plt.show()




