#Luke Williams 18051086
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#Connect to database and create sorted dataframe
conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
SQL_Query = pd.read_sql_query("SELECT Sector, Industry, MarketCapitalization FROM FUNDAMENTALS", conn)
df = pd.DataFrame(SQL_Query, columns = ['Sector', 'Industry', 'MarketCapitalization'])
df.sort_values(by=['MarketCapitalization'], inplace=True, ascending=False)

#loop through dataframe and create dictionary which calculates the sum of mktcap for each sector
mktcap = {}
for index, row in df.iterrows():
    if row['Sector'] not in mktcap:
        mktcap[row['Sector']] = row['MarketCapitalization']
    else:
        mktcap[row['Sector']] += row['MarketCapitalization']

#create a new sorted dictionary so the donut chart is sorted
mktcap_sorted = dict(sorted(mktcap.items(), key=lambda item: item[1]))

#Getting the labels and values for the pie chart
labels = list(mktcap_sorted.keys())
values = list(mktcap_sorted.values())

#Choosing the colours for the pie chart
colours = ['lightcoral','coral','wheat', 'gold','yellowgreen','mediumseagreen','lightseagreen','lightskyblue','dodgerblue','mediumslateblue','darkorchid','hotpink']

#Plotting the pie chart
plt.pie(values,labels=labels, radius=1.6, wedgeprops = {'linewidth':1.5,'edgecolor':'black'}, shadow=True, colors=colours,autopct='%1.1f%%', pctdistance=0.65, labeldistance=1.1)

#Plotting a white cirlce to convert from pie chart to donut chart
circle = plt.Circle((0,0),1.2, color='black', fc='white', linewidth=1.5)
fig=plt.gcf()
fig.gca().add_artist(circle)
plt.subplots_adjust(left=0.26, bottom=0.238, right=0.745, top=0.824)
plt.show()
