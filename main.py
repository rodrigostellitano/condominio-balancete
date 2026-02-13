
from pydoc import doc




from repository.excel_repository import ExcelRepository
from services.finance_service import FinanceService
from utils.date_utils import Utils
from services.debit_service import DebitService
from services.people_service import PeopleService
from reports.report_generator import ReportGenerator


def main():
    
    repository = ExcelRepository()
    finance = FinanceService()
    debit = DebitService()
    utility = Utils()
    people = PeopleService()
    report = ReportGenerator()
    
    df, df_aux = repository.load()
   
    entrance = finance.calculate_entrace(df, df_aux)

    exit_result = finance.calculate_exit(df)
    
    date = utility.ajust_date(entrance.current_month)
    
    df_names = people.extract_names(df_aux)
    
    total = finance.calculate_total(
        entrance.previous_value,
        entrance.total,
        exit_result.total
    )
    
    debit_result  = debit.extract_house_debit(df)
    houses_paid = debit.extract_house_payed(df)

    print("Date:", date)
    print("Previous Month Entrace:", entrance.previous_value)
    print("Total Entrace:", entrance.total)
    print("Details Entrace:", entrance.details)
    print("Result Exit:", exit_result.total)
    print("Details Exit:", exit_result.details)
    print(df_names)
    print("Total Final:", total)
    print("Houses with debit:", debit_result.houses_debit)
    print("Total Houses with debit:", debit_result.total_houses_debit)

    file = report.generate_report(
        date_info=date,
        previous_month_value=entrance.previous_value,
        total_entrace=entrance.total,
        details_entrace=entrance.details,
        total_exit=exit_result.total,
        details_exit=exit_result.details,
        houses_debit=debit_result.houses_debit,
        total_casas_em_debito=debit_result.total_houses_debit,
        people=df_names,
        total_final=total,
        houses_paid=houses_paid
    )



if __name__ == "__main__":
    main()