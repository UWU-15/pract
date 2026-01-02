from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from config.settings import DEFAULT_COVER

# Загружаем KV описание виджета
Builder.load_string('''
<AlbumCard>:
    orientation: 'vertical'
    size_hint: None, None
    size: dp(150), dp(200)
    padding: dp(10)
    spacing: dp(5)
    
    Image:
        source: root.cover_url
        size_hint_y: None
        height: dp(120)
        allow_stretch: True
    
    Label:
        text: root.title
        color: 1, 1, 1, 1
        size_hint_y: None
        height: dp(30)
        text_size: self.width, None
        shorten: True
        halign: 'center'
    
    Label:
        text: root.artist
        color: 0.7, 0.7, 0.7, 1
        size_hint_y: None
        height: dp(20)
        text_size: self.width, None
        shorten: True
        halign: 'center'
''')

class AlbumCard(ButtonBehavior, BoxLayout):
    """
    Карточка альбома, отображающая обложку, название и исполнителя.
    Наследует от ButtonBehavior для возможности клика.
    """
    title = StringProperty('')
    artist = StringProperty('')
    cover_url = StringProperty(DEFAULT_COVER)
    album_id = NumericProperty(0)
    
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