from kivy.lang import Builder
from kivy.uix.modalview import ModalView
import sqlite3
from kivymd.app import MDApp
from utils.validators import validate_user_registration
from presentation.dialogs.error_popup import ErrorPopup
from config.settings import DB_PATH

# Загружаем KV описание виджета
Builder.load_string('''
<RegisterPopup>:
    size_hint: (0.8, 0.8)  # Размер окна относительно родительского
    auto_dismiss: False    # Окно не закрывается при клике вне его
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)   # Внутренние отступы
        spacing: dp(15)   # Расстояние между элементами
        
        Label:
            text: 'Create Account'
            color: 1, 1, 1, 1      # Белый цвет текста
            font_size: sp(24)      # Размер шрифта
            size_hint_y: None
            height: dp(50)
        
        TextInput:
            id: reg_username
            hint_text: 'Username'
            size_hint_y: None
            height: dp(40)
            multiline: False       # Однострочное поле
            padding: [dp(10), dp(10), 0, 0]
            background_color: 0.2, 0.2, 0.2, 1  # Темно-серый фон
            foreground_color: 1, 1, 1, 1        # Белый текст
        
        TextInput:
            id: reg_email
            hint_text: 'Email'
            size_hint_y: None
            height: dp(40)
            multiline: False       # Однострочное поле
            padding: [dp(10), dp(10), 0, 0]
            background_color: 0.2, 0.2, 0.2, 1  # Темно-серый фон
            foreground_color: 1, 1, 1, 1        # Белый текст
        
        TextInput:
            id: reg_password
            hint_text: 'Password'
            password: True         # Скрытый ввод пароля
            size_hint_y: None
            height: dp(40)
            multiline: False       # Однострочное поле
            padding: [dp(10), dp(10), 0, 0]
            background_color: 0.2, 0.2, 0.2, 1  # Темно-серый фон
            foreground_color: 1, 1, 1, 1        # Белый текст
        
        TextInput:
            id: reg_confirm
            hint_text: 'Confirm Password'
            password: True         # Скрытый ввод пароля
            size_hint_y: None
            height: dp(40)
            multiline: False       # Однострочное поле
            padding: [dp(10), dp(10), 0, 0]
            background_color: 0.2, 0.2, 0.2, 1  # Темно-серый фон
            foreground_color: 1, 1, 1, 1        # Белый текст
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            
            Button:
                text: 'Cancel'
                background_color: 0.7, 0, 0, 1  # Красный цвет фона
                color: 1, 1, 1, 1               # Белый цвет текста
                on_release: root.dismiss()      # Закрытие окна
            
            Button:
                text: 'Register'
                background_color: 0, 0.7, 0, 1  # Зеленый цвет фона
                color: 1, 1, 1, 1               # Белый цвет текста
                on_release: root.register()     # Обработчик регистрации
''')

class RegisterPopup(ModalView):
    """
    Всплывающее окно для регистрации нового пользователя.
    """
    
    def register(self):
        """
        Обрабатывает регистрацию нового пользователя:
        1. Получает данные из полей ввода
        2. Проверяет валидность данных
        3. Регистрирует пользователя в базе данных
        4. Выполняет авторизацию
        """
        # Получаем данные из полей ввода
        username = self.ids.reg_username.text.strip()
        email = self.ids.reg_email.text.strip()
        password = self.ids.reg_password.text.strip()
        confirm = self.ids.reg_confirm.text.strip()
        
        # Валидируем данные
        errors = validate_user_registration(username, email, password, confirm)
        
        # Если есть ошибки валидации - показываем их
        if errors:
            error_popup = ErrorPopup(title='Registration Error', message='\n'.join(errors))
            error_popup.open()
            return
        
        # Подключаемся к базе данных
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            # Регистрируем пользователя в базе данных
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password, email)
            )
            user_id = cursor.lastrowid  # Получаем ID нового пользователя
            conn.commit()  # Сохраняем изменения
            
            # Авторизуем пользователя в приложении
            app = MDApp.get_running_app()
            app.current_user_id = user_id
            app.current_username = username
            
            self.dismiss()  # Закрываем окно регистрации
            
            # Переходим на экран выбора тегов
            screen_manager = app.root
            screen_manager.current = 'tag_selection'
            
        except sqlite3.IntegrityError as e:
            # Обрабатываем ошибки уникальности данных
            if 'username' in str(e):
                error_popup = ErrorPopup(title='Registration Error', message='Username already exists')
            elif 'email' in str(e):
                error_popup = ErrorPopup(title='Registration Error', message='Email already registered')
            else:
                error_popup = ErrorPopup(title='Registration Error', message='Registration failed')
            error_popup.open()
        finally:
            # Всегда закрываем соединение с базой данных
            conn.close()