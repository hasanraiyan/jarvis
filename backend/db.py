import csv
import sqlite3

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)
query = "CREATE TABLE IF NOT EXISTS chat_history(id integer primary key, user_message TEXT, ai_response TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
cursor.execute(query)
query = "CREATE TABLE IF NOT EXISTS face_auth(id integer primary key, user_id INTEGER DEFAULT 1, is_setup BOOLEAN DEFAULT 0, setup_date DATETIME DEFAULT CURRENT_TIMESTAMP)"
cursor.execute(query)
conn.commit()


# query = "INSERT INTO sys_command VALUES (null,'obs', 'C:\\Program Files\\obs-studio\\bin\\obs64.exe')"
# cursor.execute(query)
# conn.commit()

# query = "DELETE FROM sys_command WHERE name='obs'"
# cursor.execute(query)
# conn.commit()

# testing module
# app_name = "obs"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])




# cursor.execute("DROP TABLE IF EXISTS contacts;")
# conn.commit()
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name VARCHAR(200), Phone VARCHAR(255), email VARCHAR(255) NULL)''') 

 
# desired_columns_indices = [0, 20]
 
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'Phone') VALUES (null, ?,? );''', tuple(selected_data))

# # Commit changes and close connection
# conn.commit()
# conn.close()

# print("Data inserted successfully") 


# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# cursor.execute(query)
# conn.commit() 


# query = 'Ankit'
# query = query.strip().lower()  # Added parentheses to call the method

# cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
#                ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])
#
# Chat history functions
def save_chat_message(user_message, ai_response):
    """Save a chat conversation to the database"""
    try:
        cursor.execute("INSERT INTO chat_history (user_message, ai_response) VALUES (?, ?)", 
                      (user_message, ai_response))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving chat message: {e}")
        return False

def get_chat_history(limit=50):
    """Retrieve chat history from the database"""
    try:
        cursor.execute("SELECT user_message, ai_response, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT ?", (limit,))
        results = cursor.fetchall()
        # Reverse to show oldest first
        return list(reversed(results))
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []

def clear_chat_history():
    """Clear all chat history"""
    try:
        cursor.execute("DELETE FROM chat_history")
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        return False
def get_recent_chat_context(limit=5):
    """Get recent chat history formatted for AI context"""
    try:
        cursor.execute("SELECT user_message, ai_response FROM chat_history ORDER BY timestamp DESC LIMIT ?", (limit,))
        results = cursor.fetchall()
        # Reverse to show oldest first for proper context
        return list(reversed(results))
    except Exception as e:
        print(f"Error retrieving chat context: {e}")
        return []

# Face authentication functions
def is_face_setup():
    """Check if face authentication is already set up"""
    try:
        cursor.execute("SELECT is_setup FROM face_auth WHERE user_id = 1")
        result = cursor.fetchone()
        return result[0] if result else False
    except Exception as e:
        print(f"Error checking face setup: {e}")
        return False

def mark_face_setup_complete():
    """Mark face authentication as set up"""
    try:
        cursor.execute("INSERT OR REPLACE INTO face_auth (user_id, is_setup) VALUES (1, 1)")
        conn.commit()
        return True
    except Exception as e:
        print(f"Error marking face setup complete: {e}")
        return False

def reset_face_setup():
    """Reset face authentication setup"""
    try:
        cursor.execute("UPDATE face_auth SET is_setup = 0 WHERE user_id = 1")
        conn.commit()
        return True
    except Exception as e:
        print(f"Error resetting face setup: {e}")
        return False