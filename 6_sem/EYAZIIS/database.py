import sqlite3
from datetime import datetime
import uuid

def init_db():
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS application_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id TEXT,
                  user_query TEXT,
                  gpt_response TEXT,
                  model TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS document_store
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_message(session_id, user_query, gpt_response, model):
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO application_logs (session_id, user_query, gpt_response, model) VALUES (?, ?, ?, ?)',
              (session_id, user_query, gpt_response, model))
    message_id = c.lastrowid
    conn.commit()
    conn.close()
    return message_id

def get_chat_history(session_id):
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    history = [{"role": "user", "content": row[0]} if row[0] else {"role": "assistant", "content": row[1]} for row in c.fetchall()]
    conn.close()
    return history

def delete_message(message_id):
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('DELETE FROM application_logs WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def add_document(filename):
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO document_store (filename) VALUES (?)', (filename,))
    doc_id = c.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def delete_document(doc_id):
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('DELETE FROM document_store WHERE id = ?', (doc_id,))
    conn.commit()
    conn.close()

def get_sessions():
    conn = sqlite3.connect('rag_app.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT session_id FROM application_logs')
    sessions = [row[0] for row in c.fetchall()]
    conn.close()
    return sessions
