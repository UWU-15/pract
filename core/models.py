from dataclasses import dataclass
from typing import Optional, List

@dataclass
class User:
    """
    Модель пользователя приложения.
    """
    id: int
    username: str
    email: str
    password: str
    preferences_set: bool = False

@dataclass
class Tag:
    """
    Модель тега для категоризации музыки.
    """
    id: int
    name: str
    type: str
    color: str = '#2196F3' 

@dataclass
class Artist:
    """
    Модель музыкального исполнителя.
    """
    id: int
    name: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

@dataclass
class Album:
    """
    Модель музыкального альбома.
    """
    id: int
    title: str
    artist_id: int
    release_year: int
    cover_url: Optional[str] = None
    description: Optional[str] = None
    lore_description: Optional[str] = None
    is_conceptual: bool = False
    artist_name: Optional[str] = None
    tags: List[Tag] = None
    
    def __post_init__(self):
        """
        Инициализирует список тегов если он не был передан.
        Вызывается автоматически после __init__ в dataclass.
        """
        if self.tags is None:
            self.tags = []

@dataclass
class Track:
    """
    Модель музыкального трека.
    """
    id: int
    title: str
    album_id: int
    track_number: int
    duration: int
    audio_url: str
    album_title: Optional[str] = None
    artist_name: Optional[str] = None