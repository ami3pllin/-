#database.py
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Request:
    def __init__(self, id, client_name, client_email, client_phone, service, item, description, status):
        self.id = id
        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone
        self.service = service
        self.item = item
        self.description = description
        self.status = status

class Employee:
    def __init__(self, id, code):
        self.id = id
        self.code = code

class DatabaseManager:
    def __init__(self, database_name='application_database.db'):
        self.init_db(database_name)

    def init_db(self, database_name):
        self.connection = sqlite3.connect(database_name, check_same_thread=False, isolation_level=None)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA synchronous=OFF")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_requests_table()
        self.create_employees_table()

    def create_requests_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                client_email TEXT,
                client_phone TEXT,
                service TEXT,
                item TEXT,
                description TEXT,
                status TEXT
            )
        """)
        self.connection.commit()

    def create_employees_table(self):
        with self.connection:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE
                )
            ''')

    def insert_employee(self, code):
        with self.connection:
            self.cursor.execute('''
                INSERT INTO employees (code)
                VALUES (?)
            ''', (code,))

    def get_all_employees(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM employees")
            rows = self.cursor.fetchall()
            employees = [Employee(*row) for row in rows]
            return employees

    def check_employee_code(self, employee_code):
        with self.connection:
            self.cursor.execute("SELECT * FROM employees WHERE code=?", (employee_code,))
            result = self.cursor.fetchone()
            return result is not None

    def insert_request(self, client_name, client_email, client_phone, service, item, description, status='Pending'):
        with self.connection:
            self.cursor.execute('''
                INSERT INTO requests (client_name, client_email, client_phone, service, item, description, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (client_name, client_email, client_phone, service, item, description, status))

    def get_all_requests(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM requests")
            rows = self.cursor.fetchall()
            requests = [Request(*row) for row in rows]
            return requests

    def update_request_status(self, request_id, status):
        with self.connection:
            self.cursor.execute("UPDATE requests SET status=? WHERE id=?", (status, request_id))

    def send_email(self, my_email, password, you_email, subject, message):
        try:
            server = smtplib.SMTP('smtp.mail.ru', 587)
            server.starttls()
            server.login(my_email, password)

            msg = MIMEMultipart()
            msg['From'] = my_email
            msg['To'] = you_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            server.send_message(msg)
            print('Сообщение успешно отправлено')
        except smtplib.SMTPException as e:
            print(f'Ошибка при отправке сообщения: {str(e)}')
        finally:
            server.quit()

    def send_email_notification(self, client_email, status):
        my_email = 'repairshop05@mail.ru'
        password = 'NXxj4sFnvSpN8TrzzQ5n'

        subject = 'Статус заявки'
        if status == 'Accepted':
            message = (
                'Добрый день! Ваша заявка на ремонт одобрена. Ждем вас по адресу г. Москва Волгоградский проспект 43с1Д '
                'с 10:00 до 20:00. Там наши сотрудники проведут диагностику вашей техники и укажут точную цену за ремонт. '
                'Спасибо, что выбрали нас.'
            )
        elif status == 'Rejected':
            message = (
                'Добрый день! К сожалению, ваша заявка на ремонт была отклонена в связи с рабочими обстоятельствами. '
                'Пожалуйста, обратитесь снова, если у вас возникнут проблемы. Спасибо за понимание.'
            )
        else:
            return

        self.send_email(my_email, password, client_email, subject, message)


    def delete_request(self, request_id):
        with self.connection:
            self.cursor.execute("DELETE FROM requests WHERE id=?", (request_id,))

    def check_employee_code(self, employee_code):
        with self.connection:
            self.cursor.execute("SELECT * FROM employees WHERE code=?", (employee_code,))
            result = self.cursor.fetchone()
            return result is not None

    def get_employee_requests(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM requests")
            rows = self.cursor.fetchall()
            requests = [Request(*row) for row in rows]
            return requests

    def get_client_email_by_request_id(self, request_id):
        with self.connection:
            self.cursor.execute("SELECT client_email FROM requests WHERE id=?", (request_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None

if __name__ == "__main__":

    db_manager = DatabaseManager()
    employee_codes = ['136', '666', '111']
    for code in employee_codes:
        db_manager.insert_employee(code)
