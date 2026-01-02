import sqlite3
import os
from typing import Optional, List
from core.interfaces import (
    IUserRepository, IAlbumRepository, ITrackRepository, 
    IArtistRepository, ITagRepository
)
from core.models import User, Album, Track, Artist, Tag
from config.settings import DB_PATH
from config.constants import SQL_QUERIES

class DatabaseInitializer:
    """
    Класс для инициализации базы данных и добавления тестовых данных.
    """
    @staticmethod
    def init_database():
        """
        Инициализирует базу данных:
        1. Создает все необходимые таблицы
        2. Добавляет тестовые данные если таблицы пусты
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Создаем таблицы согласно схеме базы данных
        cursor.execute(SQL_QUERIES['CREATE_USERS'])      # Пользователи
        cursor.execute(SQL_QUERIES['CREATE_TAGS'])       # Теги (жанры, настроения)
        cursor.execute(SQL_QUERIES['CREATE_USER_TAGS'])  # Связь пользователей и тегов
        cursor.execute(SQL_QUERIES['CREATE_ARTISTS'])    # Исполнители
        cursor.execute(SQL_QUERIES['CREATE_ALBUMS'])     # Альбомы
        cursor.execute(SQL_QUERIES['CREATE_ALBUM_TAGS']) # Связь альбомов и тегов
        cursor.execute(SQL_QUERIES['CREATE_TRACKS'])     # Треки
        cursor.execute(SQL_QUERIES['CREATE_FAVORITES'])  # Избранные треки пользователей
        
        # Проверяем наличие тестовых данных
        cursor.execute("SELECT COUNT(*) FROM tags")
        if cursor.fetchone()[0] == 0:
            DatabaseInitializer._add_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def _add_sample_data(cursor):
        """
        Добавляет тестовые данные в базу данных.
        
        Добавляет:
        - Теги (жанры и настроения)
        - Исполнителей
        - Альбомы
        - Связи альбомов с тегами
        - Треки
        """
        # Теги (жанры и вайбы)
        tags = [
            ('Hip Hop', 'genre', '#9C27B0'),      # Фиолетовый
            ('Rock', 'genre', '#F44336'),         # Красный
            ('Industrial', 'genre', '#795548'),   # Коричневый
            ('Alternative', 'genre', '#FF5722'),  # Оранжевый
            ('Experimental', 'genre', '#607D8B'), # Сине-серый
            ('Aggressive', 'vibe', '#D32F2F'),    # Темно-красный
            ('Emotional', 'vibe', '#2196F3'),     # Синий
            ('Dark', 'vibe', '#212121'),          # Черный
            ('Epic', 'vibe', '#FF9800'),          # Оранжевый
            ('Melancholic', 'vibe', '#00BCD4'),   # Бирюзовый
            ('Energetic', 'vibe', '#4CAF50'),     # Зеленый
            ('Atmospheric', 'vibe', '#673AB7'),   # Темно-фиолетовый
            ('Raw', 'vibe', '#795548'),           # Коричневый
        ]
        cursor.executemany("INSERT INTO tags (name, type, color) VALUES (?, ?, ?)", tags)
        
        # Исполнители
        artists = [
            ('Kanye West', 'American rapper and producer', 'assets/covers/kanye_fantasy.png'),
            ('Limp Bizkit', 'American rap rock band', 'assets/covers/limp_significant.png'),
            ('Nine Inch Nails', 'American industrial rock band', 'assets/covers/nin_spiral.png'),
        ]
        cursor.executemany("INSERT INTO artists (name, bio, image_url) VALUES (?, ?, ?)", artists)
        
        # Получаем ID тегов и исполнителей для создания связей
        cursor.execute("SELECT id, name FROM tags")
        tag_ids = {name: id for id, name in cursor.fetchall()}
        
        cursor.execute("SELECT id, name FROM artists")
        artist_ids = {name: id for id, name in cursor.fetchall()}
        
        # Альбомы
        albums = [
            ('My Beautiful Dark Twisted Fantasy', artist_ids['Kanye West'], 2010,
             'assets/covers/kanye_fantasy.png',
             "Kanye West's critically acclaimed fifth studio album",
             "An exploration of fame, excess, and creativity through a surreal lens.",
             1),
            ('Significant Other', artist_ids['Limp Bizkit'], 1999,
             'assets/covers/limp_significant.png',
             "Limp Bizkit's breakthrough second studio album",
             "A raw expression of late-90s youth culture and angst.",
             1),
            ('The Downward Spiral', artist_ids['Nine Inch Nails'], 1994,
             'assets/covers/nin_spiral.png',
             "Nine Inch Nails' seminal second studio album",
             "A harrowing journey through depression, self-destruction, and rebirth.",
             1),
        ]
        cursor.executemany(
            """INSERT INTO albums (title, artist_id, release_year, cover_url, 
               description, lore_description, is_conceptual) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            albums
        )
        
        # Получаем ID альбомов для создания треков
        cursor.execute("SELECT id, title FROM albums")
        album_ids = {title: id for id, title in cursor.fetchall()}
        
        # Связываем альбомы с тегами
        album_tags = [
            (album_ids['My Beautiful Dark Twisted Fantasy'], tag_ids['Hip Hop']),
            (album_ids['My Beautiful Dark Twisted Fantasy'], tag_ids['Emotional']),
            (album_ids['My Beautiful Dark Twisted Fantasy'], tag_ids['Epic']),
            (album_ids['My Beautiful Dark Twisted Fantasy'], tag_ids['Melancholic']),
            (album_ids['Significant Other'], tag_ids['Rock']),
            (album_ids['Significant Other'], tag_ids['Aggressive']),
            (album_ids['Significant Other'], tag_ids['Energetic']),
            (album_ids['Significant Other'], tag_ids['Raw']),
            (album_ids['The Downward Spiral'], tag_ids['Industrial']),
            (album_ids['The Downward Spiral'], tag_ids['Experimental']),
            (album_ids['The Downward Spiral'], tag_ids['Dark']),
            (album_ids['The Downward Spiral'], tag_ids['Atmospheric']),
            (album_ids['The Downward Spiral'], tag_ids['Aggressive']),
        ]
        cursor.executemany("INSERT INTO album_tags (album_id, tag_id) VALUES (?, ?)", album_tags)
        
        # Треки
        tracks = [
            ('Dark Fantasy', album_ids['My Beautiful Dark Twisted Fantasy'], 1, 272, 'assets/tracks/kanye_power.mp3'),
            ('Power', album_ids['My Beautiful Dark Twisted Fantasy'], 2, 292, 'assets/tracks/kanye_runaway.mp3'),
            ('Runaway', album_ids['My Beautiful Dark Twisted Fantasy'], 3, 548, 'assets/tracks/kanye_lights.mp3'),
            ('Nookie', album_ids['Significant Other'], 1, 289, 'assets/tracks/limp_nookie.mp3'),
            ('Break Stuff', album_ids['Significant Other'], 2, 167, 'assets/tracks/limp_break.mp3'),
            ('Re-Arranged', album_ids['Significant Other'], 3, 306, 'assets/tracks/limp_nobody.mp3'),
            ('Mr. Self Destruct', album_ids['The Downward Spiral'], 1, 272, 'assets/tracks/nin_mr_self_destruct.mp3'),
            ('Closer', album_ids['The Downward Spiral'], 2, 371, 'assets/tracks/nin_closer.mp3'),
            ('Hurt', album_ids['The Downward Spiral'], 3, 378, 'assets/tracks/nin_hurt.mp3'),
        ]
        cursor.executemany(
            "INSERT INTO tracks (title, album_id, track_number, duration, audio_url) VALUES (?, ?, ?, ?, ?)",
            tracks
        )

class BaseRepository:
    """
    Базовый класс репозитория, предоставляющий подключение к базе данных.
    """
    def __init__(self):
        self.db_path = DB_PATH
    
    def _get_connection(self):
        """
        Создает и возвращает соединение с базой данных.
        """
        return sqlite3.connect(self.db_path)

class UserRepository(BaseRepository, IUserRepository):
    """
    Репозиторий для работы с пользователями.
    """
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, password, preferences_set FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(*row)
        return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Получает пользователя по имени пользователя.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, password, preferences_set FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(*row)
        return None
    
    def create(self, user: User) -> User:
        """
        Создает нового пользователя.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (user.username, user.password, user.email)
        )
        user.id = cursor.lastrowid  # Устанавливаем ID из базы данных
        conn.commit()
        conn.close()
        return user
    
    def update_preferences_set(self, user_id: int) -> bool:
        """
        Отмечает, что пользователь установил свои предпочтения.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET preferences_set = 1 WHERE id = ?",
            (user_id,)
        )
        conn.commit()
        affected = cursor.rowcount > 0
        conn.close()
        return affected

class AlbumRepository(BaseRepository, IAlbumRepository):
    """
    Репозиторий для работы с альбомами.
    """
    def get_by_id(self, album_id: int) -> Optional[Album]:
        """
        Получает альбом по ID с полной информацией.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.artist_id, a.release_year, a.cover_url,
                   a.description, a.lore_description, a.is_conceptual, ar.name
            FROM albums a
            JOIN artists ar ON a.artist_id = ar.id
            WHERE a.id = ?
        ''', (album_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            album = Album(
                id=row[0], title=row[1], artist_id=row[2], release_year=row[3],
                cover_url=row[4], description=row[5], lore_description=row[6],
                is_conceptual=bool(row[7]), artist_name=row[8]
            )
            
            # Загружаем теги альбома
            album.tags = self._get_album_tags(album_id)
            return album
        return None
    
    def get_by_artist(self, artist_id: int) -> List[Album]:
        """
        Получает все альбомы исполнителя.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.artist_id, a.release_year, a.cover_url,
                   a.description, a.lore_description, a.is_conceptual, ar.name
            FROM albums a
            JOIN artists ar ON a.artist_id = ar.id
            WHERE a.artist_id = ?
            ORDER BY a.release_year DESC
        ''', (artist_id,))
        rows = cursor.fetchall()
        conn.close()
        
        albums = []
        for row in rows:
            album = Album(
                id=row[0], title=row[1], artist_id=row[2], release_year=row[3],
                cover_url=row[4], description=row[5], lore_description=row[6],
                is_conceptual=bool(row[7]), artist_name=row[8]
            )
            album.tags = self._get_album_tags(album.id)
            albums.append(album)
        
        return albums
    
    def get_all(self) -> List[Album]:
        """
        Получает все альбомы (ограниченное количество).
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.artist_id, a.release_year, a.cover_url,
                   a.description, a.lore_description, a.is_conceptual, ar.name
            FROM albums a
            JOIN artists ar ON a.artist_id = ar.id
            LIMIT 10
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        albums = []
        for row in rows:
            album = Album(
                id=row[0], title=row[1], artist_id=row[2], release_year=row[3],
                cover_url=row[4], description=row[5], lore_description=row[6],
                is_conceptual=bool(row[7]), artist_name=row[8]
            )
            albums.append(album)
        
        return albums
    
    def get_recommendations(self, user_tags: List[int]) -> List[Album]:
        """
        Получает рекомендации альбомов на основе тегов пользователя.
        """
        if not user_tags:
            return self.get_all()[:3]  # Если нет тегов - возвращаем популярные
        
        conn = self._get_connection()
        cursor = conn.cursor()
        tag_ids = ','.join(map(str, user_tags))
        
        # SQL запрос для получения альбомов с тегами пользователя
        query = f'''
            SELECT DISTINCT a.id, a.title, a.artist_id, a.release_year, a.cover_url,
                   a.description, a.lore_description, a.is_conceptual, ar.name
            FROM albums a
            JOIN artists ar ON a.artist_id = ar.id
            JOIN album_tags at ON a.id = at.album_id
            WHERE at.tag_id IN ({tag_ids})
            LIMIT 6
        '''
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        albums = []
        for row in rows:
            album = Album(
                id=row[0], title=row[1], artist_id=row[2], release_year=row[3],
                cover_url=row[4], description=row[5], lore_description=row[6],
                is_conceptual=bool(row[7]), artist_name=row[8]
            )
            albums.append(album)
        
        return albums
    
    def _get_album_tags(self, album_id: int) -> List[Tag]:
        """
        Внутренний метод для получения тегов альбома.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.name, t.type, t.color
            FROM tags t
            JOIN album_tags at ON t.id = at.tag_id
            WHERE at.album_id = ?
        ''', (album_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Tag(id=row[0], name=row[1], type=row[2], color=row[3]) for row in rows]

class TrackRepository(BaseRepository, ITrackRepository):
    """
    Репозиторий для работы с треками.
    """
    def get_by_id(self, track_id: int) -> Optional[Track]:
        """
        Получает трек по ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.title, t.album_id, t.track_number, t.duration, t.audio_url,
                   a.title, ar.name
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            WHERE t.id = ?
        ''', (track_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Track(
                id=row[0], title=row[1], album_id=row[2], track_number=row[3],
                duration=row[4], audio_url=row[5], album_title=row[6], artist_name=row[7]
            )
        return None
    
    def get_by_album(self, album_id: int) -> List[Track]:
        """
        Получает все треки альбома.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.title, t.album_id, t.track_number, t.duration, t.audio_url,
                   a.title, ar.name
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            WHERE t.album_id = ?
            ORDER BY t.track_number
        ''', (album_id,))
        rows = cursor.fetchall()
        conn.close()
        
        tracks = []
        for row in rows:
            track = Track(
                id=row[0], title=row[1], album_id=row[2], track_number=row[3],
                duration=row[4], audio_url=row[5], album_title=row[6], artist_name=row[7]
            )
            tracks.append(track)
        
        return tracks
    
    def get_favorites(self, user_id: int) -> List[Track]:
        """
        Получает избранные треки пользователя.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.title, t.album_id, t.track_number, t.duration, t.audio_url,
                   a.title, ar.name
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            JOIN favorites f ON t.id = f.track_id
            WHERE f.user_id = ?
            ORDER BY f.added_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        tracks = []
        for row in rows:
            track = Track(
                id=row[0], title=row[1], album_id=row[2], track_number=row[3],
                duration=row[4], audio_url=row[5], album_title=row[6], artist_name=row[7]
            )
            tracks.append(track)
        
        return tracks

class ArtistRepository(BaseRepository, IArtistRepository):
    """
    Репозиторий для работы с исполнителями.
    """
    def get_by_id(self, artist_id: int) -> Optional[Artist]:
        """
        Получает исполнителя по ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, bio, image_url
            FROM artists
            WHERE id = ?
        ''', (artist_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Artist(id=row[0], name=row[1], bio=row[2], image_url=row[3])
        return None
    
    def search(self, query: str) -> List[Artist]:
        """
        Ищет исполнителей по имени.
        """
        search_term = f"%{query}%"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, bio, image_url
            FROM artists
            WHERE name LIKE ?
            ORDER BY name
            LIMIT 10
        ''', (search_term,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Artist(id=row[0], name=row[1], bio=row[2], image_url=row[3]) for row in rows]

class TagRepository(BaseRepository, ITagRepository):
    """
    Репозиторий для работы с тегами.
    """
    def get_all(self) -> List[Tag]:
        """
        Получает все теги.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, type, color FROM tags ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        return [Tag(id=row[0], name=row[1], type=row[2], color=row[3]) for row in rows]
    
    def get_by_type(self, tag_type: str) -> List[Tag]:
        """
        Получает теги определенного типа.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, type, color FROM tags WHERE type = ? ORDER BY name",
            (tag_type,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [Tag(id=row[0], name=row[1], type=row[2], color=row[3]) for row in rows]
    
    def save_user_tags(self, user_id: int, tag_ids: List[int]) -> bool:
        """
        Сохраняет теги пользователя (предпочтения).
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Удаляем старые теги пользователя
        cursor.execute("DELETE FROM user_tags WHERE user_id = ?", (user_id,))
        
        # Добавляем новые теги
        for tag_id in tag_ids:
            cursor.execute(
                "INSERT OR IGNORE INTO user_tags (user_id, tag_id) VALUES (?, ?)",
                (user_id, tag_id)
            )
        
        conn.commit()
        conn.close()
        return True