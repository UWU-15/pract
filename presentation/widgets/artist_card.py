from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from config.settings import DEFAULT_IMAGE

# Загружаем KV описание виджета
Builder.load_string('''
<ArtistCard>:
    orientation: 'vertical'
    size_hint: None, None
    size: dp(120), dp(150)
    padding: dp(10)
    spacing: dp(5)
    
    Image:
        source: root.image_url
        size_hint_y: None
        height: dp(80)
        allow_stretch: True
        radius: [dp(40)]  # Делаем изображение круглым
    
    Label:
        text: root.name
        color: 1, 1, 1, 1
        size_hint_y: None
        height: dp(40)
        text_size: self.width, None
        shorten: True
        halign: 'center'
''')

class ArtistCard(ButtonBehavior, BoxLayout):
    """
    Карточка исполнителя, отображающая фотографию и имя.
    Наследует от ButtonBehavior для возможности клика.
    """
    name = StringProperty('')
    image_url = StringProperty(DEFAULT_IMAGE)
    artist_id = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Создаем закругленный прямоугольный фон для карточки
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        # Связываем обновление позиции и размера с фоном
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        """Обновляет позицию и размер фонового прямоугольника."""
        self.rect.pos = self.pos
        self.rect.size = self.size