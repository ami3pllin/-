# email_manager.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt6.QtCore import QThread, pyqtSignal

class EmailThread(QThread):
    email_sent = pyqtSignal()

    def __init__(self, email_manager, you_email, subject, message):
        super().__init__()
        self.email_manager = email_manager
        self.you_email = you_email
        self.subject = subject
        self.message = message

    def run(self):
        try:
            print('Пытаюсь отправить электронное письмо...')
            self.email_manager.send_email(self.you_email, self.subject, self.message)
            print('Электронное письмо успешно отправлено')
            self.email_sent.emit()
        except Exception as e:
            print(f'Ошибка при отправке электронной почты: {str(e)}')

class EmailManager:
    def __init__(self):
        self.my_email = 'repairshop05@mail.ru'
        self.application_password = "nNXxj4sFnvSpN8TrzzQ5"

    def send_email(self, you_email, subject, message):
        try:
            # Используйте порт 465 для SSL/TLS
            server = smtplib.SMTP('smtp.mail.ru', 587)
            server.starttls()

            server.login(self.my_email, self.application_password)

            msg = MIMEMultipart()
            msg['From'] = self.my_email
            msg['To'] = you_email
            msg['Subject'] = subject

            # Добавляем текст сообщения
            msg.attach(MIMEText(message, 'plain', charset='utf-8'))

            # Отправляем сообщение
            server.sendmail(self.my_email, you_email, msg.as_bytes())
            print('Сообщение успешно отправлено')
        except smtplib.SMTPException as e:
            print(f'Ошибка при отправке сообщения: {str(e)}')
        except Exception as ex:
            print(f'Произошла непредвиденная ошибка: {str(ex)}')
        finally:
            server.quit()

    def send_email_notification(self, client_email, status):
        my_email = 'repairshop05@mail.ru'
        password = 'nNXxj4sFnvSpN8TrzzQ5'

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

if __name__ == "__main__":
    # Пример использования EmailManager для тестирования
    email_manager = EmailManager()
    email_thread = EmailThread(email_manager, 'test@example.com', 'Test Subject', 'Test Message')
    email_thread.email_sent.connect(lambda: print('Email Sent!'))
    email_thread.start()
