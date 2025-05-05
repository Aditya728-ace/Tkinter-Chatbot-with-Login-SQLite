# Tkinter-Chatbot-with-Login-SQLite
🤖 A simple chatbot built using Tkinter and Gemini API. It features signup and login functionality, with user credentials stored in SQLite. Each user’s chat history is saved in a separate SQLite database for data isolation. Ideal for learning AI-based chatbots with basic authentication and database handling.

---


## ✨ Features

- 🔐 **Signup/Login** functionality with **SQLite database** for secure user authentication.
- 🤖 **Gemini API-powered responses** for intelligent, AI-driven conversations.
- 🖼️ **Messenger-style UI** using **Tkinter** for a familiar and user-friendly interface.
- 📂 **Individual chat history storage** in separate SQLite database files for each user.
- 💬 **Data isolation** for each user’s chat history, stored in user-specific databases.

---

## 🧠 How It Works

1. **User Signup/Login**: Users can create an account or log in using the UI. Credentials are securely stored in an SQLite database.
2. **Chat Interface**: After logging in, users can interact with the chatbot, and their conversations are processed through the Gemini API.
3. **Chat History**: Every user has a personalized SQLite database where their chat history is stored, ensuring **data isolation**.
4. **Seamless User Experience**: The login system is integrated with the frontend, making it easy to manage user accounts and track conversation history.

---

## 🚀 Getting Started

## 1. Clone the Repository
bash
git clone https://github.com/your-username/tkinter-chatbot.git
cd tkinter-chatbot

---

## 2. Install Required Packages
pip install tkinter 
pip install google-generativeai

---

## 3. Add Your Gemini API Key
Visit Google AI to get your Gemini API Key and configure it in your Python file:
api_key = "YOUR_GEMINI_API_KEY"

---

## 🔐 Database Details
users.db: Stores user credentials (username & password) for login authentication.
chat_history.db: For each user, a new SQLite database is created to store their chat history in isolation. The database is named based on the user's username.

---

## 📦 Tech Stack
Backend: Python 3, Tkinter, Gemini API
Database: SQLite

---

## 🚀 Future Improvements
🔑 Add email verification during signup.
🌐 Add multi-language support for responses.
📊 Store chat history on a server for better scalability.
🧑‍💻 Add a multi-user system with different roles (admin, user).

