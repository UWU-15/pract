from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty
from presentation.screens.base_screen import BaseScreen
from presentation.widgets.album_card import AlbumCard
import sqlite3
import os
from config.settings import DB_PATH
from utils.helpers import ensure_file_exists

Builder.load_string('''
<ArtistScreen>:
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
                text: root.name
                color: 1, 1, 1, 1
                font_size: sp(20)
                size_hint_x: 0.6
        
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(20)
                size_hint_y: None
                height: self.minimum_height
                
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(120)
                    spacing: dp(20)
                    
                    Image:
                        source: root.image_url
                        size_hint_x: 0.3
                        size_hint_y: 1
                        allow_stretch: True
                        radius: [dp(60)]  # Круглое изображение
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(10)
                        size_hint_x: 0.7
                        
                        Label:
                            text: root.name
                            color: 1, 1, 1, 1
                            font_size: sp(22)
                            size_hint_y: None
                            height: dp(40)
                            text_size: self.width, None
                            halign: 'left'
                            bold: True
                        
                        Label:
                            text: 'Artist'
                            color: 0.7, 0.7, 0.7, 1
                            font_size: sp(14)
                            size_hint_y: None
                            height: dp(20)
                            halign: 'left'
                
                Label:
                    text: 'Biography'
                    color: 0.9, 0.9, 0.9, 1
                    font_size: sp(18)
                    size_hint_y: None
                    height: dp(30)
                
                Label:
                    id: bio_text
                    text: root.bio
                    color: 0.7, 0.7, 0.7, 1
                    size_hint_y: None
                    height: self.texture_size[1] + dp(20)
                    text_size: self.width - dp(20), None
                    padding: [dp(10), dp(10)]
                
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(40)
                    
                    Label:
                        text: 'Albums'
                        color: 0.9, 0.9, 0.9, 1
                        font_size: sp(18)
                        size_hint_x: 0.7
                    
                    Label:
                        id: album_count
                        text: ''
                        color: 0.7, 0.7, 0.7, 1
                        font_size: sp(14)
                        size_hint_x: 0.3
                        halign: 'right'
                
                GridLayout:
                    id: artist_albums_grid
                    cols: 2
                    spacing: dp(15)
                    size_hint_y: None
                    height: self.minimum_height
''')

class ArtistScreen(BaseScreen):
    """
    Экран для отображения детальной информации об исполнителе.
    """
    name = StringProperty('')
    bio = StringProperty('')
    image_url = StringProperty('')
    artist_id = NumericProperty(0)
    
    def on_pre_enter(self):
        """
        Вызывается перед показом экрана.
        Загружает данные об исполнителе и его альбомы.
        """
        self.load_artist_data()
        self.load_artist_albums()
    
    def load_artist_data(self):
        """
        Загружает основную информацию об исполнителе из базы данных.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, bio, image_url
            FROM artists
            WHERE id = ?
        ''', (self.artist_id,))
        
        artist_data = cursor.fetchone()
        conn.close()
        
        if artist_data:
            self.name = artist_data[0]
            self.bio = artist_data[1] if artist_data[1] else "No biography available"
            self.image_url = ensure_file_exists(artist_data[2])
    
    def load_artist_albums(self):
        """
        Загружает альбомы исполнителя из базы данных.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.title, a.cover_url, a.release_year, a.description
            FROM albums a
            WHERE a.artist_id = ?
            ORDER BY a.release_year DESC
        ''', (self.artist_id,))
        albums = cursor.fetchall()
        
        album_count_label = self.ids.album_count
        album_count_label.text = f"{len(albums)} album{'s' if len(albums) != 1 else ''}"
        
        albums_grid = self.ids.artist_albums_grid
        albums_grid.clear_widgets()
        
        for album_id, title, cover_url, year, description in albums:
            cover_url = ensure_file_exists(cover_url)
            
            card = AlbumCard(
                title=title,
                artist=self.name,
                cover_url=cover_url,
                album_id=album_id
            )
            app = MDApp.get_running_app()
            card.bind(on_release=lambda x, aid=album_id: app.open_album(aid))
            albums_grid.add_widget(card)
        
        conn.close()
    
    def go_back(self):
        """
        Возвращается на главный экран.
        """
        self.manager.current = 'main'