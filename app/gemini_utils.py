# # gemini_utils.py
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model = genai.GenerativeModel('gemini-2.5-flash')

# def generate_financial_suggestions(income, expense_data):
#     prompt = f"""
# You are a professional financial advisor. Analyze the following user's financial situation:

# - Total Income: ₹{income}
# - Expenses:
# {expense_data}

# Return the response in the **exact format below** (no extra commentary or markdown formatting):

# ---
# Areas of Potential Overspending:
# - [Point 1]
# - [Point 2]
# - ...

# Estimated Savings:
# - Monthly Savings: ₹[amount]
# - Weekly Savings: ₹[amount]

# Improving Savings:
# - [Tip 1]
# - [Tip 2]
# - ...

# Investment Suggestions:
# - [Suggestion 1]
# - [Suggestion 2]
# - ...

# Motivational Quote:
# "[2-line quote about financial discipline]"

# ---
# Only return content in this format.
# """


#     response = model.generate_content(prompt)
#     return response.text


# gemini_utils.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_financial_suggestions(income, expense_data):
    prompt = f"""
You are a professional financial advisor. Analyze the following user's financial situation:

- Total Income: ₹{income}
- Expenses:
{expense_data}

Return the response in the **exact format below** (no extra commentary or markdown formatting):

---
Areas of Potential Overspending:
- [Point 1]
- [Point 2]
- ...

Estimated Savings:
- Monthly Savings: ₹[amount]
- Weekly Savings: ₹[amount]

Improving Savings:
- [Tip 1]
- [Tip 2]
- ...

Investment Suggestions:
- [Suggestion 1]
- [Suggestion 2]
- ...

Motivational Quote:
"[2-line quote about financial discipline]"

---
Only return content in this format.
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
