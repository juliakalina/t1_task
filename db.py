import psycopg2
from psycopg2 import sql
import json

def get_connection(dbname):
    try:
        return psycopg2.connect(
            dbname=dbname,
            user='admin',
            password='supersecuritypassword',
            host='postgres_db',
            port='5432'
        )
    except psycopg2.OperationalError as e:
        print(f"Failed to connect to the database {dbname}: {e}")
        exit(1)

def create_database():
    conn = get_connection('main_database')
    conn.autocommit = True
    with conn.cursor() as cur:
        try:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('appsec_db')
            ))
            print("Database created successfully")
        except psycopg2.errors.DuplicateDatabase:
            print("Database already exists")
    conn.close()

def create_table():
    with get_connection('appsec_db') as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS appsec (
                    name VARCHAR PRIMARY KEY NOT NULL,
                    description JSON NOT NULL
                );
            ''')
            print("Table created successfully")
        conn.commit()

def insert_data():
    practices = [
        ('practice_sast', {
            'name': 'Static Application Security Testing (SAST)',
            'description': 'Static Application Security Testing (SAST) is a testing methodology where the code is analyzed for vulnerabilities without executing the program.'
        }),
        ('practice_dast', {
            'name': 'Dynamic Application Security Testing (DAST)',
            'description': 'Dynamic Application Security Testing (DAST) is a testing methodology where the application is tested for vulnerabilities while it is running.'
        }),
        ('practice_iast', {
            'name': 'Interactive Application Security Testing (IAST)',
            'description': 'Interactive Application Security Testing (IAST) is a testing methodology that combines elements of SAST and DAST to identify vulnerabilities during runtime with more context about the application.'
        })
    ]

    with get_connection('appsec_db') as conn:
        with conn.cursor() as cur:
            for practice in practices:
                cur.execute(
                    "INSERT INTO appsec (name, description) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
                    (practice[0], json.dumps(practice[1]))
                )
            print("Data inserted successfully")
        conn.commit()

if __name__ == "__main__":
    create_database()
    create_table()
    insert_data()
