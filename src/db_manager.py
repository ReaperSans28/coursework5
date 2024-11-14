import psycopg2


class DBManager:
    """
    Класс, который будет подключаться к базе данных PostgreSQL.
    """

    def __init__(self, database, user, password, host):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute(
            """SELECT e.company_name, COUNT(v.vacancy_name) FROM employers e
                        JOIN vacancies v USING(company_id) GROUP BY company_name;"""
        )

        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute(
            """SELECT e.company_name, v.vacancy_name, v.salary, v.url FROM employers e
                        JOIN vacancies v USING(company_id);"""
        )

        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("SELECT AVG(salary) FROM vacancies;")
        return float(self.cur.fetchall()[0][0])

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("SELECT * FROM vacancies WHERE salary > %s;", (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute(
            f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%';"
        )
        return self.cur.fetchall()
