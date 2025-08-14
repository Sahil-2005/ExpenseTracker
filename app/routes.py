import io
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from .models import User, Expense
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask import session, redirect, url_for
from flask import get_flashed_messages
from flask import Response
import csv
from io import StringIO
from datetime import datetime, timedelta

from .gemini_utils import generate_financial_suggestions
from .gemini_utils import parse_gemini_response, handle_user_query


main = Blueprint('main', __name__)

from . import login_manager

from .models import RecurringExpense


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please login or use another.', 'danger')
            return redirect(url_for('main.register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw, income=0)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')


@main.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    total_income = sum(e.amount for e in expenses if e.type == 'Income')
    total_expense = sum(e.amount for e in expenses if e.type == 'Expense')
    
    
    categories = {}
    for e in expenses:
        key = f"{e.category} ({e.type})"  
        categories[key] = categories.get(key, 0) + e.amount

    labels = list(categories.keys())
    values = list(categories.values())
    
    chart_data = [{
        "type": e.type,
        "category": e.category,
        "amount": e.amount
    } for e in expenses]
    types = [e.type for e in expenses]  


    return render_template('dashboard.html',
                           income=total_income,
                           total_expense=total_expense,
                           labels=labels,
                           values=values,
                           chart_data=chart_data,
                           types=types,
                           expenses=expenses,
                           username=current_user.username)



@main.route('/calendar')
@login_required
def calendar_view():
    user_id = current_user.id
    expenses = Expense.query.filter_by(user_id=user_id).all()

    events = []
    for e in expenses:
        events.append({
            'title': f"{e.category} - ₹{e.amount}",
            'start': e.date.strftime('%Y-%m-%d'),
            'color': '#28a745' if e.type == 'Income' else '#dc3545',
            'category': e.category,  # ✅ Added directly
            'extendedProps': {
                'type': e.type,
                'amount': e.amount,
                'description': e.description
            }
        })


    print(events)
    return render_template('calendar.html', events=events)



@main.route('/export', methods=['GET'])
@login_required
def export_data():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Type', 'Category', 'Amount', 'Description', 'Date'])

    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    for e in user_expenses:
        cw.writerow([e.type, e.category, e.amount, e.description, e.date.strftime('%Y-%m-%d')])

    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=transactions.csv"
    return output



@main.route('/import', methods=['POST'])
@login_required
def import_data():
    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        flash('Please upload a valid CSV file.', 'danger')
        return redirect(url_for('main.expenses'))

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)

    for row in csv_input:
        try:
            if not any(row.values()):
                continue

            new_expense = Expense(
                type=row['Type'],
                category=row['Category'],
                amount=float(row['Amount']),
                description=row['Description'],
                date=datetime.strptime(row['Date'], "%d-%m-%Y"),
                user_id=current_user.id
            )
            db.session.add(new_expense)
        except Exception as e:
            print(f"Error in row: {row} - {e}")

    db.session.commit()
    flash('Data imported successfully!', 'success')
    return redirect(url_for('main.expenses'))




@main.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('main.expenses'))

    if request.method == 'POST':
        expense.type = request.form['type']
        expense.category = request.form['category']
        expense.amount = request.form['amount']
        expense.description = request.form['description']
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.expenses'))

    return render_template('edit_expense.html', expense=expense)



@main.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('main.expenses'))

    # If it's a recurring type expense, remove matching recurring entry as well
    if expense.type.lower() == "recurring":
        recurring = RecurringExpense.query.filter_by(
            name=expense.category,  # category stores the recurring name
            user_id=current_user.id
        ).first()

        if recurring:
            db.session.delete(recurring)
            flash(f"Recurring expense '{recurring.name}' also deleted!", "info")

    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('main.expenses'))



@main.route('/monthly-breakdown')
@login_required
def monthly_breakdown():
    from sqlalchemy import extract, func
    from collections import defaultdict
    import calendar

    # Step 1: Query to fetch monthly grouped data
    monthly_data = db.session.query(
        extract('year', Expense.date).label('year'),
        extract('month', Expense.date).label('month'),
        Expense.type,
        func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by('year', 'month', Expense.type).order_by('year', 'month').all()

    monthly_summary = defaultdict(lambda: {'Income': 0, 'Expense': 0})
    for entry in monthly_data:
        label = f"{calendar.month_abbr[int(entry.month)]} {int(entry.year)}"
        monthly_summary[label][entry.type] = entry.total

    labels = list(monthly_summary.keys())
    income_data = [monthly_summary[month]['Income'] for month in labels]
    expense_data = [monthly_summary[month]['Expense'] for month in labels]

    # Compute best savings month (max difference between income and expense)
    best_month_index = 0
    if income_data and expense_data:
        differences = [i - e for i, e in zip(income_data, expense_data)]
        max_diff = max(differences)
        best_month_index = differences.index(max_diff)

    # Compute highest expense month
    highest_expense_index = expense_data.index(max(expense_data)) if expense_data else 0

    return render_template('monthly.html',
                           labels=labels,
                           income_data=income_data,
                           expense_data=expense_data,
                           best_month_index=best_month_index,
                           highest_expense_index=highest_expense_index)




@main.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    current = session.get('theme', 'light-mode')
    session['theme'] = 'dark-mode' if current == 'light-mode' else 'light-mode'
    return redirect(request.referrer or url_for('main.dashboard'))


from dateutil.relativedelta import relativedelta  

@main.route('/add_recurring_expense', methods=['POST'])
@login_required
def add_recurring_expense():
    name = request.form['name']
    total_amount = float(request.form['total_amount'])
    installments = int(request.form['installments'])
    frequency = request.form['frequency']
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()

    # Calculate installment amount
    installment_amount = round(total_amount / installments, 2)

    # Calculate end date
    if frequency == 'monthly':
        end_date = start_date + relativedelta(months=installments - 1)
    elif frequency == 'weekly':
        end_date = start_date + relativedelta(weeks=installments - 1)
    else:
        flash("Invalid frequency selected", "danger")
        return redirect(url_for('main.expenses'))

    new_recurring = RecurringExpense(
        name=name,
        total_amount=total_amount,
        installment_amount=installment_amount,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
        installments_remaining=installments,
        user_id=current_user.id
    )

    db.session.add(new_recurring)
    db.session.commit()
    flash("Recurring expense added!", "success")
    return redirect(url_for('main.expenses'))







@main.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    if request.method == 'POST':
        e = Expense(
            type=request.form['type'],
            category=request.form['category'],
            amount=request.form['amount'],
            description=request.form['description'],
            user_id=current_user.id
        )
        db.session.add(e)
        db.session.commit()

    now = datetime.now().date()
    recurring_expenses = RecurringExpense.query.filter_by(user_id=current_user.id).all()

    for rec in recurring_expenses:
        if rec.installments_remaining == 0 or now < rec.start_date:
            continue  # fully paid or not started yet

        apply = False
        if rec.last_applied is None:
            apply = True
        elif rec.frequency == 'monthly':
            if rec.last_applied.month != now.month or rec.last_applied.year != now.year:
                apply = True
        elif rec.frequency == 'weekly':
            if rec.last_applied + timedelta(weeks=1) <= now:
                apply = True

        if apply:
            new_exp = Expense(
                type='Recurring',
                category=rec.name,
                amount=rec.installment_amount,
                description=f"{rec.name} - installment auto-deducted",
                user_id=current_user.id
            )
            db.session.add(new_exp)

            rec.last_applied = now
            rec.installments_remaining -= 1

    db.session.commit()

    all_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

    return render_template(
        'expenses.html',
        expenses=all_expenses,
        recurring_expenses=recurring_expenses
    )




@main.route('/debug-expenses')
@login_required
def debug_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return f"Found {len(expenses)} records for user {current_user.id}"



@main.route('/ai-suggestions', methods=['GET', 'POST'])
@login_required
def ai_suggestions():
    from collections import defaultdict
    from app.models import Expense, RecurringExpense  # Make sure this is imported

    user_id = current_user.id

    # Get all one-time expenses
    expenses = Expense.query.filter_by(user_id=user_id).all()

    # Get all active recurring expenses
    recurring_expenses = RecurringExpense.query.filter_by(user_id=user_id).all()

    # Income and expense total from Expense table
    income = sum(e.amount for e in expenses if e.type.lower() == 'income')
    expense_total = sum(e.amount for e in expenses if e.type.lower() == 'expense')

    category_totals = defaultdict(float)

    # Add regular expenses to category totals
    for e in expenses:
        if e.type.lower() == 'expense':
            category_totals[e.category] += e.amount

    # Add recurring expenses to category totals
    for rec in recurring_expenses:
        # category_totals[f"(Recurring) {rec.name}"] += rec.amount
        # expense_total += rec.amount  # Add recurring to overall total
        category_totals[f"(Recurring) {rec.name}"] += rec.installment_amount
        expense_total += rec.installment_amount


    # Format category-wise expense breakdown
    expense_summary = ""
    for category, total in category_totals.items():
        expense_summary += f"- {category}: ₹{total}\n"

    # Generate AI response
    ai_response = generate_financial_suggestions(income, expense_summary)
    parsed = parse_gemini_response(ai_response)

    overspending = "<br>".join(f"- {point}" for point in parsed["overspending"])
    estimated_savings = "<br>".join(f"{k}: {v}" for k, v in parsed["savings"].items())
    improving_savings = "<br>".join(f"- {tip}" for tip in parsed["improvement"])
    investment_suggestions = "<br>".join(f"- {inv}" for inv in parsed["investment"])
    motivational_quote = parsed["quote"]

    # Handle user query (POST)
    user_response = None
    if request.method == "POST":
        user_query = request.form.get("user_query")
        if user_query:
            user_response = handle_user_query(user_query)

    return render_template(
        "ai_suggestions.html",
        overspending=overspending,
        estimated_savings=estimated_savings,
        improving_savings=improving_savings,
        investment_suggestions=investment_suggestions,
        motivational_quote=motivational_quote,
        ai_response=ai_response,
        user_response=user_response
    )




@main.route('/ai-suggestions-loading')
@login_required
def ai_suggestions_loading():
    return render_template("ai_suggestions_loading.html")



@main.route('/ask-ai', methods=['POST'])
@login_required
def ask_ai():
    user_query = request.json.get("user_query")
    if user_query:
        user_response = handle_user_query(user_query)
        return jsonify({"response": user_response})
    return jsonify({"response": "⚠️ No query provided."}), 400




@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
