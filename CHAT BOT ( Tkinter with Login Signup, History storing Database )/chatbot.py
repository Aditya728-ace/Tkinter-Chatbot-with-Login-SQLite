import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key='AIzaSyBlk-AzukxmjqorlZD-q18Jq-A-bfmeHqQ')

# Path for user credentials database
USER_CREDENTIALS_DB = 'user_credentials.db'

# Create the user credentials database
def create_user_credentials_db():
    if not os.path.exists(USER_CREDENTIALS_DB):
        conn = sqlite3.connect(USER_CREDENTIALS_DB)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Store user credentials (username and password)
def store_user_credentials(username, password):
    conn = sqlite3.connect(USER_CREDENTIALS_DB)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Check if the username already exists
def check_user_exists(username):
    conn = sqlite3.connect(USER_CREDENTIALS_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Authenticate user by username and password
def authenticate_user(username, password):
    conn = sqlite3.connect(USER_CREDENTIALS_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    stored_password = cursor.fetchone()
    conn.close()
    
    if stored_password:
        return stored_password[0] == password
    return False

# API call to get chatbot response
def get_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Create a user-specific chat history database
def create_user_chat_history_db(username):
    db_file = f"chat_history_{username}.db"
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

# Store user chat history in their user-specific database
def save_chat_history(username, user_input, response):
    db_file = f"chat_history_{username}.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chats (user_input, response) VALUES (?, ?)
    ''', (user_input, response))
    conn.commit()
    conn.close()

# Load chat history from the user-specific database
def load_chat_history(username):
    db_file = f"chat_history_{username}.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_input, response FROM chats ORDER BY timestamp ASC
    ''')
    chat_history = cursor.fetchall()
    conn.close()
    return chat_history

# GUI for Chatbot with Tkinter
class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot - Login")
        self.root.geometry("500x500")
        self.username = ""
        
        self.create_login_page()

    def create_login_page(self):
        self.clear_window()

        login_frame = tk.Frame(self.root, padx=10, pady=10)
        login_frame.pack(padx=10, pady=10)

        tk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=0, column=1)

        tk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*", width=25)
        self.password_entry.grid(row=1, column=1)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Login", font=("Arial", 12), command=self.login).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Sign Up", font=("Arial", 12), command=self.create_signup_page).grid(row=0, column=1)

    def create_signup_page(self):
        self.clear_window()

        signup_frame = tk.Frame(self.root, padx=10, pady=10)
        signup_frame.pack(padx=10, pady=10)

        tk.Label(signup_frame, text="Create Username:", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        self.new_username_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25)
        self.new_username_entry.grid(row=0, column=1)

        tk.Label(signup_frame, text="Create Password:", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        self.new_password_entry = tk.Entry(signup_frame, font=("Arial", 12), show="*", width=25)
        self.new_password_entry.grid(row=1, column=1)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Sign Up", font=("Arial", 12), command=self.signup).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Back to Login", font=("Arial", 12), command=self.create_login_page).grid(row=0, column=1)

    def signup(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        if check_user_exists(username):
            messagebox.showerror("Error", "Username already exists!")
            return

        store_user_credentials(username, password)
        create_user_chat_history_db(username)  # Create user-specific chat history DB
        messagebox.showinfo("Success", "Sign Up Successful! Please log in.")
        self.create_login_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if authenticate_user(username, password):
            self.username = username
            self.create_chat_page()
        else:
            messagebox.showerror("Error", "Invalid Username or Password!")

    def create_chat_page(self):
        self.clear_window()
        self.root.title(f"Chatbot - {self.username}")

        chat_frame = tk.Frame(self.root, padx=10, pady=10)
        chat_frame.pack(padx=10, pady=10)

        self.chat_box = tk.Text(chat_frame, width=60, height=20, font=("Arial", 12), state=tk.DISABLED, wrap=tk.WORD)
        self.chat_box.pack(pady=10)

        message_frame = tk.Frame(self.root, padx=10, pady=10)
        message_frame.pack(pady=10)

        self.message_entry = tk.Entry(message_frame, width=40, font=("Arial", 12))
        self.message_entry.grid(row=0, column=0, padx=5)

        tk.Button(message_frame, text="Send", font=("Arial", 12), command=self.send_message).grid(row=0, column=1)

        # Configure tags for the Text widget inside the chat page
        self.chat_box.tag_configure("user_message", justify='right', background='#c1e1fc', relief='solid', padding=5)
        self.chat_box.tag_configure("chatbot_message", justify='left', background='#f2f2f2', relief='solid', padding=5)

        self.load_chat_history()

    def send_message(self):
        user_input = self.message_entry.get()
        if user_input:
            response = get_response(user_input)

            # Display user message in a box on the right
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, f"You: {user_input}\n", "user_message")
            self.chat_box.insert(tk.END, f"Chatbot: {response}\n\n", "chatbot_message")
            self.chat_box.config(state=tk.DISABLED)

            self.save_chat_history(user_input, response)

            self.message_entry.delete(0, tk.END)

    def load_chat_history(self):
        chat_history = load_chat_history(self.username)
        self.chat_box.config(state=tk.NORMAL)
        for user_input, response in chat_history:
            self.chat_box.insert(tk.END, f"You: {user_input}\n", "user_message")
            self.chat_box.insert(tk.END, f"Chatbot: {response}\n\n", "chatbot_message")
        self.chat_box.config(state=tk.DISABLED)

    def save_chat_history(self, user_input, response):
        save_chat_history(self.username, user_input, response)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    create_user_credentials_db()
    root = tk.Tk()
    
    app = ChatBotApp(root)
    root.mainloop()
