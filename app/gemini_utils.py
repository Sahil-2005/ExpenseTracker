# gemini_utils.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


def generate_financial_suggestions(income, expense_data):
    prompt = f"""
You are a certified financial advisor helping users understand and improve their personal finance. A user has provided the following information:

- Total Income: ₹{income}
- Expenses:
{expense_data}

Analyze this data and return a detailed and personalized financial advisory report in the EXACT format shown below (no markdown formatting, no numbering, no headings outside the structure).

Make sure:
- Each bullet point gives a **clear explanation**.
- Provide **specific advice or steps** the user can take.
- Write in **simple, professional, yet empathetic tone**.
- Use **Indian financial context** (e.g., SIPs, PPF, etc.)

---

Areas of Potential Overspending:
- [Explanation of area, why it's problematic, and how to control it]
- [Another potential overspending area, why it matters, and suggestion to reduce it]
- ...

Estimated Savings:
- Monthly Savings: ₹[estimated amount] (based on user's income and discretionary expenses)
- Weekly Savings: ₹[weekly equivalent] (include note on how this can compound over time)

Improving Savings:
- [Practical and specific tip to improve saving habits with example or method]
- [Another savings strategy and how the user can implement it right away]
- ...

Investment Suggestions:
- [Detailed suggestion including type of investment, reason, and expected benefit]
- [Another investment option with timeframe, risk level, and purpose]
- ...

Motivational Quote:
"[2-line motivational quote about financial discipline, savings, or smart investing]"

---

Only return content in this format. Do not include any introduction, explanation, or closing remarks.
"""
    response = model.generate_content(prompt)
    return response.text


def parse_gemini_response(response_text):
    sections = {
        "overspending": [],
        "savings": {},
        "improvement": [],
        "investment": [],
        "quote": ""
    }

    lines = response_text.splitlines()
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("Areas of Potential Overspending:"):
            current_section = "overspending"
        elif line.startswith("Estimated Savings:"):
            current_section = "savings"
        elif line.startswith("Improving Savings:"):
            current_section = "improvement"
        elif line.startswith("Investment Suggestions:"):
            current_section = "investment"
        elif line.startswith("Motivational Quote:"):
            current_section = "quote"
        elif current_section == "overspending" and line.startswith("-"):
            sections["overspending"].append(line[2:])
        elif current_section == "savings" and line.startswith("-"):
            key, val = line[2:].split(":")
            sections["savings"][key.strip()] = val.strip()
        elif current_section == "improvement" and line.startswith("-"):
            sections["improvement"].append(line[2:])
        elif current_section == "investment" and line.startswith("-"):
            sections["investment"].append(line[2:])
        elif current_section == "quote" and line.startswith('"') and line.endswith('"'):
            sections["quote"] = line.strip('"')

    return sections



# def handle_user_query(query):
#     from flask_login import current_user
#     from app.models import Expense  # Ensure this is correctly imported

#     from collections import defaultdict

#     user_id = current_user.id
#     expenses = Expense.query.filter_by(user_id=user_id).all()

#     income = sum(e.amount for e in expenses if e.type.lower() == 'income')
#     expense_total = sum(e.amount for e in expenses if e.type.lower() == 'expense')

#     category_totals = defaultdict(float)
#     for e in expenses:
#         if e.type.lower() == 'expense':
#             category_totals[e.category] += e.amount

#     expense_summary = "\n".join(f"- {cat}: ₹{amt}" for cat, amt in category_totals.items())

#     prompt = f"""
# You are a friendly and professional financial assistant. A user has asked a question about their finances. 

# Here is their financial summary:
# - Total Income: ₹{income}
# - Total Expenses: ₹{expense_total}
# - Expense Breakdown by Category:
# {expense_summary}

# Now, respond to their query based on this data. If the query is unrelated to this data, still respond helpfully but briefly.

# User Query: "{query}"

# Response:
# """

#     response = model.generate_content(prompt)
#     return response.text.strip()


def handle_user_query(query):
    from flask_login import current_user
    from app.models import Expense, RecurringExpense
    from collections import defaultdict

    user_id = current_user.id
    expenses = Expense.query.filter_by(user_id=user_id).all()
    recurring_expenses = RecurringExpense.query.filter_by(user_id=user_id).all()

    income = sum(e.amount for e in expenses if e.type.lower() == 'income')
    expense_total = sum(e.amount for e in expenses if e.type.lower() == 'expense')

    category_totals = defaultdict(float)

    for e in expenses:
        if e.type.lower() == 'expense':
            category_totals[e.category] += e.amount

    for rec in recurring_expenses:
        # category_totals[f"(Recurring) {rec.name}"] += rec.amount
        # expense_total += rec.amount
        category_totals[f"(Recurring) {rec.name}"] += rec.installment_amount
        expense_total += rec.installment_amount


    expense_summary = "\n".join(f"- {cat}: ₹{amt}" for cat, amt in category_totals.items())

    prompt = f"""
You are a friendly and professional financial assistant. A user has asked a question about their finances. 

Here is their financial summary:
- Total Income: ₹{income}
- Total Expenses: ₹{expense_total}
- Expense Breakdown by Category:
{expense_summary}

Now, respond to their query based on this data. If the query is unrelated to this data, still respond helpfully but briefly.

User Query: "{query}"

Response:
"""

    response = model.generate_content(prompt)
    return response.text.strip()
