from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session
from database.connection import get_connection
from dateutil.relativedelta import relativedelta
import sqlite3


from flask import session


general_info_bp = Blueprint("general_info_bp", __name__)

@general_info_bp.route("/general_info", methods=["GET", "POST"])
def general_info():
    # Valores padrão para preencher o formulário
    if "month" not in session or "year" not in session:
        hoje = datetime.now()
        session["month"] = hoje.month
        session["year"] = hoje.year
    valor_anterior = 0  # pode deixar 0 ou pegar do banco se quiser

    if request.method == "POST":
        session["month"] = request.form.get("month")
        session["year"] = request.form.get("year")
        previus_balance = float(request.form.get("previus_balance", 0))
        paid_quotas = int(request.form.get("paid_quotas", 0))
        tags = int(request.form.get("tags", 0))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO general_form (month, year, previous_balance, paid_quotas, tags)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(month, year)
            DO UPDATE SET
                previous_balance=excluded.previous_balance,
                paid_quotas=excluded.paid_quotas,
                tags=excluded.tags
""", (session["month"], session["year"], previus_balance, paid_quotas, tags))

        conn.commit()
        conn.close()

        return redirect(url_for("general_info_bp.expense_form", month=session["month"], year=session["year"]))
    
    

    return render_template(
        "general_info.html",
        mes_atual=session["month"],
        ano_atual=session["year"],
        valor_anterior=valor_anterior
    )

@general_info_bp.route("/expense_form", methods=["GET", "POST"])
def expense_form():
    month = session.get("month")
    year = session.get("year")

    conn = get_connection()
    cursor = conn.cursor()

    # Pega informações do mês
    cursor.execute("SELECT * FROM general_form WHERE month=? AND year=?", (month, year))
    info = cursor.fetchone()

    if "current_expenses" not in session:
        # Puxa todas as despesas do banco e coloca na sessão
        cursor.execute("SELECT description, value FROM expense_form WHERE month=? AND year=?", (month, year))
        session["current_expenses"] = [{"description": d[0], "amount": d[1]} for d in cursor.fetchall()]

    expenses = session["current_expenses"]

    # Adicionar despesa na lista temporária
    if request.method == "POST" and request.form.get("add_expense"):
        description = request.form.get("description")
        amount = float(request.form.get("amount", 0))
        expenses.append({"description": description, "amount": amount})
        session["current_expenses"] = expenses
        return redirect(url_for("general_info_bp.expense_form", month=month, year=year))

    # Deletar despesa da lista
    if request.method == "POST" and request.form.get("delete_index") is not None:
        index = int(request.form.get("delete_index"))
        if 0 <= index < len(expenses):
            expenses.pop(index)
            session["current_expenses"] = expenses
        return redirect(url_for("general_info_bp.expense_form", month=month, year=year))

    # Salvar tudo no banco
    if request.method == "POST" and request.form.get("save_all"):
        # Deleta todas as despesas antigas
        cursor.execute("DELETE FROM expense_form WHERE month=? AND year=?", (month, year))
        # Insere todas as despesas da lista
        for e in expenses:
            cursor.execute(
                "INSERT INTO expense_form (description, value, month, year) VALUES (?, ?, ?, ?)",
                (e["description"], e["amount"], month, year)
            )
        conn.commit()
        session.pop("current_expenses")
        return redirect(url_for("general_info_bp.debit_houses_form", month=month, year=year))

    conn.close()

    return render_template(
        "expense_form.html",
        info=info,
        expenses=expenses,
        month=month,
        year=year
    )


@general_info_bp.route("/debit_houses_form", methods=["GET", "POST"])
def debit_houses_form():
    month = session.get("month")
    year = session.get("year")

    conn = get_connection()
    cursor = conn.cursor()

    # Info do mês atual
    cursor.execute("SELECT * FROM general_form WHERE month=? AND year=?", (month, year))
    info = cursor.fetchone()

    # Mês/ano anterior
    mes_ano_atual = datetime(year=int(year), month=int(month), day=1)
    mes_ano_anterior = mes_ano_atual - relativedelta(months=1)
    mes_anterior = str(mes_ano_anterior.month)
    ano_anterior = str(mes_ano_anterior.year)

    # Inicializa sessão
    if "current_debits" not in session:
        cursor.execute(
            "SELECT id, house, debt_month, debt_year FROM debit_houses_form "
            "WHERE (month=? AND year=?) OR (month=? AND year=?)",
            (mes_anterior, ano_anterior, month, year)
        )
        all_debits = [
            {"id": d[0], "house": d[1], "debt_month": d[2], "debt_year": d[3]}
            for d in cursor.fetchall()
        ]

        # Deduplica
        seen = set()
        merged_debits = []
        for d in all_debits:
            key = (d["house"], d["debt_month"], d["debt_year"])
            if key not in seen:
                merged_debits.append(d)
                seen.add(key)

        session["current_debits"] = merged_debits

    debits = session["current_debits"]

    # Adicionar casa
    if request.method == "POST" and request.form.get("add_debit"):
        house = request.form.get("house")
        debt_month = request.form.get("debt_month")
        debt_year = request.form.get("debt_year")

        key = (house, debt_month, debt_year)
        if not any((d["house"], d["debt_month"], d["debt_year"]) == key for d in debits):
            debits.append({"house": house, "debt_month": debt_month, "debt_year": debt_year})
            session["current_debits"] = debits
            session.modified = True

        # renderiza de volta com a lista atualizada
        return render_template(
            "debit_houses_form.html",
            info=info,
            debits=debits,
            month=month,
            year=year,
            mes_anterior=mes_anterior,
            ano_anterior=ano_anterior
        )

    # Deletar casa
    if request.method == "POST" and request.form.get("delete_index") is not None:
        index = int(request.form.get("delete_index"))
        if 0 <= index < len(debits):
            debits.pop(index)
            session["current_debits"] = debits
            session.modified = True
        return render_template(
            "debit_houses_form.html",
            info=info,
            debits=debits,
            month=month,
            year=year,
            mes_anterior=mes_anterior,
            ano_anterior=ano_anterior
        )

    # Salvar no banco
    if request.method == "POST" and request.form.get("save_all"):
        cursor.execute("DELETE FROM debit_houses_form WHERE month=? AND year=?", (month, year))
        for d in debits:
            cursor.execute(
                "INSERT INTO debit_houses_form (house, month, year, debt_month, debt_year) VALUES (?, ?, ?, ?, ?)",
                (d["house"], month, year, d["debt_month"], d["debt_year"])
            )
        conn.commit()
        session.pop("current_debits")
        return redirect(url_for("general_info_bp.house_payed_form", month=month, year=year))

    conn.close()
    return render_template(
        "debit_houses_form.html",
        info=info,
        debits=debits,
        month=month,
        year=year,
        mes_anterior=mes_anterior,
        ano_anterior=ano_anterior
    )




@general_info_bp.route("/house_payed_form", methods=["GET", "POST"])
def house_payed_form():
    
    
    # Pega mês e ano do query param ou define padrão
    month = session.get("month")
    year = session.get("year")
    print(f"House Payed Form - Month: {month}, Year: {year}")
    conn = get_connection()
    cursor = conn.cursor()
     # Info do mês atual
    cursor.execute("SELECT * FROM general_form WHERE month=? AND year=?", (month, year))
    info = cursor.fetchone()

    # Inicializa lista na sessão se não existir
    if "current_paid_houses" not in session:
        session["current_paid_houses"] = []

    paid_houses = session["current_paid_houses"]

    if request.method == "POST":
        print("Form submitted with data:", request.form)

        # Adicionar casa: check for the submit button name instead of relying on value
        if "add_paid_house" in request.form:
            print("Adding paid house...")
            house = (request.form.get("house") or "").strip()

            # Safe parsing with fallbacks to current month/year when values are missing or invalid
            try:
                paid_month = int(request.form.get("paid_month") or month)
            except (TypeError, ValueError):
                paid_month = month

            try:
                paid_year = int(request.form.get("paid_year") or year)
            except (TypeError, ValueError):
                paid_year = year

            if house:
                # Evita duplicatas: mesma casa, mês e ano
                duplicate = any(
                    (d.get("house", "").strip().lower() == house.lower()
                     and int(d.get("paid_month") or 0) == paid_month
                     and int(d.get("paid_year") or 0) == paid_year)
                    for d in paid_houses
                )

                if duplicate:
                    print("Duplicate paid house found; skipping add")
                else:
                    paid_houses.append({
                        "house": house,
                        "paid_month": paid_month,
                        "paid_year": paid_year
                    })
                    session["current_paid_houses"] = paid_houses
                    session.modified = True  # garante que a sessão seja salva
                    print("Paid Houses:", paid_houses)
            else:
                print("No house name provided; skipping add")

            # Redireciona para GET para evitar duplicação de POST
            return redirect(url_for("general_info_bp.house_payed_form", month=month, year=year))

        # Deletar casa
        if "delete_index" in request.form:
            try:
                index = int(request.form.get("delete_index"))
            except (TypeError, ValueError):
                index = None

            if index is not None and 0 <= index < len(paid_houses):
                paid_houses.pop(index)
                session["current_paid_houses"] = paid_houses
                session.modified = True
            return redirect(url_for("general_info_bp.house_payed_form", month=month, year=year))

        # Salvar no banco: persiste `current_paid_houses` em `house_payed_form`
        if "save_all" in request.form:
            

            # Remove registros antigos para o mês/ano atual
            cursor.execute("DELETE FROM house_payed_form WHERE month=? AND year=?", (str(month), str(year)))

            # Insere os valores atuais
            for d in paid_houses:
                cursor.execute(
                    "INSERT INTO house_payed_form (house, month, year, paid_month, paid_year) VALUES (?, ?, ?, ?, ?)",
                    (d.get("house"), str(month), str(year), str(d.get("paid_month")), str(d.get("paid_year")))
                )

            conn.commit()
            conn.close()

            # limpa sessão e redireciona
            session.pop("current_paid_houses", None)
            return redirect(url_for("general_info_bp.aux_form", month=month, year=year))

    # GET inicial ou após redirect
    return render_template(
        "house_payed_form.html",
        paid_houses=paid_houses,
        month=month,
        year=year,
        total_casas=len(paid_houses),
        info=info
    )


@general_info_bp.route("/aux_form", methods=["GET", "POST"])
def aux_form():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    month = session.get("month")
    year = session.get("year")
    cursor.execute("SELECT * FROM general_form WHERE month=? AND year=?", (month, year))
    info = cursor.fetchone()

    # =========================
    # POST (SALVAR)
    # =========================
    if request.method == "POST":

        # ---------- VALUES ----------
        cursor.execute("SELECT * FROM aux_form_values")
        values_exists = cursor.fetchone()

        if values_exists:
            cursor.execute("""
                UPDATE aux_form_values
                SET valor_cota=?,
                    valor_cota_atrasada=?,
                    valor_tag=?
            """, (
                request.form.get("valor_cota"),
                request.form.get("valor_cota_atrasada"),
                request.form.get("valor_tag"),
            ))
        else:
            cursor.execute("""
                INSERT INTO aux_form_values
                (valor_cota, valor_cota_atrasada, valor_tag)
                VALUES (?, ?, ?)
            """, (
                request.form.get("valor_cota"),
                request.form.get("valor_cota_atrasada"),
                request.form.get("valor_tag"),
            ))

        # ---------- MANAGEMENT ----------
        roles = ["Sindico", "Presidente", "Conselheiro 1", "Conselheiro 2"]

        for role in roles:
            name = request.form.get(role)

            cursor.execute("SELECT * FROM aux_form_management WHERE role=?", (role,))
            exists = cursor.fetchone()

            if exists:
                cursor.execute("""
                    UPDATE aux_form_management
                    SET name=?
                    WHERE role=?
                """, (name, role))
            else:
                cursor.execute("""
                    INSERT INTO aux_form_management (role, name)
                    VALUES (?, ?)
                """, (role, name))

        conn.commit()
        conn.close()

        return redirect(url_for("general_info_bp.general_info"))


    # =========================
    # GET (BUSCAR DADOS)
    # =========================

    # Buscar valores
    cursor.execute("SELECT * FROM aux_form_values")
    values_data = cursor.fetchone()

    # Se não existir, criar dicionário vazio
    if not values_data:
        values_data = {
            "valor_cota": "",
            "valor_cota_atrasada": "",
            "valor_tag": ""
        }

    # Buscar cargos
    cursor.execute("SELECT role, name FROM aux_form_management")
    management_rows = cursor.fetchall()

    management_data = {
        "Sindico": "",
        "Presidente": "",
        "Conselheiro 1": "",
        "Conselheiro 2": ""
    }

    for row in management_rows:
        management_data[row["role"]] = row["name"]

    conn.close()

    return render_template(
        "aux_form.html",
        values=values_data,
        management=management_data,
        info=info,
        month=month,
        year=year
    
    )