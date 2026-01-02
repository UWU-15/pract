# Мобильное приложение для знакомства с концептуальными и лорными альбомами. Приложение предоставляет детальную информацию о лоре, концепции и сюжете альбомов, а также интеллектуальные рекомендации на основе специальных тегов (вайб, сюжет).

# Структура:
│   main.py
│   README.md
│   requirements.txt
│
├───assets
│   ├───covers
│   │       default.png
│   │       kanye_fantasy.png
│   │       limp_significant.png
│   │       nin_spiral.png
│   │
│   └───tracks
│           kanye_lights.mp3
│           kanye_power.mp3
│           kanye_runaway.mp3
│           limp_break.mp3
│           limp_nobody.mp3
│           limp_nookie.mp3
│           nin_closer.mp3
│           nin_hurt.mp3
│           nin_mr_self_destruct.mp3
│
├───config
│   │   constants.py
│   │   settings.py
│   │   __init__.py
│   │
│   └───__pycache__
│
├───core
│   │   interfaces.py
│   │   models.py
│   │   services.py
│   │   __init__.py
│   │
│   └───__pycache__
│
├───data
│       music_app.db
│
├───infrastructure
│   │   __init__.py
│   │
│   ├───audio
│   │   │   kivy_audio_player.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │
│   ├───database
│   │   │   sqlite_repository.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │
│   └───__pycache__
│
├───presentation
│   │   app.py
│   │   __init__.py
│   │
│   ├───dialogs
│   │   │   error_popup.py
│   │   │   menu_popup.py
│   │   │   register_popup.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │
│   ├───screens
│   │   │   album_screen.py
│   │   │   artist_screen.py
│   │   │   base_screen.py
│   │   │   favorites_screen.py
│   │   │   login_screen.py
│   │   │   main_screen.py
│   │   │   player_screen.py
│   │   │   search_screen.py
│   │   │   tag_selection_screen.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │
│   ├───widgets
│   │   │   album_card.py
│   │   │   artist_card.py
│   │   │   tag_button.py
│   │   │   track_item.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │
│   └───__pycache__
└───utils
    │   helpers.py
    │   validators.py
    │   __init__.py
    │
    └───__pycache__

# Основные возможности:
1) Музыкальный плеер с базовыми функциями воспроизведения
2) Информация о лоре и концепции альбомов
3) Специальные теги для вайба и сюжета
4) Персональные рекомендации на основе предпочтений
5) Поиск по альбомам, исполнителям и трекам
6) Избранное
7) Регистрация и настройка музыкальных предпочтений

# Установка:
# 1. Клонировать или скачать проект
Если у вас Git:
git clone <URL_вашего_репозитория>
cd music_lore_app
# 2. Создать виртуальное окружение
python -m venv venv
# 3. Активировать окружение
В CMD:
venv\Scripts\activate
В PowerShell:
.\venv\Scripts\Activate.ps1
# 4. Установить зависимости
pip install -r requirements.txt
# 5. Запустить приложение
python main.py