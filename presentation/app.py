import os
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty

# Импорт конфигурации и утилит
from config.settings import WINDOW_SIZE
from infrastructure.database.sqlite_repository import DatabaseInitializer
from utils.helpers import create_placeholder_files

# Импорт экранов приложения
from presentation.screens.login_screen import LoginScreen
from presentation.screens.tag_selection_screen import TagSelectionScreen
from presentation.screens.main_screen import MainScreen
from presentation.screens.album_screen import AlbumScreen
from presentation.screens.artist_screen import ArtistScreen
from presentation.screens.search_screen import SearchScreen
from presentation.screens.favorites_screen import FavoritesScreen
from presentation.screens.player_screen import PlayerScreen

# Настройки окна приложения
Window.size = WINDOW_SIZE

class MusicLoreApp(MDApp):
    """
    Главный класс приложения MusicLore, наследующий от MDApp (Material Design App).
    """
    current_user_id = NumericProperty(0)
    current_username = StringProperty('')
    favorite_tracks = ListProperty([])
    current_favorite_index = NumericProperty(0)
    
    def build(self):
        """
        Создаёт и возвращает корневой виджет приложения.
        """
        # Инициализируем базу данных
        DatabaseInitializer.init_database()
        
        # Создаем placeholder файлы для треков и обложек
        create_placeholder_files()
        
        # Создаем менеджер экранов
        sm = ScreenManager()
        
        # Добавляем все экраны приложения
        sm.add_widget(LoginScreen(name='login'))                # Экран авторизации
        sm.add_widget(TagSelectionScreen(name='tag_selection')) # Экран выбора тегов
        sm.add_widget(MainScreen(name='main'))                  # Главный экран
        sm.add_widget(AlbumScreen(name='album'))                # Экран альбома
        sm.add_widget(ArtistScreen(name='artist'))              # Экран исполнителя
        sm.add_widget(FavoritesScreen(name='favorites'))        # Экран избранного
        sm.add_widget(SearchScreen(name='search'))              # Экран поиска
        sm.add_widget(PlayerScreen(name='player'))              # Экран плеера
        
        return sm
    
    def open_album(self, album_id):
        """
        Открывает экран с информацией об альбоме.
        """
        import sqlite3
        from config.settings import DB_PATH
        from utils.helpers import ensure_file_exists
        
        # Подключаемся к базе данных и получаем данные альбома
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.title, ar.name, a.release_year, a.cover_url, 
                   a.description, a.lore_description
            FROM albums a
            JOIN artists ar ON a.artist_id = ar.id
            WHERE a.id = ?
        ''', (album_id,))
        album_data = cursor.fetchone()
        
        conn.close()
        
        if album_data:
            # Распаковываем данные альбома
            title, artist, year, cover_url, description, lore_description = album_data
            
            # Проверяем существование файла обложки
            cover_url = ensure_file_exists(cover_url)
            
            # Получаем экран альбома и устанавливаем данные
            album_screen = self.root.get_screen('album')
            album_screen.title = title
            album_screen.artist = artist
            album_screen.year = year
            album_screen.cover_url = cover_url
            album_screen.description = description
            album_screen.lore_description = lore_description
            album_screen.album_id = album_id
            
            # Переключаемся на экран альбома
            self.root.current = 'album'
        else:
            print(f"Album with id {album_id} not found")
    
    def open_artist(self, artist_id):
        """
        Открывает экран с информацией об исполнителе.
        """
        artist_screen = self.root.get_screen('artist')
        artist_screen.artist_id = artist_id
        
        # Переключаемся на экран исполнителя
        self.root.current = 'artist'
    
    def play_track(self, track_id, context='single'):
        """
        Загружает и воспроизводит трек в плеере.
        """
        try:
            player_screen = self.root.get_screen('player')
            # Загружаем трек с указанным контекстом
            player_screen.load_track(track_id, context)
            
            # Переключаемся на экран плеера
            self.root.current = 'player'
            
            # Запускаем воспроизведение с небольшой задержкой
            Clock.schedule_once(lambda dt: player_screen.toggle_play(), 0.5)
        except Exception as e:
            print(f"Error in play_track: {e}")
    
    def play_from_favorites(self, start_track_id=None):
        """
        Воспроизводит треки из избранного.
        """
        if not self.current_user_id:
            return
        
        import sqlite3
        from config.settings import DB_PATH
        
        # Получаем список избранных треков пользователя
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.album_id, t.track_number
            FROM tracks t
            JOIN favorites f ON t.id = f.track_id
            WHERE f.user_id = ?
            ORDER BY f.added_at DESC
        ''', (self.current_user_id,))
        
        favorite_tracks = cursor.fetchall()
        conn.close()
        
        if not favorite_tracks:
            print("No favorite tracks")
            return
        
        # Сохраняем список ID избранных треков
        self.favorite_tracks = [track[0] for track in favorite_tracks]
        self.current_favorite_index = 0
        
        # Если указан стартовый трек, начинаем с него
        if start_track_id and start_track_id in self.favorite_tracks:
            self.current_favorite_index = self.favorite_tracks.index(start_track_id)
        
        # Запускаем воспроизведение
        self.play_track(self.favorite_tracks[self.current_favorite_index], 'favorites')

# Вспомогательные функции для использования в KV файлах
def dp(value):
    """
    Функция для конвертации значений в density-independent pixels.
    В данном случае просто возвращает значение без изменений.
    """
    return value

def sp(value):
    """
    Функция для конвертации значений в scale-independent pixels.
    В данном случае просто возвращает значение без изменений.
    """
    return value