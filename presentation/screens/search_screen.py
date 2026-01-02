from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from presentation.screens.base_screen import BaseScreen
from presentation.widgets.track_item import TrackItem
from presentation.widgets.album_card import AlbumCard
from presentation.widgets.artist_card import ArtistCard
import sqlite3
import os
from config.settings import DB_PATH
from utils.helpers import ensure_file_exists

Builder.load_string('''
<SearchScreen>:
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
            
            TextInput:
                id: search_input
                hint_text: 'Search tracks, albums, artists...'
                multiline: False
                size_hint_x: 0.6
                padding: [dp(10), dp(10), 0, 0]
                background_color: 0.2, 0.2, 0.2, 1
                foreground_color: 1, 1, 1, 1
                on_text_validate: root.search()
            
            Button:
                text: 'Go'
                size_hint_x: 0.2
                background_color: 0.5, 0, 1, 1
                color: 1, 1, 1, 1
                on_release: root.search()
        
        ScrollView:
            BoxLayout:
                id: search_results
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(20)
                size_hint_y: None
                height: self.minimum_height
''')

class SearchScreen(BaseScreen):
    """
    Экран для поиска музыкального контента.
    """
    
    def search(self):
        """
        Выполняет поиск треков, альбомов и исполнителей по запросу.
        """
        query = self.ids.search_input.text.strip()
        if not query:
            return
        
        search_term = f"%{query}%"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Поиск треков
        cursor.execute('''
            SELECT t.id, t.title, ar.name, a.title, t.duration
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            WHERE t.title LIKE ? OR ar.name LIKE ?
            ORDER BY t.title
            LIMIT 10
        ''', (search_term, search_term))
        tracks = cursor.fetchall()
        
        # Поиск альбомов
        cursor.execute('''
            SELECT a.id, a.title, ar.name, a.cover_url, a.release_year
            FROM albums a
            JOIN artists ar ON a.artist_id = ar.id
            WHERE a.title LIKE ? OR ar.name LIKE ?
            ORDER BY a.title
            LIMIT 10
        ''', (search_term, search_term))
        albums = cursor.fetchall()
        
        # Поиск исполнителей
        cursor.execute('''
            SELECT id, name, image_url
            FROM artists
            WHERE name LIKE ?
            ORDER BY name
            LIMIT 10
        ''', (search_term,))
        artists = cursor.fetchall()
        
        conn.close()
        
        results_container = self.ids.search_results
        results_container.clear_widgets()
        
        # Отображение треков
        if tracks:
            label = Label(
                text="Tracks",
                color=(1, 1, 1, 1),
                font_size='18sp',
                size_hint_y=None,
                height=40
            )
            results_container.add_widget(label)
            
            for track_id, title, artist, album, duration in tracks:
                item = TrackItem(
                    track_title=title,
                    track_artist=f"{artist} • {album}",
                    track_id=track_id
                )
                results_container.add_widget(item)
        
        # Отображение альбомов
        if albums:
            label = Label(
                text="Albums",
                color=(1, 1, 1, 1),
                font_size='18sp',
                size_hint_y=None,
                height=40
            )
            results_container.add_widget(label)
            
            grid = GridLayout(cols=2, spacing=15, size_hint_y=None, height=300)
            results_container.add_widget(grid)
            
            for album_id, title, artist, cover_url, year in albums:
                cover_url = ensure_file_exists(cover_url)
                
                card = AlbumCard(
                    title=title,
                    artist=artist,
                    cover_url=cover_url,
                    album_id=album_id
                )
                app = MDApp.get_running_app()
                card.bind(on_release=lambda x, aid=album_id: app.open_album(aid))
                grid.add_widget(card)
        
        # Отображение исполнителей
        if artists:
            label = Label(
                text="Artists",
                color=(1, 1, 1, 1),
                font_size='18sp',
                size_hint_y=None,
                height=40
            )
            results_container.add_widget(label)
            
            grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=200)
            results_container.add_widget(grid)
            
            for artist_id, name, image_url in artists:
                image_url = ensure_file_exists(image_url)
                
                card = ArtistCard(
                    name=name,
                    image_url=image_url,
                    artist_id=artist_id
                )
                card.bind(on_release=lambda x, aid=artist_id: app.open_artist(aid))
                grid.add_widget(card)
        
        # Сообщение если ничего не найдено
        if not tracks and not albums and not artists:
            label = Label(
                text=f"No results found for '{query}'",
                color=(0.7, 0.7, 0.7, 1),
                font_size='16sp',
                size_hint_y=None,
                height=100,
                halign='center'
            )
            results_container.add_widget(label)
    
    def go_back(self):
        """
        Возвращается на главный экран.
        """
        self.manager.current = 'main'