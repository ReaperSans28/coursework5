import psycopg2
from psycopg2 import sql


def create_database(database, params):
    """
    Функция для создания таблицы.
    """
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.set_client_encoding("UTF8")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(database)))
    cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(database)))

    cur.close()
    conn.close()

    with psycopg2.connect(dbname=database, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE employers (
                    company_id INTEGER PRIMARY KEY,
                    company_name TEXT NOT NULL);"""
            )

            cur.execute(
                """CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR,
                        salary NUMERIC,
                        company_id INTEGER REFERENCES employers(company_id),
                        url VARCHAR);"""
            )
            conn.commit()
    return None


def save_to_database(database, vacancy, params):
    """
    Функция для добавления значений в таблицу.
    """
    with psycopg2.connect(dbname=database, **params) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employers (company_id, company_name) VALUES (%s, %s);
            """,
                (vacancy.employer_id, vacancy.employer_name),
            )

            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, salary, company_id, url) VALUES (%s, %s, %s, %s, %s);
            """,
                (
                    vacancy.id,
                    vacancy.name,
                    vacancy.salary,
                    vacancy.employer_id,
                    vacancy.url,
                ),
            )
