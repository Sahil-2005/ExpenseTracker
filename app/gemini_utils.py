# gemini_utils.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def generate_financial_suggestions(income, expense_data):
    prompt = f"""
You are a financial advisor. Here's a user's financial data:

- Total Income: ₹{income}
- Expenses:
{expense_data}

Please:
1. Highlight where the user is overspending.
2. Estimate weekly/monthly savings.
3. Suggest how the user can improve savings.
4. Give investment suggestions based on saved money.
5. Provide a 2-line motivational quote related to financial discipline.
Make the tone friendly but professional.
"""

    response = model.generate_content(prompt)
    return response.text
