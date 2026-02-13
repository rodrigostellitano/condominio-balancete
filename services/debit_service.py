

from models.models import DebitResult

# services/debit_service.py

class DebitService:

    
    def extract_house_payed(self,df):
        df_pago = df[["Cotas Atrasadas Pagas", "Mes Atrasado", "Ano Atrasado"]].dropna()

        MESES_ABREV = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
            5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
            9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }

        resultado = []

        for casa, grupo in df_pago.groupby("Cotas Atrasadas Pagas"):
            anos = {}

            for _, row in grupo.iterrows():
                ano = int(row["Ano Atrasado"])
                mes = int(row["Mes Atrasado"])
                anos.setdefault(ano, []).append(mes)

            partes = []
            for ano, meses in sorted(anos.items()):
                meses_ordenados = sorted(meses)
                meses_txt = "/".join(MESES_ABREV[m] for m in meses_ordenados)
                partes.append(f"{meses_txt}/{str(ano)[-2:]}")

            resultado.append(f" {int(casa):02d}({' | '.join(partes)})")

        print(resultado)
        
        return resultado




    def extract_house_debit(self,df):
        df_debito = df[["Casas com debito", "Mes", "Ano"]].dropna()

        MESES_ABREV = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
            5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
            9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }

        total_casas_em_debito = len(df_debito["Casas com debito"])
        print("Total casas em debito:", total_casas_em_debito)
        resultado = []

        for casa, grupo in df_debito.groupby("Casas com debito"):
            anos = {}

            for _, row in grupo.iterrows():
                ano = int(row["Ano"])
                mes = int(row["Mes"])
                anos.setdefault(ano, []).append(mes)

            partes = []
            for ano, meses in sorted(anos.items()):
                meses_ordenados = sorted(meses)
                meses_txt = "/".join(MESES_ABREV[m] for m in meses_ordenados)
                partes.append(f"{meses_txt}/{str(ano)[-2:]}")

            resultado.append(f"Casa {int(casa):02d} ({' | '.join(partes)})")

        return DebitResult(
                    houses_debit=resultado,
                    total_houses_debit=total_casas_em_debito
                )