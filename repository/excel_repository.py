# repository/excel_repository.py

import pandas as pd
from typing import Tuple


class ExcelRepository:

    def load(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = pd.read_excel("templates/template.xlsx", sheet_name="Main")
        df_aux = pd.read_excel("templates/template.xlsx", sheet_name="Aux")
        return df, df_aux
