from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.properties import StringProperty
from presentation.screens.base_screen import BaseScreen
from presentation.widgets.track_item import TrackItem
import sqlite3
from config.settings import DB_PATH

Builder.load_string('''
<FavoritesScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            
            Button:
                text: '< Back'
                size_hint_x: 0.2
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.go_back()
            
            Label:
                text: 'My Favorites'
                color: 1, 1, 1, 1
                font_size: sp(20)
                size_hint_x: 0.6
        
        ScrollView:
            BoxLayout:
                id: favorites_list
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
''')

class FavoritesScreen(BaseScreen):
    """
    Экран для отображения избранных треков пользователя.
    """
    
    def on_pre_enter(self):
        """
        Вызывается перед показом экрана.
        Загружает список избранных треков пользователя.
        """
        self.load_favorites()
    
    def load_favorites(self):
        """
        Загружает избранные треки пользователя из базы данных.
        """
        app = MDApp.get_running_app()
        if not app.current_user_id:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.title, ar.name, a.title, t.duration
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            JOIN favorites f ON t.id = f.track_id
            WHERE f.user_id = ?
            ORDER BY f.added_at DESC
        ''', (app.current_user_id,))
        favorites = cursor.fetchall()
        
        favorites_list = self.ids.favorites_list
        favorites_list.clear_widgets()
        
        if not favorites:
            label = Label(
                text="No favorites yet\n\nAdd tracks to favorites by clicking the heart icon",
                color=(0.7, 0.7, 0.7, 1),
                font_size='16sp',
                halign='center',
                size_hint_y=None,
                height=200
            )
            favorites_list.add_widget(label)
        else:
            for track_id, title, artist, album, duration in favorites:
                item = TrackItem(
                    track_title=title,
                    track_artist=f"{artist}•{album}",
                    track_id=track_id
                )
                item.is_favorite = True
                favorites_list.add_widget(item)
        
        conn.close()
    
    def go_back(self):
        """
        Возвращается на главный экран.
        """
        self.manager.current = 'main'