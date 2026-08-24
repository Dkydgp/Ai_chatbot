# ☕ Cafe De Flora AI Assistant

An AI-powered customer support chatbot built for **Cafe De Flora**.

The assistant helps customers get information about the cafe's menu, prices, vegetarian and non-vegetarian options, ordering, delivery, location, opening hours, and other common questions.

> **Version 1.0 — Beta**

---

## ✨ Features

### 🤖 AI Customer Assistant

- Answers customer questions using Cafe De Flora's business and menu information.
- Uses an OpenRouter-powered AI model.
- Designed to avoid inventing menu items or prices.
- Provides concise and customer-friendly responses.

### 🍽️ Smart Menu Search

Customers can ask questions such as:

- What vegetarian pizzas do you have?
- Give me pasta options under ₹600.
- What is the cheapest item?
- What is the most expensive item?
- What non-vegetarian options are under ₹600?
- Tell me about the Salmon Fillet.

### 🥗 Vegetarian / Non-Vegetarian Filtering

Each menu item contains a dietary classification:

```text
veg
non-veg

The chatbot uses the diet field from menu.json to filter dishes.

Examples:

What vegetarian options are under ₹600?
What non-vegetarian options are under ₹600?

The chatbot does not rely only on the dish name to determine whether an item is vegetarian or non-vegetarian.

💰 Price Filtering

Customers can ask:

What can I get under ₹500?

or:

Give me pasta options under ₹600.

The system filters the menu using the actual prices stored in menu.json.

🍕 Category Filtering

The assistant supports category-based queries including:

Pizza
Pasta
Burgers
Sandwiches
Drinks
Coffee
Desserts
Breakfast
🏆 Cheapest / Most Expensive Items

Customers can ask:

What is the cheapest item on the menu?
What is the most expensive item?

Category-specific queries are also supported:

What is the cheapest pizza?
What is the most expensive pasta?
📍 Cafe Location

The chatbot can provide:

Cafe address
Location information
Directions
Google Maps link

Customers can ask:

Where is Cafe De Flora?
Show me the Google Maps location.
🛵 Online Ordering

Customers can be directed to the available online ordering platforms:

Swiggy
Zomato

Delivery is handled by the respective platform.

The chatbot does not claim that Cafe De Flora directly provides home delivery.

⭐ Customer Feedback

After receiving an answer, customers can rate the response from:

1 to 5 stars

★
★★
★★★
★★★★
★★★★★

For ratings of 1 or 2 stars, the customer must provide a reason.

Available reasons include:

Incorrect information
Didn't answer my question
Information was missing
Other

Customers can also provide an optional comment.

🏗️ Architecture
                    ┌─────────────────────┐
                    │      Customer       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │       + Vite        │
                    └──────────┬──────────┘
                               │
                               │ HTTP API
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          ┌──────────┐   ┌───────────┐  ┌────────────┐
          │ Chatbot  │   │ Retriever │  │  Feedback  │
          │  Logic   │   │   Logic   │  │   System   │
          └────┬─────┘   └─────┬─────┘  └────────────┘
               │               │
               ▼               ▼
        ┌─────────────┐  ┌─────────────────┐
        │  OpenRouter │  │  JSON Knowledge │
        │     AI      │  │     Files       │
        └─────────────┘  └────────┬────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                   business.json      menu.json
📁 Project Structure
Ai_chatbot/
│
├── backend/
│   │
│   ├── app/
│   │   ├── chatbot.py
│   │   ├── config.py
│   │   ├── main.py
│   │   └── retriever.py
│   │
│   ├── knowledge/
│   │   ├── business.json
│   │   └── menu.json
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
CSS
React Markdown
Backend
Python
FastAPI
Uvicorn
OpenAI Python SDK
OpenRouter
Data
JSON-based knowledge files
menu.json
business.json
Feedback / Storage
Supabase
⚙️ Requirements

Install the following before running the project:

Python 3.12+
Node.js
npm
Git
🚀 Installation
1. Clone the Repository
git clone https://github.com/Dkydgp/Ai_chatbot.git

Go into the project:

cd Ai_chatbot
🔧 Backend Setup

Go to the backend directory:

cd backend

Create a virtual environment from the project root:

python -m venv ..\.venv

Activate it on Windows PowerShell:

..\.venv\Scripts\Activate.ps1

Install backend dependencies:

pip install -r requirements.txt
🔐 Environment Variables

Create a file:

backend/.env

Add:

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=your_model_name

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
⚠️ Important

Never upload your real .env file to GitHub.

API keys and other secrets must remain private.

The repository should contain only example configuration or environment-variable placeholders.

▶️ Run the Backend

From:

Ai_chatbot/backend

run:

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

The backend will be available at:

http://localhost:8000
API Documentation

FastAPI Swagger documentation:

http://localhost:8000/docs
Health Check
http://localhost:8000/health

Example:

{
  "status": "healthy"
}
💻 Frontend Setup

Open a second terminal.

Go to the frontend:

cd C:\Users\yadav\Ai_chatbot\frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Vite will provide a local URL, normally:

http://localhost:5173
🔗 API Endpoints
Health Check
GET /health
Example response:

{
  "status": "healthy"
}
Chat
POST /chat

Request:

{
  "message": "What vegetarian pizzas do you have?"
}

Response:

{
  "message": "What vegetarian pizzas do you have?",
  "response": "..."
}
Feedback
POST /feedback

Example request:

{
  "message": "What is the cheapest item?",
  "bot_response": "The cheapest item is...",
  "rating": 5,
  "reason": null,
  "comment": "Very helpful"
}

For ratings of 1 or 2, a reason is required.

🍽️ Menu Knowledge

Menu information is stored in:

backend/knowledge/menu.json

A menu item can contain information such as:

{
  "name": "Example Dish",
  "price": 500,
  "description": "Example description",
  "diet": "veg"
}

Dietary classification uses:

diet = "veg"

or:

diet = "non-veg"

The diet field is used as the authoritative source for vegetarian and non-vegetarian filtering.

📍 Business Knowledge

Business information is stored in:

backend/knowledge/business.json

This contains information such as:

Cafe name
Address
Contact number
Opening hours
Online ordering information
Swiggy link
Zomato link
Google Maps location

The chatbot uses this information when answering business-related questions.

🧠 Chatbot Logic

The chatbot follows two main paths.

Exact Menu Queries

Queries that require reliable menu calculations are handled directly from the menu data.

Examples:

Cheapest item
Most expensive item
Cheapest pizza
Cheapest pasta
Vegetarian options under ₹600
Non-vegetarian options under ₹600
Pasta options under ₹600
Pizza options under ₹600

This reduces the chance of the AI inventing menu information.

General Questions

Other questions are processed using:

Business Knowledge
        +
Relevant Menu Information
        +
OpenRouter AI

The AI is instructed to use only the provided knowledge.

⭐ Feedback Workflow

The feedback process works as follows:

Customer asks question
        ↓
AI provides answer
        ↓
Customer sees 1–5 star rating
        ↓
Rating selected
        ↓
If rating ≤ 2
        ↓
Reason required
        ↓
Optional comment
        ↓
Feedback submitted

This allows future analysis of chatbot quality and customer satisfaction.

🧪 Example Questions

Try asking the assistant:

What is the cheapest item on the menu?
What is the most expensive item?
What is the cheapest pizza?
What is the cheapest pasta?
Give me pasta options under ₹600.
Give me pizza options under ₹700.
What vegetarian options are under ₹600?
What non-vegetarian options are under ₹600?
What vegetarian pizzas do you have?
What non-vegetarian dishes do you have?
Tell me about the Salmon Fillet.
What time do you open?
Do you provide home delivery?
What is the delivery charge?
Where is Cafe De Flora located?
Show me the Google Maps location.
How can I order online?
🔒 Security

Never expose or commit:

.env
OPENROUTER_API_KEY
SUPABASE_KEY

Keep sensitive credentials in environment variables.

The following directories should also remain excluded from Git:

.venv/
__pycache__/
node_modules/
🎯 Version 1.0 Beta

The current beta includes:

AI customer support
Menu search
Menu filtering
Price filtering
Cheapest item detection
Most expensive item detection
Vegetarian filtering
Non-vegetarian filtering
Pizza filtering
Pasta filtering
Cafe information
Opening hours
Online ordering information
Delivery information
Google Maps location
1–5 star feedback
Low-rating reason collection
Optional customer comments
🔮 Future Improvements

Possible future versions may include:

Conversation history
Admin dashboard
Feedback analytics
Frequently asked questions analytics
Automatic menu updates
Real-time item availability
Order status integration
WhatsApp integration
Voice assistant
Multi-language support
Better intent detection
Customer analytics
Production deployment
Admin authentication
Restaurant management dashboard
📌 Project Status

Cafe De Flora AI Assistant — Version 1.0 Beta

The project is currently in the beta stage and is intended for testing, demonstration, and further development of AI-powered restaurant customer support.

👨‍💻 Developer

Developed as an AI-powered customer support prototype for:

Cafe De Flora

📄 License

This project is currently intended for private/demo use.

License terms can be added when the project is released publicly.


