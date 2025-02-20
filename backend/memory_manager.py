import sqlite3
import os

DB_PATH = "/mnt/ASTRO/astro_memory.db"

def init_db():
    """Créer la base de données et la table si elles n'existent pas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(user, message, response):
    """Enregistrer une conversation dans la base"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_memory (user, message, response) VALUES (?, ?, ?)", (user, message, response))
    conn.commit()
    conn.close()

def get_last_messages(user, limit=5):
    """Récupérer les derniers messages pour garder le contexte"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message, response FROM chat_memory WHERE user = ? ORDER BY timestamp DESC LIMIT ?", (user, limit))
    messages = cursor.fetchall()
    conn.close()
    
    return [{"role": "user", "content": msg[0]}, {"role": "assistant", "content": msg[1]}] for msg in messages[::-1]]

# Initialisation au démarrage
init_db()
