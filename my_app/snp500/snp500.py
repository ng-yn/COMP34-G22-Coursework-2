# S&P 500 index page
from io import BytesIO, StringIO
import base64
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, send_file
from my_app.snp500.forms import SearchBar
from my_app.models import Fundamentals
from my_app import db
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as py

snp500_bp = Blueprint('snp500_bp', __name__, url_prefix='/index')
# conn = sqlite3.connect('../data/FinancialDatabase.db')


@snp500_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchBar()
    # if form.validate_on_submit():
    # #     # result = Fundamentals.query.filter_by(Symbol='ticker')
    #     return redirect(url_for('watchlist_bp.index'))
    return render_template('snp500.html', title='S&P 500 Index', form=form)


@snp500_bp.route('/autocomplete_tickers', methods=['GET'])
def autocomplete_tickers():
    text = request.args.get('ticker')
    query = db.session.query(Fundamentals.Symbol).filter(Fundamentals.Symbol.like('%' + str(text) + '%'))
    results = [item.Symbol for item in query.all()][:10]  # limit first 10 results
    return jsonify(results)


@snp500_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        term = request.form['autocomplete_tickers']
        if term == "":
            flash("Enter a label to search for")
            return redirect(url_for('snp500_bp.index'))
        plotly_graph_object()
        results = Fundamentals.query.filter_by(Symbol=term).first()

        # figure = plotly_graph_object(str(term), 300)
        if not results:
            flash("No symbol found with that name")
            return redirect(url_for('snp500_bp.index'))
        return render_template("search_result.html", title=str(term), results=results)
    else:
        return redirect(url_for('snp500_bp.index'))


def plotly_graph_object():
    term = request.form['autocomplete_tickers']
    # conn = sqlite3.connect('../data/FinancialDatabase.db')
    df = pd.read_sql_query("SELECT * from {}".format(term), db.engine)
    df_plot = df[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 300 days' data
    df_plot = df_plot.head(300)
    # using candlestick chart with plotly graph object to plot the stock price
    fig = go.Figure(go.Candlestick(x=df_plot['timestamp'], open=df_plot['open'],
                                   high=df_plot['high'], low=df_plot['low'],
                                   close=df_plot['close'], name='Stock Price'))
    # adding the moving average line with two different period
    ma_10 = df_plot['close'].rolling(10, min_periods=1).mean()
    ma_50 = df_plot['close'].rolling(50, min_periods=1).mean()
    fig.add_trace(go.Scatter(x=df_plot['timestamp'], y=ma_10, line=dict(color='royalblue')
                             , name='Moving Average 10'))
    fig.add_trace(go.Scatter(x=df_plot['timestamp'], y=ma_50, line=dict(color='chocolate')
                             , name='Moving Average 50'))
    # set the chart title and axis label to the chart
    fig.update_layout(
        title="{} Stock Price".format(term),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Technical Data",
        font=dict(size=18, color="Black")
    )
    # return fig
    return fig.write_html('static/img/' + "{}".format(term) + '.html',
                          full_html=False,
                          include_plotlyjs='cdn')
    # img = StringIO()
    # fig.savefig(img, format='png')
    # fig.close()
    # img.seek(0)
    # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    # return render_template('search_result.html', plot_url=plot_url)
    # fig.show()
    # fig.write_html("my_app/templates/stock_graph.html")
    # html_div = py.plot(fig, output_type='div')
    # return fig.write_image("templates/stock.jpg")
    # return send_file(img, mimetype='image/png')

    # text = request.args.get('ticker')
    # query = db.session.query(Fundamentals).filter(Fundamentals.Symbol)
    # results = db.session.query(search).filter(Fundamentals.(search)).all()
    #
    # ticker = request.form.get("autocomplete_tickers")
    # all_tickers = [item.Symbol for item in Fundamentals.query.all()]
    # if ticker not in all_tickers:
    #     flash("Invalid ticker")
    #     return redirect(url_for('snp500.index'))
    # if ticker in all_tickers:
    #     flash("Successful")
    # # try:
    # #     watchlist_item = WatchlistItem(user_id=current_user.get_id(), watchlist_id=watchlist_id, ticker=ticker)
    # #     db.session.add(watchlist_item)
    # #     db.session.commit()
    # # except Exception as e:
    # #     flash("Failed to add ticker")
    # return redirect(url_for('snp500.index'))
# def search():
#     if request.method == 'POST':
#         term = request.form['search_term']
#         if term == "":
#             flash("Enter a name to search for")
#             return redirect(url_for('index'))
#     #users = with_polymorphic(User, [Company_name])
#     #results = db.session.query(Company_name).filter(
#         #Company_name.Symbol.contains(term)).all()
#         results = Company_name.query.filter(Company_name.Symbol.contains(term)).all()
#         if not results:
#             flash("No company found with that label.")
#             return redirect(url_for('index'))
#         return render_template('search_bar.html', results=results)
#     else:
#         return redirect(url_for('index'))
