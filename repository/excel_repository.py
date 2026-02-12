# repository/excel_repository.py

import pandas as pd

class ExcelRepository:

    def load(self):
        df = pd.read_excel("templates/template.xlsx", sheet_name="Main")
        df_aux = pd.read_excel("templates/template.xlsx", sheet_name="Aux")
        return df, df_aux
