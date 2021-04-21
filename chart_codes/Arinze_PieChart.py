# Created by Arinze David Nwanna
import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as pdr

# Creating watchlist
tickers = ['AAPL', 'AMZN', 'TSLA', 'BABA', 'PYPL']
amounts = [10, 10, 10, 10, 10]
prices = []
total = []

# Extracting data
for ticker in tickers:
    df = pdr.DataReader(ticker, 'yahoo', dt.datetime(2019, 8, 1), dt.datetime.now())
    price = df[-1:]['Close'][0]
    prices.append(price)
    index = tickers.index(ticker)
    total.append(price * amounts[index])

# Create figure
fig, ax = plt.subplots(figsize=(11, 6))

# Formatting figure
ax.set_facecolor('white')
ax.figure.set_facecolor('white')
ax.tick_params(axis='x', color='black')
ax.tick_params(axis='y', color='black')
ax.set_title('Portfolio Visualiser', color='Black', fontsize=25)
_, texts, _ = ax.pie(total, labels=tickers, autopct='%1.1f%%', pctdistance=0.8)
[text.set_color('black') for text in texts]

# Make it a pie ring by adding a circle
my_circle = plt.Circle((0, 0), 0.55, color='white')
plt.gca().add_artist(my_circle)

ax.text(-2, 1, "Portfolio Overview", fontsize=14, color='black', verticalalignment='center',
        horizontalalignment='center')
ax.text(-2, 0.85, f'Total USD amount: {sum(total):.2f} $', fontsize=12, color='black', verticalalignment='center',
        horizontalalignment='center')
counter = 0.15

for ticker in tickers:
    ax.text(-2, 0.85 - counter, f' {ticker}: {total[tickers.index(ticker)]:.2f} $', fontsize=12, color='black',
            verticalalignment='center', horizontalalignment='center')
    counter += 0.15

# Save to local disk
plt.savefig('/Users/arinze/PycharmProjects/coursework-1-groups-group-22-comp0034/static/charts/Pie_Chart.png')
