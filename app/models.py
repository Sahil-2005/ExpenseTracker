# from . import db
# from flask_login import UserMixin
# from datetime import datetime

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     income = db.Column(db.Float, default=0)

#     expenses = db.relationship('Expense', backref='user', lazy=True)


# class Expense(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(10)) 
#     category = db.Column(db.String(50))
#     amount = db.Column(db.Float)
#     date = db.Column(db.Date, default=datetime.utcnow)
#     description = db.Column(db.String(200))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# models.py

from . import db
from flask_login import UserMixin
from datetime import datetime, date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    income = db.Column(db.Float, default=0)

    expenses = db.relationship('Expense', backref='user', lazy=True)
    recurring_expenses = db.relationship('RecurringExpense', backref='user', lazy=True)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10)) 
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class RecurringExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # Null if ongoing
    frequency = db.Column(db.String(20), default="Monthly")  # Can be Monthly, Weekly, etc.
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
