from typing import Optional, List
from core.interfaces import (
    IUserRepository, IAlbumRepository, ITrackRepository,
    IArtistRepository, ITagRepository
)
from core.models import User, Album, Track, Artist, Tag

class AuthService:
    """
    Сервис для аутентификации и регистрации пользователей.
    """
    def __init__(self, user_repository: IUserRepository):
        """
        Инициализирует сервис аутентификации.
        """
        self._user_repository = user_repository
    
    def login(self, username: str, password: str) -> Optional[User]:
        """
        Аутентифицирует пользователя.
        """
        user = self._user_repository.get_by_username(username)
        # Проверяем совпадение пароля (в реальном приложении следует использовать хэширование)
        if user and user.password == password:
            return user
        return None
    
    def register(self, username: str, email: str, password: str) -> User:
        """
        Регистрирует нового пользователя.
        """
        user = User(
            id=0,  # ID будет присвоен репозиторием при сохранении
            username=username,
            email=email,
            password=password,
            preferences_set=False  # Новый пользователь еще не выбрал предпочтения
        )
        return self._user_repository.create(user)

class MusicService:
    """
    Сервис для работы с музыкальными данными.
    """
    def __init__(
        self,
        album_repository: IAlbumRepository,
        track_repository: ITrackRepository,
        artist_repository: IArtistRepository,
        tag_repository: ITagRepository
    ):
        """
        Инициализирует музыкальный сервис.
        """
        self._album_repository = album_repository
        self._track_repository = track_repository
        self._artist_repository = artist_repository
        self._tag_repository = tag_repository
    
    def get_album_recommendations(self, user_tags: List[int]) -> List[Album]:
        """
        Получает рекомендации альбомов на основе тегов пользователя.
        """
        return self._album_repository.get_recommendations(user_tags)
    
    def get_album_by_id(self, album_id: int) -> Optional[Album]:
        """
        Получает альбом по ID.
        """
        return self._album_repository.get_by_id(album_id)
    
    def get_artist_by_id(self, artist_id: int) -> Optional[Artist]:
        """
        Получает исполнителя по ID.
        """
        return self._artist_repository.get_by_id(artist_id)
    
    def get_tracks_by_album(self, album_id: int) -> List[Track]:
        """
        Получает все треки альбома.
        """
        return self._track_repository.get_by_album(album_id)
    
    def get_favorite_tracks(self, user_id: int) -> List[Track]:
        """
        Получает избранные треки пользователя.
        """
        return self._track_repository.get_favorites(user_id)
    
    def get_tags_by_type(self, tag_type: str) -> List[Tag]:
        """
        Получает теги определенного типа.
        """
        return self._tag_repository.get_by_type(tag_type)
    
    def save_user_tags(self, user_id: int, tag_ids: List[int]) -> bool:
        """
        Сохраняет выбранные пользователем теги (предпочтения).
        """
        return self._tag_repository.save_user_tags(user_id, tag_ids)

class SearchService:
    """
    Сервис для поиска музыкального контента.
    (Заглушка - в реальном приложении будет реализован полнотекстовый поиск)
    """
    def __init__(
        self,
        album_repository: IAlbumRepository,
        track_repository: ITrackRepository,
        artist_repository: IArtistRepository
    ):
        """
        Инициализирует сервис поиска.
        """
        self._album_repository = album_repository
        self._track_repository = track_repository
        self._artist_repository = artist_repository
    
    def search(self, query: str) -> dict:
        """
        Ищет музыкальный контент по запросу.
        """
        return {
            'tracks': [],    # Список найденных треков
            'albums': [],    # Список найденных альбомов
            'artists': []    # Список найденных исполнителей
        }