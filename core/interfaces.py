from abc import ABC, abstractmethod
from typing import Optional, List
from core.models import User, Album, Track, Artist, Tag

class IUserRepository(ABC):
    """
    Интерфейс репозитория для работы с пользователями.
    """
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по ID.
        """
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Получает пользователя по имени пользователя.
        """
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        """
        Создает нового пользователя.
        """
        pass
    
    @abstractmethod
    def update_preferences_set(self, user_id: int) -> bool:
        """
        Отмечает, что пользователь установил свои предпочтения.
        """
        pass

class IAlbumRepository(ABC):
    """
    Интерфейс репозитория для работы с альбомами.
    """
    @abstractmethod
    def get_by_id(self, album_id: int) -> Optional[Album]:
        """
        Получает альбом по ID.
        """
        pass
    
    @abstractmethod
    def get_by_artist(self, artist_id: int) -> List[Album]:
        """
        Получает все альбомы исполнителя.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Album]:
        """
        Получает все альбомы.
        """
        pass
    
    @abstractmethod
    def get_recommendations(self, user_tags: List[int]) -> List[Album]:
        """
        Получает рекомендации альбомов на основе тегов пользователя.
        """
        pass

class ITrackRepository(ABC):
    """
    Интерфейс репозитория для работы с треками.
    """
    @abstractmethod
    def get_by_id(self, track_id: int) -> Optional[Track]:
        """
        Получает трек по ID.
        """
        pass
    
    @abstractmethod
    def get_by_album(self, album_id: int) -> List[Track]:
        """
        Получает все треки альбома.
        """
        pass
    
    @abstractmethod
    def get_favorites(self, user_id: int) -> List[Track]:
        """
        Получает избранные треки пользователя.
        """
        pass

class IArtistRepository(ABC):
    """
    Интерфейс репозитория для работы с исполнителями.
    """
    @abstractmethod
    def get_by_id(self, artist_id: int) -> Optional[Artist]:
        """
        Получает исполнителя по ID.
        """
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Artist]:
        """
        Ищет исполнителей по имени.
        """
        pass

class ITagRepository(ABC):
    """
    Интерфейс репозитория для работы с тегами.
    """
    @abstractmethod
    def get_all(self) -> List[Tag]:
        """
        Получает все теги.
        """
        pass
    
    @abstractmethod
    def get_by_type(self, tag_type: str) -> List[Tag]:
        """
        Получает теги определенного типа.
        """
        pass
    
    @abstractmethod
    def save_user_tags(self, user_id: int, tag_ids: List[int]) -> bool:
        """
        Сохраняет теги пользователя (его предпочтения).
        """
        pass

class IAudioPlayer(ABC):
    """
    Интерфейс аудио плеера.
    """
    @abstractmethod
    def load(self, file_path: str) -> bool:
        """
        Загружает аудио файл для воспроизведения.
        """
        pass
    
    @abstractmethod
    def play(self) -> bool:
        """
        Начинает воспроизведение загруженного аудио.
        """
        pass
    
    @abstractmethod
    def pause(self) -> bool:
        """
        Приостанавливает воспроизведение.
        """
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """
        Полностью останавливает воспроизведение.
        """
        pass
    
    @abstractmethod
    def seek(self, position: float) -> bool:
        """
        Перемещает позицию воспроизведения.
        """
        pass
    
    @abstractmethod
    def get_position(self) -> float:
        """
        Получает текущую позицию воспроизведения.
        """
        pass
    
    @abstractmethod
    def get_length(self) -> float:
        """
        Получает общую длительность аудио файла.
        """
        pass