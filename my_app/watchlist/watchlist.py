# Watchlist page
import random

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from my_app import db
from my_app.models import UserWatchlist, Fundamentals, WatchlistItem

watchlist_bp = Blueprint('watchlist_bp', __name__, url_prefix='/watchlist')

items = []
for i in range(10):
    items.append({
        'remove': 'x',
        'company': 'company',
        'ticker': 'ticker',
        'sector': 'sector',
        'market_cap': 'cap',
        'price': 100
    })


@watchlist_bp.route('/')
@watchlist_bp.route('/<watchlist_id>')
@login_required
def index(watchlist_id=None):
    current_watchlist_name = "(No watchlist selected)"
    if watchlist_id:
        try:
            current_watchlist_name = UserWatchlist.query.filter_by(user_id=current_user.get_id(),
                                                                   watchlist_id=watchlist_id).first().watchlist_name
        except:
            pass

    tickers = WatchlistItem.query.filter_by(user_id=current_user.get_id(), watchlist_id=watchlist_id).all()
    rows = []
    for ticker in tickers:
        row = Fundamentals.query.filter_by(Symbol=ticker.ticker).first()
        if row is None:
            continue
        else:
            rows.append({
                'remove': 'x',
                'company': row.Name,
                'ticker': ticker.ticker,
                'sector': row.Sector,
                'market_cap': '$' + str(row.MarketCapitalization),
                'price': '$' + str(round(row._50DayMovingAverage, 2)),
            })

    return render_template('watchlist.html', title='Watchlists', items=rows,
                           watchlist_list=UserWatchlist.query.filter_by(user_id=current_user.get_id()),
                           current_watchlist_id=watchlist_id,
                           current_watchlist_name=current_watchlist_name)


@watchlist_bp.route('/create_watchlist', methods=['GET', 'POST'])
@login_required
def create_watchlist():
    new_watchlist_id = str(random.getrandbits(64))
    watchlist = UserWatchlist(user_id=int(current_user.get_id()), watchlist_id=new_watchlist_id,
                              watchlist_name=request.form.get("createWatchlistName"))
    try:
        db.session.add(watchlist)
        db.session.commit()
    except Exception as e:
        flash(str(e))
    return redirect(url_for('watchlist_bp.index', watchlist_id=new_watchlist_id, current_watchlist_id=new_watchlist_id,
                            current_watchlist_name=request.form.get("createWatchlistName")))


@watchlist_bp.route('/delete_watchlist', methods=['GET', 'POST'])
@watchlist_bp.route('/delete_watchlist/<watchlist_id>', methods=['GET', 'POST'])
@login_required
def delete_watchlist(watchlist_id=None):
    try:
        UserWatchlist.query.filter_by(user_id=current_user.get_id(), watchlist_id=watchlist_id).delete()
        db.session.commit()
        flash('Watchlist deleted')
    except Exception as e:
        flash(str(e))
    return redirect(url_for('watchlist_bp.index'))


@watchlist_bp.route('/autocomplete_tickers', methods=['GET'])
@login_required
def autocomplete_tickers():
    text = request.args.get('ticker')
    query = db.session.query(Fundamentals.Symbol).filter(Fundamentals.Symbol.like('%' + str(text) + '%'))
    results = [item.Symbol for item in query.all()][:10]  # limit first 10 results
    return jsonify(results)


@watchlist_bp.route('/add_ticker', methods=['GET', 'POST'])
@login_required
def add_ticker():
    watchlist_id = request.form.get("add_ticker_watchlist_id")
    ticker = request.form.get("autocomplete_tickers")
    all_tickers = [item.Symbol for item in Fundamentals.query.all()]
    if ticker not in all_tickers:
        flash("Invalid ticker")
        return redirect(url_for('watchlist_bp.index', watchlist_id=watchlist_id))
    try:
        watchlist_item = WatchlistItem(user_id=current_user.get_id(), watchlist_id=watchlist_id, ticker=ticker)
        db.session.add(watchlist_item)
        db.session.commit()
    except Exception as e:
        flash("Failed to add ticker")
    return redirect(url_for('watchlist_bp.index', watchlist_id=watchlist_id))


@watchlist_bp.route('/delete_ticker/<ticker>', methods=['GET', 'POST'])
@login_required
def delete_ticker(ticker):
    watchlist_id = request.form.get("delete_ticker_watchlist_id")
    try:
        WatchlistItem.query.filter_by(user_id=current_user.get_id(), watchlist_id=watchlist_id, ticker=ticker).delete()
        db.session.commit()
    except Exception as e:
        flash(str(e))
    return redirect(url_for('watchlist_bp.index', watchlist_id=watchlist_id))
