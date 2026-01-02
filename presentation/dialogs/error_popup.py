from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty

# Загружаем KV описание виджета
Builder.load_string('''
<ErrorPopup>:
    size_hint: (0.7, 0.3)  # Размер окна относительно родительского
    auto_dismiss: False    # Окно не закрывается при клике вне его
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)   # Внутренние отступы
        spacing: dp(15)   # Расстояние между элементами
        
        Label:
            text: root.title
            color: 1, 1, 1, 1      # Белый цвет текста
            font_size: sp(18)      # Размер шрифта
            size_hint_y: None
            height: dp(40)
        
        Label:
            text: root.message
            color: 0.9, 0.9, 0.9, 1  # Светло-серый цвет текста
            text_size: self.width, None  # Автоматический перенос текста
        
        Button:
            text: 'OK'
            size_hint_y: None
            height: dp(40)
            background_color: 0.5, 0, 1, 1  # Фиолетовый цвет фона
            color: 1, 1, 1, 1              # Белый цвет текста
            on_release: root.dismiss()      # Закрытие окна при клике
''')

class ErrorPopup(ModalView):
    """
    Всплывающее окно для отображения сообщений об ошибках.
    """
    title = StringProperty('Error')
    message = StringProperty('')