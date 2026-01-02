# Импортируем все экраны приложения
from .base_screen import BaseScreen           # Базовый класс экрана
from .login_screen import LoginScreen         # Экран авторизации
from .tag_selection_screen import TagSelectionScreen  # Экран выбора тегов
from .main_screen import MainScreen           # Главный экран
from .album_screen import AlbumScreen         # Экран альбома
from .artist_screen import ArtistScreen       # Экран исполнителя
from .search_screen import SearchScreen       # Экран поиска
from .favorites_screen import FavoritesScreen # Экран избранного
from .player_screen import PlayerScreen       # Экран плеера

# Определяем публичные экспорты модуля
__all__ = [
    'BaseScreen',
    'LoginScreen',
    'TagSelectionScreen',
    'MainScreen',
    'AlbumScreen',
    'ArtistScreen',
    'SearchScreen',
    'FavoritesScreen',
    'PlayerScreen'
]