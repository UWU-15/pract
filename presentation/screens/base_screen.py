from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class BaseScreen(Screen):
    """
    Базовый класс для всех экранов приложения.
    Предоставляет общую функциональность и свойства.
    """
    screen_title = StringProperty('')
    
    def show_error(self, title, message):
        """
        Отображает всплывающее окно с сообщением об ошибке.
        """
        from presentation.dialogs.error_popup import ErrorPopup
        error_popup = ErrorPopup(title=title, message=message)
        error_popup.open()