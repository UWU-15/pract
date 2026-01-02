from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivymd.app import MDApp
from presentation.screens.base_screen import BaseScreen
from presentation.widgets.album_card import AlbumCard
from presentation.widgets.track_item import TrackItem
from presentation.dialogs.menu_popup import MenuPopup
import sqlite3
import os
from config.settings import DB_PATH
from utils.helpers import ensure_file_exists

Builder.load_string('''
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            
            Button:
                text: 'Menu'
                size_hint_x: 0.15
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.show_menu()
            
            Label:
                text: 'Music Lore'
                color: 1, 1, 1, 1
                font_size: sp(20)
                size_hint_x: 0.5
            
            Button:
                text: 'Fav'
                size_hint_x: 0.15
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.show_favorites()
            
            Button:
                text: 'Search'
                size_hint_x: 0.15
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.show_search()
        
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(20)
                size_hint_y: None
                height: self.minimum_height
                
                Label:
                    text: 'Recommended Albums'
                    color: 1, 1, 1, 1
                    font_size: sp(18)
                    size_hint_y: None
                    height: dp(40)
                
                GridLayout:
                    id: albums_grid
                    cols: 2
                    spacing: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
                
                Label:
                    text: 'Recommended Tracks'
                    color: 1, 1, 1, 1
                    font_size: sp(18)
                    size_hint_y: None
                    height: dp(40)
                
                BoxLayout:
                    id: tracks_list
                    orientation: 'vertical'
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
''')

class MainScreen(BaseScreen):
    """
    Главный экран приложения с рекомендациями на основе предпочтений пользователя.
    """
    
    def on_pre_enter(self):
        """
        Вызывается перед показом экрана.
        Загружает рекомендации для пользователя.
        """
        self.load_recommendations()
    
    def load_recommendations(self):
        """
        Загружает рекомендованные альбомы и треки на основе тегов пользователя.
        """
        app = MDApp.get_running_app()
        if not app.current_user_id:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Получаем теги пользователя
        cursor.execute('''
            SELECT t.id 
            FROM tags t
            JOIN user_tags ut ON t.id = ut.tag_id
            WHERE ut.user_id = ?
        ''', (app.current_user_id,))
        user_tags = cursor.fetchall()
        
        # Получаем рекомендованные альбомы
        if user_tags:
            tag_ids = [str(tag[0]) for tag in user_tags]
            query = f'''
                SELECT DISTINCT a.id, a.title, ar.name, a.cover_url, a.release_year, a.description
                FROM albums a
                JOIN artists ar ON a.artist_id = ar.id
                JOIN album_tags at ON a.id = at.album_id
                WHERE at.tag_id IN ({','.join(tag_ids)})
                LIMIT 6
            '''
        else:
            query = '''
                SELECT a.id, a.title, ar.name, a.cover_url, a.release_year, a.description
                FROM albums a
                JOIN artists ar ON a.artist_id = ar.id
                LIMIT 3
            '''
        
        cursor.execute(query)
        albums = cursor.fetchall()
        
        albums_grid = self.ids.albums_grid
        albums_grid.clear_widgets()
        
        for album_id, title, artist, cover_url, year, description in albums:
            cover_url = ensure_file_exists(cover_url)
            
            card = AlbumCard(
                title=title,
                artist=artist,
                cover_url=cover_url,
                album_id=album_id
            )
            card.bind(on_release=lambda x, aid=album_id: app.open_album(aid))
            albums_grid.add_widget(card)
        
        # Получаем рекомендованные треки
        if user_tags:
            query = f'''
                SELECT DISTINCT t.id, t.title, ar.name, a.title, t.duration
                FROM tracks t
                JOIN albums a ON t.album_id = a.id
                JOIN artists ar ON a.artist_id = ar.id
                JOIN album_tags at ON a.id = at.album_id
                WHERE at.tag_id IN ({','.join(tag_ids)})
                LIMIT 5
            '''
        else:
            query = '''
                SELECT t.id, t.title, ar.name, a.title, t.duration
                FROM tracks t
                JOIN albums a ON t.album_id = a.id
                JOIN artists ar ON a.artist_id = ar.id
                LIMIT 3
            '''
        
        cursor.execute(query)
        tracks = cursor.fetchall()
        
        tracks_list = self.ids.tracks_list
        tracks_list.clear_widgets()
        
        for track_id, title, artist, album, duration in tracks:
            item = TrackItem(
                track_title=title,
                track_artist=f"{artist} • {album}",
                track_id=track_id
            )
            tracks_list.add_widget(item)
        
        conn.close()
    
    def show_menu(self):
        """
        Отображает меню приложения.
        """
        menu = MenuPopup()
        menu.open()
    
    def show_favorites(self):
        """
        Переходит на экран избранного.
        """
        self.manager.current = 'favorites'
    
    def show_search(self):
        """
        Переходит на экран поиска.
        """
        self.manager.current = 'search'