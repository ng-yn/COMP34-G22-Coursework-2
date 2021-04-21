from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, ValidationError
import sqlite3


class SearchBar(FlaskForm):
    stock = StringField(label='Stock Name', validators=[InputRequired()])

    # def validate_stock(self,stock):
    #     conn = sqlite3.connect('../FinancialDatabase.db')
    #     # c = conn.cursor()
    #     # c.execute(""" SELECT name FROM sqlite_master WHERE type='table' AND name=?; """, (stock, ))
