from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
import sqlite3
from kivymd.app import MDApp
from config.settings import DB_PATH

# Загружаем KV описание виджета
Builder.load_string('''
<TrackItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(60)
    padding: dp(10)
    spacing: dp(10)
    
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.6
        
        Label:
            text: root.track_title
            color: 1, 1, 1, 1
            size_hint_y: None
            height: dp(25)
            text_size: self.width, None
            halign: 'left'
        
        Label:
            text: root.track_artist
            color: 0.7, 0.7, 0.7, 1
            size_hint_y: None
            height: dp(20)
            text_size: self.width, None
            halign: 'left'
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.4
        spacing: dp(5)
        
        Button:
            text: 'Fav'
            size_hint_x: 0.5
            background_color: (0.7, 0, 0, 1) if root.is_favorite else (0.3, 0.3, 0.3, 1)
            color: 1, 1, 1, 1
            font_size: sp(18)
            on_release: root.toggle_favorite()
        
        Button:
            text: 'Play'
            size_hint_x: 0.5
            background_color: 0.5, 0, 1, 1
            color: 1, 1, 1, 1
            on_release: root.play()
''')

class TrackItem(BoxLayout):
    """
    Элемент списка треков, отображающий название, исполнителя и кнопки действий.
    """
    track_title = StringProperty('')
    track_artist = StringProperty('')
    track_id = NumericProperty(0)
    is_favorite = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Проверяем статус избранного при создании
        self.check_favorite_status()
    
    def check_favorite_status(self):
        """
        Проверяет, находится ли трек в избранном у текущего пользователя.
        """
        app = MDApp.get_running_app()
        if app.current_user_id and self.track_id:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM favorites WHERE user_id = ? AND track_id = ?",
                (app.current_user_id, self.track_id)
            )
            self.is_favorite = cursor.fetchone() is not None
            conn.close()
    
    def toggle_favorite(self):
        """
        Добавляет или удаляет трек из избранного пользователя.
        """
        app = MDApp.get_running_app()
        if not app.current_user_id:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if self.is_favorite:
            # Удаляем из избранного
            cursor.execute(
                "DELETE FROM favorites WHERE user_id = ? AND track_id = ?",
                (app.current_user_id, self.track_id)
            )
            self.is_favorite = False
        else:
            # Добавляем в избранное
            cursor.execute(
                "INSERT OR IGNORE INTO favorites (user_id, track_id) VALUES (?, ?)",
                (app.current_user_id, self.track_id)
            )
            self.is_favorite = True
        
        conn.commit()
        conn.close()
    
    def play(self):
        """
        Запускает воспроизведение трека с учетом текущего контекста.
        """
        app = MDApp.get_running_app()
        if hasattr(app, 'play_track'):
            current_screen = app.root.current
            
            # Выбираем контекст воспроизведения в зависимости от текущего экрана
            if current_screen == 'album':
                app.play_track(self.track_id, 'album')
            elif current_screen == 'favorites':
                # Для избранного запускаем последовательное воспроизведение
                if hasattr(app, 'play_from_favorites'):
                    app.play_from_favorites(self.track_id)
                else:
                    app.play_track(self.track_id, 'single')
            else:
                app.play_track(self.track_id, 'single')