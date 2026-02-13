

#service/people_service.py
import pandas as pd

class PeopleService:

    

    def extract_names(self,df_aux: pd.DataFrame) -> dict:

        df_aux = df_aux[["Titulo", "Info"]].dropna()
        names = dict(zip(df_aux["Titulo"], df_aux["Info"]))
        sindico = names.get("Sindico", 0)
        president = names.get("Presidente", 0)
        cons_1 = names.get("Cons Fiscal 1", 0)
        cons_2 = names.get("Cons Fiscal 2", 0)
        
        
        return {
            "Síndico": sindico,
            "Presidente": president,
            "Fiscal 1": cons_1,
            "Fiscal 2": cons_2,
        }
