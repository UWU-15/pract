import os

# Настройки окна
WINDOW_SIZE = (360, 640)

# Пути к файлам
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
COVERS_DIR = os.path.join(ASSETS_DIR, 'covers')
TRACKS_DIR = os.path.join(ASSETS_DIR, 'tracks')
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'music_app.db')

# Дефолтные изображения
DEFAULT_COVER = os.path.join(COVERS_DIR, 'default.png')
DEFAULT_IMAGE = os.path.join(COVERS_DIR, 'default.png')

# Создаем папки
os.makedirs(COVERS_DIR, exist_ok=True)
os.makedirs(TRACKS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)