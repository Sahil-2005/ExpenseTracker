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


# app/models.py

# class RecurringExpense(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     frequency = db.Column(db.String(10), nullable=False)  # e.g., 'weekly' or 'monthly'
#     start_date = db.Column(db.Date, nullable=False)  # ✅ Add this line
#     last_applied = db.Column(db.Date, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class RecurringExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)  # total loan/subscription amount
    installment_amount = db.Column(db.Float, nullable=False)  # auto-calculated
    frequency = db.Column(db.String(10), nullable=False)  # weekly/monthly
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)  # auto-calculated
    installments_remaining = db.Column(db.Integer, nullable=False)  # auto-managed
    last_applied = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
