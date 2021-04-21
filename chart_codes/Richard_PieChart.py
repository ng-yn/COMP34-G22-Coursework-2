# Richard Gao 18017045
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')


# Creates a pie chart of the market capitalization of the top 10 largest companies in any given sector
def sector_market_share(sector):
    # Create a dataframe of the symbol, sector and market cap of all companies in the database and sort by market cap
    df = pd.read_sql_query("select Symbol, Sector, MarketCapitalization from Fundamentals;", conn)
    df.sort_values(by=["MarketCapitalization"], inplace=True, ascending=False)
    df = df.reset_index(drop=True)

    # Loop through the dataframe to select the top 10 companies in a given sector and their market cap and then add
    # an "Other" entity to represent the rest of the companies in the sector
    total = 0
    symbols = []
    sizes = []
    for i in range(len(df["Sector"])):
        if df["Sector"][i] == sector:
            total += df["MarketCapitalization"][i]
            if len(symbols) < 10:
                symbols.append(df["Symbol"][i])
                sizes.append(df["MarketCapitalization"][i])
    symbols.append("Other")
    sizes.append(total - sum(sizes))

    # Use matplotlib to create the pie chart
    colours = ['#6da7de', '#9e0059', '#dee000', '#d82222', '#5ea15d', '#943fa6', '#63c5b5', '#ff38ba', '#eb861e',
               '#ee266d', '#cccccc']
    plt.pie(x=sizes, autopct='%1.1f%%', pctdistance=1.15, startangle=90, colors=colours, textprops={'fontsize': 8})
    plt.title("Market Capitalization of the 10 Largest Companies in the {} Sector".format(sector), fontsize=10, y=1.05)
    plt.suptitle("Total Sector Market Capitalization: ${}".format(total), fontsize=9, y=0.91)
    plt.legend(labels=symbols, loc="upper right", bbox_to_anchor=(-0.1, 1), fontsize=8, frameon=False)
    plt.show()
