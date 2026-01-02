from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

# Загружаем KV описание виджета
Builder.load_string('''
<TagButton>:
    text: root.tag_name
    size_hint_y: None
    height: dp(40)
    background_color: (0.2, 0.2, 0.2, 1) if not root.selected else (0.5, 0, 1, 1)
    color: 1, 1, 1, 1
    on_release: root.toggle()
''')

class TagButton(Button):
    """
    Кнопка тега, которая может находиться в выбранном/невыбранном состоянии.
    """
    tag_id = NumericProperty(0)
    tag_name = StringProperty('')
    selected = BooleanProperty(False)
    
    def toggle(self):
        """
        Переключает состояние кнопки и уведомляет родительский экран.
        """
        self.selected = not self.selected
        # Находим родительский экран и вызываем обработчик выбора тега
        screen = self.parent.parent.parent.parent.parent
        if hasattr(screen, 'on_tag_toggle'):
            screen.on_tag_toggle(self.tag_id, self.selected)