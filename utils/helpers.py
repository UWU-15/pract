import os
from config.settings import DEFAULT_COVER, DEFAULT_IMAGE

def ensure_file_exists(file_path: str, default_path: str = None) -> str:
    """Проверяет существование файла, возвращает путь к дефолтному если файл не существует"""
    if file_path and os.path.exists(file_path):
        return file_path
    
    if default_path and os.path.exists(default_path):
        return default_path
    
    return DEFAULT_COVER

def create_placeholder_files():
    """Создает placeholder файлы для тестирования"""
    test_audio_files = [
        'assets/tracks/kanye_power.mp3',
        'assets/tracks/kanye_runaway.mp3',
        'assets/tracks/kanye_lights.mp3',
        'assets/tracks/limp_nookie.mp3',
        'assets/tracks/limp_break.mp3',
        'assets/tracks/limp_nobody.mp3',
        'assets/tracks/nin_mr_self_destruct.mp3',
        'assets/tracks/nin_closer.mp3',
        'assets/tracks/nin_hurt.mp3'
    ]
    
    for file_path in test_audio_files:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                pass
    
    # Создаем файл обложки по умолчанию если его нет
    if not os.path.exists(DEFAULT_COVER):
        try:
            with open(DEFAULT_COVER, 'wb') as f:
                f.write(b'')
        except:
            pass