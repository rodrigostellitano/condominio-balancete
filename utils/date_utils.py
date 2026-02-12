class Utils:

    def ajust_date(self,current_month):
            MESES_PT = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro",
        }
            month, year = current_month.split("-")
            month = int(month)

            previus_month = month - 1
            
            if previus_month == 0:
                previus_month = 12
                previus_year = int(year) - 1
            else:
                previus_year = int(year)
            return {"Previus Month": MESES_PT[previus_month], "Previus Year": previus_year, "Current Month": MESES_PT[month], "Current Year": year}

