from database.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    
    -- ==========================
    -- 1️⃣ Monthly Balance
    -- ==========================
    CREATE TABLE IF NOT EXISTS monthly_balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL UNIQUE,              
        previous_balance REAL NOT NULL,
        paid_quotas INTEGER NOT NULL CHECK(paid_quotas >= 0),
        paid_with_fine INTEGER NOT NULL CHECK(paid_with_fine >= 0),
        tags INTEGER NOT NULL CHECK(tags >= 0)
    );


    -- ==========================
    -- 2️⃣ Income
    -- ==========================
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        FOREIGN KEY (month) REFERENCES monthly_balance(month)
            ON DELETE CASCADE
    );


    -- ==========================
    -- 3️⃣ Expense
    -- ==========================
    CREATE TABLE IF NOT EXISTS expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        FOREIGN KEY (month) REFERENCES monthly_balance(month)
            ON DELETE CASCADE
    );


    -- ==========================
    -- 4️⃣ Arrears (Casas com débito atual)
    -- ==========================
    CREATE TABLE IF NOT EXISTS arrears (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    house_number INTEGER NOT NULL,
    reference_month INTEGER NOT NULL,
    reference_year INTEGER NOT NULL,

    FOREIGN KEY (month) REFERENCES monthly_balance(month)
        ON DELETE CASCADE,

    UNIQUE(house_number, reference_month, reference_year,month)
);



    -- ==========================
    -- 5️⃣ Management (Histórico de gestão)
    -- ==========================
    CREATE TABLE IF NOT EXISTS management (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    role TEXT NOT NULL,
    name TEXT NOT NULL,

    FOREIGN KEY (month) REFERENCES monthly_balance(month)
        ON DELETE CASCADE
);


    """)

    conn.commit()
    conn.close()
