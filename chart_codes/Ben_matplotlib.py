# COMP0034 CW1 Group 22
# Code create by Yu-Hsiang Chen
# STN : 18035617

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

#connect to the database
conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')




def matplotlib(label,value):
    df = pd.read_sql_query("SELECT * from {}".format(label), conn)
    df_plot = df[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 200 days' data
    df_plot = df_plot.head(value)
    # using matplotlib to plot moving average convergence divergence (MACD)
    #calculate the exponential moving average (EMA) by using the exponential weight mean
    df_plot['EMA_12'] = df_plot['adjusted_close'].ewm(span=12,adjust=False).mean()
    df_plot['EMA_26'] = df_plot['adjusted_close'].ewm(span=26, adjust=False).mean()
    # set another column to calculate the EMA difference
    df_plot['DIF'] = df_plot['EMA_12'] - df_plot['EMA_26']
    # DEA is the signal line which is the 9 days EMA of the DIF
    df_plot['DEA'] = df_plot['DIF'].ewm(span=9, adjust=False).mean()
    # calculate the MACD value
    df_plot['MACD'] = 2 * (df_plot['DIF']-df_plot["DEA"])
    df_plot['DIF'].plot(linewidth = 0.5, color = 'red', label = 'MACD')
    df_plot['DEA'].plot(linewidth = 0.5, color='blue', label='Signal')
    # set positive MACD with red bar and negative MACD with green bar
    for index, row in df_plot.iterrows():
        if (row['MACD']>0):
            plt.bar(row['timestamp'],row['MACD'],width=0.5,color ='red')
        else:
            plt.bar(row['timestamp'], row['MACD'], width=0.5, color='green')
    # save the space at x axis by decreasing the number of label
    major_index = df_plot.index[df_plot.index%40==0]
    major_xtics = df_plot['timestamp'][df_plot.index%40==0]
    plt.xticks(major_index,major_xtics)
    plt.setp(plt.gca().get_xticklabels(), rotation=60)
    # set grid to the chart
    plt.grid(linestyle='-.')
    plt.legend()
    plt.title('MACD of {}'.format(label), fontsize=12)
    plt.show()

matplotlib("MMM",200)
