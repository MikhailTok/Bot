import sqlite3

def create_database():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY,
              user_id INTERGER,
              ip TEXT,
              question TEXT NOT NULL,
              answer TEXT,
              date datetime default current_timestamp)''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()