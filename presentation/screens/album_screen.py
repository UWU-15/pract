from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty
from presentation.screens.base_screen import BaseScreen
from presentation.widgets.track_item import TrackItem
import sqlite3
from config.settings import DB_PATH
from utils.helpers import ensure_file_exists

Builder.load_string('''
<AlbumScreen>:
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
                text: 'Album'
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
                    height: dp(200)
                    spacing: dp(20)
                    
                    Image:
                        source: root.cover_url
                        size_hint_x: 0.4
                        allow_stretch: True
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(5)
                        
                        Label:
                            text: root.title
                            color: 1, 1, 1, 1
                            font_size: sp(20)
                            size_hint_y: None
                            height: dp(40)
                            text_size: self.width, None
                            halign: 'left'
                        
                        Label:
                            text: root.artist
                            color: 0.7, 0.7, 0.7, 1
                            font_size: sp(16)
                            size_hint_y: None
                            height: dp(30)
                            text_size: self.width, None
                            halign: 'left'
                        
                        Label:
                            text: str(root.year)
                            color: 0.5, 0.5, 0.5, 1
                            size_hint_y: None
                            height: dp(25)
                            halign: 'left'
                
                Label:
                    text: 'Description'
                    color: 0.9, 0.9, 0.9, 1
                    font_size: sp(18)
                    size_hint_y: None
                    height: dp(30)
                
                Label:
                    text: root.description
                    color: 0.7, 0.7, 0.7, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                
                Label:
                    text: 'Story & Lore'
                    color: 0.9, 0.9, 0.9, 1
                    font_size: sp(18)
                    size_hint_y: None
                    height: dp(30)
                
                Label:
                    text: root.lore_description
                    color: 0.7, 0.7, 0.7, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                
                Label:
                    text: 'Tracks'
                    color: 0.9, 0.9, 0.9, 1
                    font_size: sp(18)
                    size_hint_y: None
                    height: dp(30)
                
                BoxLayout:
                    id: album_tracks_list
                    orientation: 'vertical'
                    spacing: dp(5)
                    size_hint_y: None
                    height: self.minimum_height
''')

class AlbumScreen(BaseScreen):
    """
    Экран для отображения детальной информации об альбоме.
    """
    title = StringProperty('')
    artist = StringProperty('')
    year = NumericProperty(0)
    cover_url = StringProperty('')
    description = StringProperty('')
    lore_description = StringProperty('')
    album_id = NumericProperty(0)
    
    def on_pre_enter(self):
        """
        Вызывается перед показом экрана.
        Загружает треки альбома.
        """
        self.load_album_tracks()
    
    def load_album_tracks(self):
        """
        Загружает список треков альбома из базы данных.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.title, t.duration, t.track_number
            FROM tracks t
            WHERE t.album_id = ?
            ORDER BY t.track_number
        ''', (self.album_id,))
        tracks = cursor.fetchall()
        
        tracks_list = self.ids.album_tracks_list
        tracks_list.clear_widgets()
        
        for track_id, title, duration, track_num in tracks:
            item = TrackItem(
                track_title=f"{track_num}. {title}",
                track_artist=self.artist,
                track_id=track_id
            )
            tracks_list.add_widget(item)
        
        conn.close()
    
    def go_back(self):
        """
        Возвращается на главный экран.
        """
        self.manager.current = 'main'