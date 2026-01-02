from kivy.lang import Builder
from kivymd.app import MDApp
from presentation.screens.base_screen import BaseScreen
from presentation.dialogs.error_popup import ErrorPopup
from presentation.dialogs.register_popup import RegisterPopup
import sqlite3
from config.settings import DB_PATH

Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(30)
        
        Label:
            text: 'Music Lore'
            font_size: sp(32)
            size_hint_y: None
            height: dp(100)
            color: 0.5, 0, 1, 1
        
        TextInput:
            id: username
            hint_text: 'Username'
            size_hint_y: None
            height: dp(40)
            multiline: False
            padding: [dp(10), dp(10), 0, 0]
            background_color: 0.2, 0.2, 0.2, 1
            foreground_color: 1, 1, 1, 1
        
        TextInput:
            id: password
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: dp(40)
            multiline: False
            padding: [dp(10), dp(10), 0, 0]
            background_color: 0.2, 0.2, 0.2, 1
            foreground_color: 1, 1, 1, 1
        
        Button:
            text: 'Login'
            size_hint_y: None
            height: dp(40)
            background_color: 0.5, 0, 1, 1
            color: 1, 1, 1, 1
            on_release: root.login()
        
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: dp(5)
            
            Label:
                text: 'New user?'
                color: 0.8, 0.8, 0.8, 1
                size_hint_x: 0.6
            
            Button:
                text: 'Register'
                size_hint_x: 0.4
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.show_register_popup()
''')

class LoginScreen(BaseScreen):
    """
    Экран для авторизации и регистрации пользователей.
    """
    
    def login(self):
        """
        Обрабатывает попытку входа пользователя.
        """
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        
        if not username or not password:
            error_popup = ErrorPopup(title='Login Error', message='Please fill in all fields')
            error_popup.open()
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, preferences_set FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_id, username, preferences_set = user
            app = MDApp.get_running_app()
            app.current_user_id = user_id
            app.current_username = username
            
            if preferences_set:
                self.manager.current = 'main'
            else:
                self.manager.current = 'tag_selection'
        else:
            error_popup = ErrorPopup(title='Login Error', message='Invalid username or password')
            error_popup.open()
    
    def show_register_popup(self):
        """
        Отображает всплывающее окно для регистрации нового пользователя.
        """
        popup = RegisterPopup()
        popup.open()