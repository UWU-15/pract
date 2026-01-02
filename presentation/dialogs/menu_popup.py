from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivymd.app import MDApp

# Загружаем KV описание виджета
Builder.load_string('''
<MenuPopup>:
    size_hint: (0.6, 0.5)  # Размер окна относительно родительского
    auto_dismiss: True     # Окно закрывается при клике вне его
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)   # Внутренние отступы
        spacing: dp(10)   # Расстояние между элементами
        
        Label:
            text: 'Menu'
            color: 1, 1, 1, 1      # Белый цвет текста
            font_size: sp(20)      # Размер шрифта
            size_hint_y: None
            height: dp(40)
        
        Button:
            text: 'Profile'
            size_hint_y: None
            height: dp(40)
            background_color: 0.3, 0.3, 0.3, 1  # Темно-серый цвет фона
            color: 1, 1, 1, 1                   # Белый цвет текста
        
        Button:
            text: 'Favorites'
            size_hint_y: None
            height: dp(40)
            background_color: 0.3, 0.3, 0.3, 1  # Темно-серый цвет фона
            color: 1, 1, 1, 1                   # Белый цвет текста
            on_release: root.show_favorites()   # Обработчик клика
        
        Button:
            text: 'Logout'
            size_hint_y: None
            height: dp(40)
            background_color: 0.7, 0, 0, 1      # Красный цвет фона
            color: 1, 1, 1, 1                   # Белый цвет текста
            on_release: root.logout()           # Обработчик клика
''')

class MenuPopup(ModalView):
    """
    Всплывающее меню приложения с навигационными кнопками.
    """
    
    def show_favorites(self):
        """
        Закрывает меню и переходит на экран избранного.
        """
        app = MDApp.get_running_app()
        self.dismiss()  # Закрываем меню
        app.root.current = 'favorites'  # Переключаемся на экран избранного
    
    def logout(self):
        """
        Выполняет выход пользователя из системы:
        1. Сбрасывает данные текущего пользователя
        2. Закрывает меню
        3. Переходит на экран входа
        """
        app = MDApp.get_running_app()
        # Сбрасываем данные пользователя
        app.current_user_id = 0
        app.current_username = ''
        self.dismiss()  # Закрываем меню
        app.root.current = 'login'  # Переключаемся на экран входа