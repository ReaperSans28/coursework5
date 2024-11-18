from src.config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.working_with_files import create_database, save_to_database


def main():
    company_ids = [
        "2144643",
        "9498120",
        "10011655",
        "1426733",
        "5486964",
        "9162108",
        "4306244",
        "1060821",
        "3078521",
        "10819001",
    ]

    params = config()
    vacancies = HeadHunterAPI(company_ids)

    if vacancies.get_vacancies() != [[]]:
        user_input = input("Введите ключевое слово для поиска вакансий: ")

        create_database("HHApi", params)

        for vacancy in vacancies.get_vacancies()[0]:
            vac = Vacancy(vacancy)
            save_to_database("HHApi", vac, params)

        dbmanager = DBManager("HHApi", params)
        companies_and_vacancies_count = dbmanager.get_companies_and_vacancies_count()
        all_vacancies = dbmanager.get_all_vacancies()
        avg_salary = dbmanager.get_avg_salary()
        vacancies_with_higher_salary = dbmanager.get_vacancies_with_higher_salary()
        vacancies_with_keyword = dbmanager.get_vacancies_with_keyword(user_input)

        print(
            f"""
            Компании и их количество вакансий: {companies_and_vacancies_count}
            Все вакансии: {all_vacancies}
            Средняя зарплата по вакансиям: {avg_salary}
            Вакансии с зарплатой выше среднего: {vacancies_with_higher_salary}
            Вакансии с ключевым словом в названии {vacancies_with_keyword}"""
        )


if __name__ == "__main__":
    main()
