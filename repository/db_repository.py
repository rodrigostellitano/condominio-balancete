from database.connection import get_connection
import re

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



def save_month_data(data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Garante que month é string
    month = str(data["month"])

    # 2️⃣ Converte valores do monthly_balance para tipos corretos
    previous_balance = float(str(data["previous_balance"]).replace(",", "."))
    paid_quotas = int(data["paid_quotas"])
    paid_with_fine = int(data["paid_with_fine"])
    tags = int(data["tags"])
    total_income = float(str(data["total_income"]).replace(",", "."))
    total_expense = float(str(data["total_expense"]).replace(",", "."))
    current_balance = float(str(data["current_balance"]).replace(",", "."))

    # 3️⃣ Delete mês existente
    cursor.execute(
        "DELETE FROM monthly_balance WHERE month = ?",
        (month,)
    )

    # 4️⃣ Insert monthly_balance
    cursor.execute("""
    INSERT INTO monthly_balance
    (month, previous_balance, paid_quotas, paid_with_fine, tags, total_income, total_expense, current_balance)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    month,
    previous_balance,
    paid_quotas,
    paid_with_fine,
    tags,
    total_income,      # valor já calculado no app
    total_expense,     # valor já calculado no app
    current_balance    # valor já calculado no app
))


    # 5️⃣ Insert incomes
    incomes_data = data.get("incomes", [])

    if isinstance(incomes_data, dict):
        # transforma todo dict em lista de dicts automaticamente
        incomes_list = [{"description": key, "amount": value} for key, value in incomes_data.items()]
    else:
        incomes_list = incomes_data  # já é lista de dicts

    # Insere no banco
    for income in incomes_list:
        description = str(income["description"])
        amount = float(str(income["amount"]).replace(",", "."))
        cursor.execute(
            "INSERT INTO income (month, description, amount) VALUES (?, ?, ?)",
            (month, description, amount)
        )

    
    # 6️⃣ Insert expenses
    expenses_data = data.get("expenses", [])

    # Se for dict, transforma em lista de dicts automaticamente
    if isinstance(expenses_data, dict):
        expenses_list = [{"description": key, "amount": value} for key, value in expenses_data.items()]
    else:
        expenses_list = expenses_data  # já é lista de dicts

    # Insere no banco
    for expense in expenses_list:
        description = str(expense["description"])
        amount = float(str(expense["amount"]).replace(",", "."))
        cursor.execute(
            "INSERT INTO expense (month, description, amount) VALUES (?, ?, ?)",
            (month, description, amount)
        )


    # 7️⃣ Insert arrears
    

    # df_debito já vem do seu extract, contendo ["Casas com debito", "Mes", "Ano"]
    arrears_list = []
    df_arrears = data["arrears"]

    for _, row in df_arrears.iterrows():
        arrears_list.append({
            "house_number": int(row["Casas com debito"]),
            "reference_month": int(row["Mes"]),
            "reference_year": int(row["Ano"])
        })

    # Inserção no banco
    for arrear in arrears_list:
        cursor.execute(
            "INSERT INTO arrears (month, house_number, reference_month, reference_year) VALUES (?, ?, ?, ?)",
            (month, arrear["house_number"], arrear["reference_month"], arrear["reference_year"])
        )



    # 8️⃣ Insert management
    for manager in data.get("management", []):
        role = str(manager["role"])
        name = str(manager["name"])
        cursor.execute(
            "INSERT INTO management (month, role, name) VALUES (?, ?, ?)",
            (month, role, name)
        )

    # 9️⃣ Commit e close
    conn.commit()
    conn.close()
