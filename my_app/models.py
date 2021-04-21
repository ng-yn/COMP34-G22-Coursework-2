from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from my_app import db


class User(UserMixin, db.Model):
    # ONLY USE THIS FOR THE FIRST INSTANCE OF THE DATABASE
    __tablename__ = "user"
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.Text, nullable=False)
    # email = db.Column(db.Text, unique=True, nullable=False)
    # password = db.Column(db.Text, nullable=False)
    # image_file = db.Column(db.Text, nullable=False, default='default.jpg')
    # #
    __table__ = db.Model.metadata.tables['user']

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.password} {self.image_file}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserWatchlist(db.Model):
    __table__ = db.Model.metadata.tables['USER_WATCHLISTS']

    def __repr__(self):
        return f"{self.user_id} {self.watchlist_id} {self.watchlist_name}"


class WatchlistItem(db.Model):
    __table__ = db.Model.metadata.tables['WATCHLIST_ITEMS']

    def __repr__(self):
        return f"{self.user_id} {self.watchlist_id} {self.ticker}"


class Fundamentals(db.Model):
    __table__ = db.Model.metadata.tables['FUNDAMENTALS']

    def __repr__(self):
        return f"{self.Symbol} {self.AssetType} {self.Name} {self.Description} {self.Exchange} {self.Country} " \
               f"{self.Sector} {self.Industry} {self.Address} {self.FullTimeEmployees} {self.FiscalYearEnd} " \
               f"{self.LatestQuarter} {self.MarketCapitalization} {self.EBITDA} {self.PERatio} {self.PEGRatio} " \
               f"{self.BookValue} {self.DividendPerShare} {self.DividendYield} {self.EPS} {self.RevenuePerShareTTM} " \
               f"{self.ProfitMargin} {self.OperatingMarginTTM} {self.ReturnOnAssetsTTM} {self.ReturnOnEquityTTM} " \
               f"{self.RevenueTTM} {self.GrossProfitTTM} {self.DilutedEPSTTM} {self.QuarterlyEarningsGrowthYOY} " \
               f"{self.QuarterlyRevenueGrowthYOY} {self.AnalystTargetPrice} {self.TrailingPE} {self.ForwardPE} " \
               f"{self.PriceToSalesRatioTTM} {self.PriceToBookRatio} {self.EVToRevenue} {self.EVToEBITDA} {self.Beta} " \
               f"{self._52WeekHigh} {self._52WeekLow} {self._50DayMovingAverage} {self._200DayMovingAverage} " \
               f"{self.SharesOutstanding} {self.SharesFloat} {self.SharesShort} {self.SharesShortPriorMonth} " \
               f"{self.ShortRatio} {self.ShortPercentOutstanding} {self.ShortPercentFloat} {self.PercentInsiders} " \
               f"{self.PercentInstitutions} {self.ForwardAnnualDividendRate} {self.ForwardAnnualDividendYield} " \
               f"{self.PayoutRatio} {self.DividendDate} {self.ExDividendDate} {self.LastSplitFactor} {self.LastSplitDate}"


class Profile(db.Model):
    # __tablename__ = "profile"
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.Text, unique=True, nullable=False)
    # bio = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table__ = db.Model.metadata.tables['profile']

    def __repr__(self):
        return f"{self.id} {self.username} {self.bio} {self.user_id}"


class Posts(db.Model):
    # ONLY USE THIS FOR THE FIRST INSTANCE OF THE DATABASE
    # __tablename__ = "posts"
    # id = db.Column(db.Integer, primary_key=True)
    # created = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    # title = db.Column(db.Text, nullable=False)
    # content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table__ = db.Model.metadata.tables['posts']

    def __repr__(self):
        return f"{self.id} {self.created} {self.title} {self.content} {self.user_id}"
