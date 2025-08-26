# 💰 Expense Tracker

An AI-powered **Expense Tracker** built with **Flask** that helps you manage your personal finances effectively.  
With features like **login/register, expense tracking, AI suggestions, recurring expenses, import/export, dashboard analytics, and financial Q&A**, it goes beyond just tracking expenses – it acts like your personal finance assistant.

---

## ✨ Features

- 🔐 **User Authentication** – Secure Login & Register system  
- 📝 **Add Expenses** – Track daily, weekly, and monthly expenses  
- 🤖 **AI Suggestions** – Get smart financial insights powered by **Google Gemini 2.5 Flash**  
- 📊 **Dashboard Analytics** – Visual analysis of your financial data  
- 📆 **Monthly Breakdown** – Understand spending patterns month by month  
- 🔄 **Recurring Expenses** – Add EMI, loans, subscriptions, etc. with automated tracking  
- 📥 **Import / Export** – Export expenses to CSV/Excel or import past records  
- ❓ **Ask Questions** – Chat-like interface to ask about your overall financial health  

---

## 🛠️ Tech Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)  
- **Frontend**: Jinja2 templates rendered by Flask, HTML, CSS, JavaScript  
- **Database**: SQLite / MySQL (based on configuration)  
- **AI Model**: [Gemini 2.5 Flash](https://ai.google.dev/) for financial suggestions  
- **Visualization**: Matplotlib / Chart.js for graphs and dashboards  

---

## 📂 Project Structure

ExpenseTracker/
│── app.py # Main Flask app (routes & logic)
│── models.py # Database models
│── static/ # CSS, JS, Images
│── templates/ # HTML templates (Jinja2)
│── requirements.txt # Python dependencies
│── README.md # Project documentation



---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.


### 1️⃣ Clone the repository
```bash
git clone https://github.com/Sahil-2005/ExpenseTracker.git
cd ExpenseTracker


Create a virtual environment
python -m venv venv


Activate it:

Windows
venv\Scripts\activate


Linux / macOS
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Flask server
python app.py


The app will be running at: http://127.0.0.1:5000/



📈 Roadmap
 Dark Mode support
 Multi-user financial comparisons
 Notifications & reminders for recurring expenses


🤝 Contributing
Contributions are welcome!
Fork the repo
Create a feature branch (git checkout -b feature-name)
Commit your changes (git commit -m 'Added feature')
Push to your branch (git push origin feature-name)
Open a Pull Request


🧑‍💻 Author
Sahil Gawade
🌐 Portfolio: sahil-gawade.netlify.app
💼 LinkedIn: linkedin.com/in/sahil-gawade-920a0a242
📌 GitHub: Sahil-2005



📜 License
This project is licensed under the MIT License – feel free to use and modify for your own projects.


⭐ Support
If you find this project useful, don’t forget to star ⭐ the repository and share it with others!

