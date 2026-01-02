# Константы приложения
DEFAULT_COVER = 'assets/covers/default.png'
DEFAULT_IMAGE = 'assets/covers/default.png'

# Сообщения об ошибках
ERROR_TITLES = {
    'LOGIN': 'Login Error',
    'REGISTRATION': 'Registration Error',
    'SELECTION': 'Selection Error',
    'VALIDATION': 'Validation Error'
}

# SQL запросы
SQL_QUERIES = {
    'CREATE_USERS': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            preferences_set BOOLEAN DEFAULT 0
        )
    ''',
    'CREATE_TAGS': '''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            color TEXT DEFAULT '#2196F3'
        )
    ''',
    'CREATE_USER_TAGS': '''
        CREATE TABLE IF NOT EXISTS user_tags (
            user_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (user_id, tag_id)
        )
    ''',
    'CREATE_ARTISTS': '''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            bio TEXT,
            image_url TEXT
        )
    ''',
    'CREATE_ALBUMS': '''
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist_id INTEGER,
            release_year INTEGER,
            cover_url TEXT,
            description TEXT,
            lore_description TEXT,
            is_conceptual BOOLEAN DEFAULT 0,
            FOREIGN KEY (artist_id) REFERENCES artists(id)
        )
    ''',
    'CREATE_ALBUM_TAGS': '''
        CREATE TABLE IF NOT EXISTS album_tags (
            album_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (album_id, tag_id)
        )
    ''',
    'CREATE_TRACKS': '''
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            album_id INTEGER,
            track_number INTEGER,
            duration INTEGER,
            audio_url TEXT,
            FOREIGN KEY (album_id) REFERENCES albums(id)
        )
    ''',
    'CREATE_FAVORITES': '''
        CREATE TABLE IF NOT EXISTS favorites (
            user_id INTEGER,
            track_id INTEGER,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, track_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (track_id) REFERENCES tracks(id)
        )
    '''
}