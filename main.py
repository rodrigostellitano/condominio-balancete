from flask import Flask
from app.routes.general_info import general_info_bp
from database.schema import create_tables
import os  # Para gerar uma chave secreta segura

app = Flask(__name__, template_folder="templates")

# 🔹 ESSENCIAL: definir uma chave secreta para usar sessões
app.secret_key = os.urandom(24)  # ou coloque uma string fixa se quiser

# 🔹 Registrar blueprint
app.register_blueprint(general_info_bp)

if __name__ == "__main__":
    create_tables()  # garante que as tabelas existam antes de iniciar
    app.run(debug=True, host="0.0.0.0")
