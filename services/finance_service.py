# services/finance_service.py
from models.models import EntranceResult, ExitResult

class FinanceService:

    
    def calculate_entrace(self,df, df_aux):
        # --- Quantidades (Main) ---
        entradas = dict(zip(df["Titulo"], df["Informacoes"]))

        value_previus_month = entradas.get("Valor do Mes anterior", 0)
        current_month = entradas.get("Mes Ano Atual", 0)

        qtd_cotas_pagas = entradas.get("Cotas", 0)
        qtd_cotas_pagas_multa = entradas.get("Cotas com Multa", 0)
        qtd_tag = entradas.get("Tag", 0)

        # --- Aux (chave → valor) ---
        aux = dict(zip(df_aux["Titulo"], df_aux["Info"]))
        #print(aux)
        valor_cota = aux.get("Valor da Cota", 0)
        #print(valor_cota)
        valor_cota_atrasada = aux.get("Valor da Cota atrasada", 0)
        #print(valor_cota_atrasada)
        valor_tag = aux.get("Valor Tag", 0)

        total_cotas = qtd_cotas_pagas * valor_cota
        total_cotas_multa = qtd_cotas_pagas_multa * valor_cota_atrasada
        total_tag = qtd_tag * valor_tag

        total_entrada = total_cotas + total_cotas_multa + total_tag

        return EntranceResult(
            previous_value=value_previus_month,
            current_month=current_month,
            total=total_entrada,
            details={
        "Total Cotas": total_cotas,
        "Qtd Cotas Pagas": qtd_cotas_pagas,
        "Qtd Cotas Pagas Multa": qtd_cotas_pagas_multa,
        "Qtd Tag": qtd_tag,
        "Total Cotas com Multa": total_cotas_multa,
        "Total Tag": total_tag,
    }
)



    def calculate_exit(self,df):

        df_saida = df[["Saida", "Valor"]].dropna()
        df_saida = dict(zip(df_saida["Saida"], df_saida["Valor"]))
        total_saida = sum(df_saida.values())


        

        return ExitResult(
                total=total_saida,
                details=df_saida
            )



    def calculate_total(self,value_previus_month,total_entrace,result_exit):
        return value_previus_month + total_entrace - result_exit
