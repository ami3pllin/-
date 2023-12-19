#windows.py

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, \
    QMainWindow, QListWidget, QTextEdit, QListWidgetItem, QMessageBox

from database import DatabaseManager

class UserTypeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.db_manager = DatabaseManager()

    def init_ui(self):
        layout = QVBoxLayout()

        self.user_type_label = QLabel('Выберите тип пользователя:')
        self.user_type_label.setFont(QFont('Arial', 20))
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItems(['Сотрудник', 'Клиент'])
        layout.addWidget(self.user_type_label)
        layout.addWidget(self.user_type_combo)

        self.next_button = QPushButton('Далее')
        self.next_button.setFont(QFont('Arial', 18))
        self.next_button.clicked.connect(self.open_next_window)
        layout.addWidget(self.next_button)

        self.setStyleSheet('''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding: 20px;
        ''')

        self.setLayout(layout)

    def open_next_window(self):
        selected_user_type = self.user_type_combo.currentText()
        if selected_user_type == 'Сотрудник':
            self.employee_login_window = EmployeeLoginWindow(self.db_manager)
            self.employee_login_window.show()
            self.close()
        elif selected_user_type == 'Клиент':
            self.client_window = ClientWindow(self.db_manager)
            self.client_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)  # Добавляем эту строку
            self.client_window.show()

class EmployeeLoginWindow(QWidget):
    def __init__(self, db_manager=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.employee_code_label = QLabel('Введите код сотрудника:')
        self.employee_code_label.setFont(QFont('Arial', 20))

        self.employee_code_edit = QLineEdit()
        layout.addWidget(self.employee_code_label)
        layout.addWidget(self.employee_code_edit)

        self.login_button = QPushButton('Войти')
        self.login_button.setFont(QFont('Arial', 20))
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setStyleSheet('''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding: 20px;
        ''')

        self.setLayout(layout)

    def login(self):
        employee_code = self.employee_code_edit.text()
        try:
            if self.db_manager.check_employee_code(employee_code):
                self.employee_main_window = EmployeeMainWindow(self.db_manager)
                self.employee_main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный код сотрудника')
        except Exception as e:
            print(f"An error occurred: {str(e)}")

class EmployeeMainWindow(QMainWindow):
    def __init__(self, db_manager=None):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle('Главное окно сотрудника')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout()

        self.requests_label = QLabel('Заявки:')
        self.requests_label.setFont(QFont('Arial', 20))
        self.central_layout.addWidget(self.requests_label)

        self.requests_list = QListWidget()
        self.central_layout.addWidget(self.requests_list)

        self.accept_button = QPushButton('Принять заявку')
        self.accept_button.setFont(QFont('Arial', 18))
        self.accept_button.clicked.connect(self.accept_request)
        self.central_layout.addWidget(self.accept_button)


        self.reject_button = QPushButton('Отклонить заявку')
        self.reject_button.setFont(QFont('Arial', 18))
        self.reject_button.clicked.connect(self.reject_request)
        self.central_layout.addWidget(self.reject_button)

        self.finish_button = QPushButton('Завершить работу')
        self.finish_button.setFont(QFont('Arial', 18))
        self.finish_button.clicked.connect(self.finish_work)
        self.central_layout.addWidget(self.finish_button)

        self.central_widget.setLayout(self.central_layout)

        self.update_requests_list()

        self.setStyleSheet('''
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
                    border: 2px solid #FFD700;
                    border-radius: 10px;
                    padding: 20px;
                ''')

    def accept_request(self):
        selected_item = self.requests_list.currentItem()
        if selected_item:
            index = self.requests_list.row(selected_item)
            request = self.db_manager.get_employee_requests()[index]
            request.status = "Accepted"
            self.db_manager.update_request_status(request.id, "Accepted")
            self.update_requests_list()
            self.db_manager.send_email_notification(request.client_email, 'Принято')
            self.show_success_message('Заявка принята', 'Заявка успешно принята, клиенту отправлено уведомление.')
            self.setStyleSheet('''
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
                        border: 2px solid #FFD700;
                        border-radius: 10px;
                        padding: 20px;
                    ''')

    def reject_request(self):
        selected_item = self.requests_list.currentItem()
        if selected_item:
            index = self.requests_list.row(selected_item)
            request = self.db_manager.get_employee_requests()[index]
            request.status = "Rejected"
            self.db_manager.update_request_status(request.id, "Rejected")
            self.update_requests_list()
            self.db_manager.send_email_notification(request.client_email, 'Отклонено')
            self.show_success_message('Заявка отклонена', 'Заявка успешно отклонена, клиенту отправлено уведомление.')
            self.setStyleSheet('''
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
                        border: 2px solid #FFD700;
                        border-radius: 10px;
                        padding: 20px;
                    ''')

    def show_success_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)  # Замените на эту строку
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        self.setStyleSheet('''
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
                    border: 2px solid #FFD700;
                    border-radius: 10px;
                    padding: 20px;
                ''')


    def update_requests_list(self):
        requests = self.db_manager.get_employee_requests()
        self.requests_list.clear()
        for request in requests:
            request_text = f"{request.client_name} - {request.service} - {request.item} - {request.status}"
            list_item = QListWidgetItem(request_text)
            self.requests_list.addItem(list_item)

    def finish_work(self):
        self.close()

class ClientWindow(QWidget):
    def __init__(self, db_manager=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.client_name_label = QLabel('Введите ФИО клиента:')
        self.client_name_label.setFont(QFont('Arial', 20))
        self.client_name_edit = QLineEdit()
        layout.addWidget(self.client_name_label)
        layout.addWidget(self.client_name_edit)

        self.client_email_label = QLabel('Введите электронную почту клиента:')
        self.client_email_label.setFont(QFont('Arial', 20))
        self.client_email_edit = QLineEdit()
        layout.addWidget(self.client_email_label)
        layout.addWidget(self.client_email_edit)

        self.client_phone_label = QLabel('Введите номер телефона клиента:')
        self.client_phone_label.setFont(QFont('Arial', 20))
        self.client_phone_edit = QLineEdit()
        layout.addWidget(self.client_phone_label)
        layout.addWidget(self.client_phone_edit)

        self.next_button = QPushButton('Далее')
        self.next_button.setFont(QFont('Arial', 20))
        self.next_button.clicked.connect(self.open_service_window)
        layout.addWidget(self.next_button)

        self.setStyleSheet('''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding: 20px;
        ''')

        self.setLayout(layout)

    def open_service_window(self):
        try:
            print("Открывается окно выбора услуги")
            self.service_window = ServiceSelectionWindow(
                client_name=self.client_name_edit.text(),
                client_email=self.client_email_edit.text(),
                client_phone=self.client_phone_edit.text(),
                db_manager=self.db_manager
            )
            self.hide()  # Скрываем текущее окно
            self.service_window.show()
        except Exception as e:
            print(f"Ошибка в open_service_window: {e}")
class ServiceSelectionWindow(QWidget):
    def __init__(self, client_name, client_email, client_phone, db_manager=None, parent=None):
        super().__init__(parent)
        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.service_label = QLabel('Выберите вид услуги:')
        self.service_label.setFont(QFont('Arial', 18))
        self.service_combo = QComboBox()
        self.service_combo.addItems(['Бытовая', 'Профессиональная', 'Мобильная'])
        self.service_combo.currentIndexChanged.connect(self.show_items_for_selected_service)
        layout.addWidget(self.service_label)
        layout.addWidget(self.service_combo)

        self.items_label = QLabel('Выберите, что нужно починить:')
        self.items_label.setFont(QFont('Arial', 18))
        self.items_combo = QComboBox()
        layout.addWidget(self.items_label)
        layout.addWidget(self.items_combo)

        self.description_label = QLabel('Опишите проблему:')
        self.description_label.setFont(QFont('Arial', 18))
        self.description_text = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_text)

        back_button = QPushButton('Назад')
        back_button.setFont(QFont('Arial', 18))
        back_button.clicked.connect(self.back_to_client_window)
        layout.addWidget(back_button)

        next_button = QPushButton('Отправить заявку')
        next_button.setFont(QFont('Arial', 18))
        next_button.clicked.connect(self.save_request_and_show_thank_you_window)
        layout.addWidget(next_button)

        self.setLayout(layout)

        self.setStyleSheet('''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding: 20px;
        ''')

    def back_to_client_window(self):
        self.client_window = ClientWindow(self.db_manager)
        self.client_window.show()
        self.close()

    def show_items_for_selected_service(self):
        selected_service = self.service_combo.currentText()
        items = []
        if selected_service == 'Бытовая':
            items = ['Микроволновая печь', 'Телевизор', 'Колонка', 'Фен', 'Плойка', 'Утюг', 'Мультиварка', 'Чайник',
                     'Массажер', 'Пылесос']
        elif selected_service == 'Профессиональная':
            items = ['Камера наблюдения', 'Фотоаппарат', 'Зарядное устройство для автомобилей', 'Блок питания',
                     'Пульт дистанционного управления', 'Насос', 'Газонокосилка', 'Микроскоп', 'Маникюрный аппарат',
                     'Навигатор']
        elif selected_service == 'Мобильная':
            items = ['Ноутбук', 'Смартфон', 'Планшет', 'Плеер', 'Наушники']
        self.items_combo.clear()
        self.items_combo.addItems(items)

    def save_request_and_show_thank_you_window(self):
        selected_item = self.items_combo.currentText()
        description = self.description_text.toPlainText()

        # Сохранение заявки в базе данных
        self.db_manager.insert_request(
            client_name=self.client_name,
            client_email=self.client_email,
            client_phone=self.client_phone,
            service=self.service_combo.currentText(),
            item=selected_item,
            description=description,
            status='Pending'
        )

        # Отображение окна с сообщением
        self.show_thank_you_window = ThankYouWindow()
        self.show_thank_you_window.show()
        self.hide()

class ThankYouWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        thank_you_label = QLabel('Ваша заявка на рассмотрение отправлена. '
                                 'Ожидайте письмо на почту.')
        thank_you_label.setFont(QFont('Arial', 20))
        thank_you_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(thank_you_label)

        ok_button = QPushButton('Ок')
        ok_button.setFont(QFont('Arial', 20))
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        self.setStyleSheet('''
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6F61, stop:1 #FFD700);
                    border: 2px solid #FFD700;
                    border-radius: 10px;
                    padding: 20px;
                ''')

    def accept(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    user_type_window = UserTypeWindow()

    app.setQuitOnLastWindowClosed(False)

    user_type_window.show()
    app.exec()