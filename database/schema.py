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
        ON DELETE CASCADE);

                         
    -- ==========================
    -- 6 General Form 
    -- ==========================
    CREATE TABLE IF NOT EXISTS general_form (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL ,
    year TEXT NOT NULL ,
    previous_balance REAL NOT NULL,
    paid_quotas INTEGER NOT NULL,
    tags INTEGER NOT NULL,
    UNIQUE(month, year)
                         
    
        );

    
        -- ==========================
    -- 7️⃣ Expense Form (reajustada)
    -- ==========================
    CREATE TABLE IF NOT EXISTS expense_form (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        year TEXT NOT NULL,
        description TEXT NOT NULL,
        value REAL NOT NULL CHECK(value >= 0),
        FOREIGN KEY (month, year) REFERENCES general_form(month, year)
            ON DELETE CASCADE
    );


        -- ==========================
    -- 8️⃣ Debit Houses
    -- ==========================
    CREATE TABLE IF NOT EXISTS debit_houses_form (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        house TEXT NOT NULL,               -- número ou identificação da casa
        month TEXT NOT NULL,               -- mês/ano do general_form
        year TEXT NOT NULL,
        debt_month TEXT NOT NULL,          -- mês de débito real
        debt_year TEXT NOT NULL,
        FOREIGN KEY (month, year) REFERENCES general_form(month, year)
            ON DELETE CASCADE
    );

    -- ==========================
    -- 9️⃣ House Payed
    -- ==========================
    CREATE TABLE IF NOT EXISTS house_payed_form (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        house TEXT NOT NULL,
        month TEXT NOT NULL,               -- mês/ano do general_form
        year TEXT NOT NULL,
        paid_month TEXT NOT NULL,          -- mês de pagamento real
        paid_year TEXT NOT NULL,
        FOREIGN KEY (month, year) REFERENCES general_form(month, year)
            ON DELETE CASCADE
    );

                         

    -- ==========================
    -- 9️⃣ Aux Form Management
    -- ==========================
    CREATE TABLE IF NOT EXISTS aux_form_management (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    role TEXT NOT NULL,
    name TEXT NOT NULL
    );
    
    -- ==========================
    -- 9️⃣ Aux Form Values
    -- ==========================
    CREATE TABLE IF NOT EXISTS aux_form_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_cota REAL NOT NULL,
    valor_cota_atrasada REAL NOT NULL,
    valor_tag REAL NOT NULL

    
    );
                         

    


    """)

    add_columns_monthly_balance()
    conn.commit()
    conn.close()


def add_columns_monthly_balance():
    conn = get_connection()
    cursor = conn.cursor()

    # Adiciona colunas apenas se não existirem
    try:
        cursor.execute("ALTER TABLE monthly_balance ADD COLUMN total_income REAL DEFAULT 0;")
    except Exception:
        pass  # ignora se já existir

    try:
        cursor.execute("ALTER TABLE monthly_balance ADD COLUMN total_expense REAL DEFAULT 0;")
    except Exception:
        pass

    try:
        cursor.execute("ALTER TABLE monthly_balance ADD COLUMN current_balance REAL DEFAULT 0;")
    except Exception:
        pass

    conn.commit()
    conn.close()
