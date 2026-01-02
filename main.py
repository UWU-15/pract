import os
import sys

# Добавляем корневую директорию проекта в путь Python
# Это позволяет импортировать модули из текущей директории и её поддиректорий
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Проверяем наличие необходимых папок для работы приложения
# Если какие-то папки отсутствуют - создаём их
required_folders = [
    'config',           # Конфигурационные файлы
    'core',             # Основная логика приложения
    'infrastructure',   # Инфраструктурный код (база данных, сеть и т.д.)
    'presentation',     # Презентационный слой (GUI, CLI)
    'utils',            # Вспомогательные утилиты
    'assets',           # Ресурсы приложения
    'assets/covers',    # Обложки музыкальных треков
    'assets/tracks',    # Аудиофайлы треков
    'data'              # Данные приложения
]

# Для каждой требуемой папки проверяем её существование
for folder in required_folders:
    folder_path = os.path.join(current_dir, folder)
    if not os.path.exists(folder_path):
        # Создаём папку (если уже существует - игнорируем)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder}")

try:
    # Пытаемся импортировать главный класс приложения
    from presentation.app import MusicLoreApp
    print("Successfully imported MusicLoreApp")
    
    # Стандартная проверка для запуска основного кода только при прямом выполнении файла
    if __name__ == '__main__':
        # Создаём экземпляр приложения
        app = MusicLoreApp()
        # Запускаем главный цикл приложения
        app.run()
        
except ImportError as e:
    # Обработка ошибки импорта - если не удалось найти необходимые модули
    print(f"Import error: {e}")
    print("Current Python path:")
    # Выводим текущие пути поиска модулей для отладки
    for path in sys.path:
        print(f"  {path}")
    # Ждём нажатия Enter перед выходом, чтобы пользователь мог увидеть сообщение об ошибке
    input("Press Enter to exit...")