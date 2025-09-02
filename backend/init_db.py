# Optional standalone initializer (not strictly required because main.py calls init_db())
import sqlite3, os
def init_db():
    DB_PATH = os.getenv("DB_PATH", "expenses.db")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL,
        category TEXT,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        note TEXT,
        currency TEXT DEFAULT 'USD',
        ts_utc TEXT NOT NULL
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    emoji TEXT
    );
                """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS category_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    UNIQUE (category_id, keyword),
    FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
    );
                """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_user_ts ON expenses(user_id, ts_utc);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_category_id ON expenses(category_id);")
    conn.commit()
    conn.close()
    print("SQLite DB initialized at", DB_PATH)