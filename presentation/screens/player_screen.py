from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivymd.app import MDApp
from presentation.screens.base_screen import BaseScreen
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty
)
from kivy.clock import Clock
import sqlite3
import os
import time
import pygame
from config.settings import DB_PATH
from utils.helpers import ensure_file_exists

Builder.load_string('''
<PlayerScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            
            Button:
                text: '‹ Back'
                size_hint_x: 0.2
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.go_back()
            
            Label:
                text: 'Now Playing'
                color: 1, 1, 1, 1
                font_size: sp(18)
                size_hint_x: 0.6
                halign: 'center'
            
            Button:
                text: 'Fav'
                size_hint_x: 0.2
                background_color: (0.7, 0, 0, 1) if root.is_favorite else (0.3, 0.3, 0.3, 1)
                color: 1, 1, 1, 1
                on_release: root.toggle_favorite()
        
        BoxLayout:
            orientation: 'vertical'
            padding: dp(40)
            spacing: dp(40)
            
            Image:
                source: root.album_cover
                size_hint_y: 0.6
                allow_stretch: True
                keep_ratio: False
            
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(10)
                size_hint_y: 0.2
                
                Label:
                    text: root.track_title
                    color: 1, 1, 1, 1
                    font_size: sp(22)
                    size_hint_y: None
                    height: dp(40)
                    text_size: self.width, None
                    halign: 'center'
                    shorten: True
                
                Label:
                    text: root.track_artist
                    color: 0.7, 0.7, 0.7, 1
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: 'center'
                    shorten: True
            
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                size_hint_y: 0.1
                
                BoxLayout:
                    size_hint_y: None
                    height: dp(20)
                    
                    Label:
                        id: current_time_label
                        text: '0:00'
                        color: 0.7, 0.7, 0.7, 1
                        font_size: sp(12)
                        size_hint_x: 0.1
                    
                    Label:
                        text: '-'
                        color: 0.7, 0.7, 0.7, 1
                        font_size: sp(12)
                        size_hint_x: 0.8
                        halign: 'center'
                    
                    Label:
                        id: total_time_label
                        text: '0:00'
                        color: 0.7, 0.7, 0.7, 1
                        font_size: sp(12)
                        size_hint_x: 0.1
                        halign: 'right'
                
                Slider:
                    id: progress_slider
                    min: 0
                    max: 100
                    value: 0
                    on_touch_down: root.on_slider_touch_down(*args)
                    on_touch_up: root.on_slider_touch_up(*args)
                    cursor_size: [dp(20), dp(20)]
            
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.2
                padding: [0, 20]
                spacing: dp(30)
                
                Button:
                    text: 'Previous'
                    font_size: sp(10)
                    background_color: 0.3, 0.3, 0.3, 1
                    color: 1, 1, 1, 1
                    size_hint_x: 0.2
                    on_release: root.prev_track()
                
                Button:
                    id: play_pause_btn
                    text: 'Stop' if not root.is_playing else 'Play'
                    font_size: sp(20)
                    background_color: 0.5, 0, 1, 1
                    color: 1, 1, 1, 1
                    size_hint_x: 0.4
                    on_release: root.toggle_play()
                
                Button:
                    text: 'Next'
                    font_size: sp(10)
                    background_color: 0.3, 0.3, 0.3, 1
                    color: 1, 1, 1, 1
                    size_hint_x: 0.2
                    on_release: root.next_track()
''')


class SimplePlayer:
    """
    Простейший аудио плеер на основе pygame.mixer.
    """
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        self.volume = 0.7
        self.playing = False
        self.paused = False
        self.current_file = None
        self.track_length = 0
        self.current_position = 0
        self._play_start_time = 0
        self._play_start_position = 0
        print("SimplePlayer инициализирован")
        
    def load(self, file_path):
        """Загружает аудио файл для воспроизведения."""
        try:
            if not os.path.exists(file_path):
                print(f"Файл не найден: {file_path}")
                return False
            
            self.current_file = file_path
            self.current_position = 0
            self._play_start_time = 0
            self._play_start_position = 0
            
            try:
                sound = pygame.mixer.Sound(file_path)
                self.track_length = sound.get_length()
                print(f"Длительность трека: {self.track_length:.2f} сек")
            except Exception as e:
                print(f"Не удалось получить длительность: {e}")
                self.track_length = 180
            
            print(f"Загружен: {os.path.basename(file_path)} ({self.track_length:.1f}с)")
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False
    
    def play(self):
        """Начинает или возобновляет воспроизведение."""
        if not self.current_file:
            return False
        
        try:
            if self.paused:
                # Возобновить с паузы
                pygame.mixer.music.unpause()
                self.paused = False
                self.playing = True
                self._play_start_time = time.time()
                print(f"Возобновлено воспроизведение с {self.current_position:.1f}с")
            else:
                # Начать с текущей позиции
                pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.play(start=self.current_position)
                pygame.mixer.music.set_volume(self.volume)
                self.playing = True
                self.paused = False
                self._play_start_time = time.time()
                self._play_start_position = self.current_position
                print(f"Начато воспроизведение с {self.current_position:.1f}с")
            
            return True
            
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")
            return False
    
    def pause(self):
        """Приостанавливает воспроизведение."""
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.playing = False
            
            # Обновляем текущую позицию при паузе
            elapsed = time.time() - self._play_start_time
            self.current_position = self._play_start_position + elapsed
            
            print(f"Пауза на позиции {self.current_position:.1f}с")
            return True
        return False
    
    def stop(self):
        """Полностью останавливает воспроизведение."""
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.current_position = 0
        self._play_start_time = 0
        self._play_start_position = 0
        print("Остановлено")
        return True
    
    def seek(self, position):
        """Перематывает к указанной позиции."""
        try:
            if self.track_length > 0:
                position = max(0.0, min(position, self.track_length))
                print(f"Перемотка к {position:.1f}с")
                
                # Сохраняем позицию
                self.current_position = position
                
                # Если трек играл, перезапускаем с новой позиции
                if self.playing and not self.paused:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.current_file)
                    pygame.mixer.music.play(start=position)
                    pygame.mixer.music.set_volume(self.volume)
                    self._play_start_time = time.time()
                    self._play_start_position = position
                    print(f"Перезапущено с {position:.1f}с")
                else:
                    print(f"Позиция сохранена: {position:.1f}с")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Ошибка перемотки: {e}")
            return False
    
    def _update_position(self):
        """Обновляет текущую позицию на основе времени."""
        if self.playing and not self.paused:
            elapsed = time.time() - self._play_start_time
            self.current_position = self._play_start_position + elapsed
            return self.current_position
        return self.current_position
    
    def update_position(self):
        """Обновляет текущую позицию (для регулярного вызова)."""
        try:
            if self.playing and not self.paused:
                # Обновляем позицию на основе времени
                self._update_position()
                
                # Простая проверка окончания трека
                if self.current_position >= self.track_length - 0.3:
                    print(f"Трек почти закончен: {self.current_position:.1f}/{self.track_length:.1f}")
                    self.playing = False
                    self.paused = False
                    self.current_position = self.track_length
                    return True
                
                # Дополнительная проверка через pygame
                pos_ms = pygame.mixer.music.get_pos()
                if pos_ms == -1 and self.current_position >= self.track_length - 1.0:
                    print(f"Pygame сообщает об окончании трека")
                    self.playing = False
                    self.paused = False
                    self.current_position = self.track_length
                    return True
            
            return False
                
        except Exception as e:
            print(f"Ошибка обновления позиции: {e}")
            return False
    
    def get_position(self):
        """Возвращает текущую позицию воспроизведения."""
        return self.current_position
    
    def get_length(self):
        """Возвращает длительность текущего трека."""
        return self.track_length


class PlayerScreen(BaseScreen):
    """
    Экран аудио плеера для воспроизведения треков.
    """
    track_title = StringProperty('')
    track_artist = StringProperty('')
    album_cover = StringProperty('')
    current_time = NumericProperty(0)
    total_time = NumericProperty(0)
    is_playing = BooleanProperty(False)
    is_favorite = BooleanProperty(False)
    current_track_id = NumericProperty(0)
    current_context = StringProperty('single')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.progress_updater = None
        self.player = SimplePlayer()
        self.playlist = None
        self._is_slider_dragging = False
        self._slider_value_before_drag = 0
        self._track_ended = False
        print("PlayerScreen инициализирован")
    
    def on_enter(self):
        """Вызывается при входе на экран."""
        self.start_progress_updater()
    
    def on_leave(self):
        """Вызывается при выходе с экрана."""
        self.stop_progress_updater()
    
    def start_progress_updater(self):
        """Запускает обновление прогресса воспроизведения."""
        self.stop_progress_updater()
        self.progress_updater = Clock.schedule_interval(self.update_progress, 0.1)
    
    def stop_progress_updater(self):
        """Останавливает обновление прогресса воспроизведения."""
        if self.progress_updater:
            self.progress_updater.cancel()
            self.progress_updater = None
    
    def update_progress(self, dt):
        """Обновляет прогресс воспроизведения."""
        try:
            # Обновляем позицию в плеере
            track_ended = self.player.update_position()
            
            # Получаем текущую позицию
            current_pos = self.player.get_position()
            self.current_time = current_pos
            
            if not self._is_slider_dragging:
                if hasattr(self, 'ids') and 'progress_slider' in self.ids:
                    if self.total_time > 0:
                        progress = (current_pos / self.total_time) * 100
                        progress = max(0.0, min(progress, 100.0))
                        self.ids.progress_slider.value = progress
            
            # Обновляем метки времени
            self._update_time_labels()
            
            # Проверка окончания трека
            if track_ended and not self._track_ended:
                self._track_ended = True
                print("Обнаружено окончание трека")
                Clock.schedule_once(lambda dt: self.on_track_end(), 0.3)
                    
        except Exception as e:
            print(f"Ошибка обновления прогресса: {e}")
    
    def _update_time_labels(self):
        """Обновляет метки времени."""
        if hasattr(self, 'ids'):
            # Текущее время
            if 'current_time_label' in self.ids:
                display_time = min(self.current_time, self.total_time)
                minutes = int(display_time // 60)
                seconds = int(display_time % 60)
                self.ids.current_time_label.text = f"{minutes}:{seconds:02d}"
            
            # Общее время
            if 'total_time_label' in self.ids and self.total_time > 0:
                minutes = int(self.total_time // 60)
                seconds = int(self.total_time % 60)
                self.ids.total_time_label.text = f"{minutes}:{seconds:02d}"
    
    def on_slider_touch_down(self, slider, touch):
        """Обрабатывает начало перетаскивания слайдера."""
        if slider.collide_point(*touch.pos):
            self._is_slider_dragging = True
            self._slider_value_before_drag = slider.value
            print(f"Начато перетаскивание слайдера: {slider.value}%")
            return True
        return False
    
    def on_slider_touch_up(self, slider, touch):
        """Обрабатывает отпускание слайдера."""
        if self._is_slider_dragging:
            self._is_slider_dragging = False
            
            slider_value = slider.value
            if self.total_time > 0:
                position = (slider_value / 100.0) * self.total_time
                
                self._track_ended = False
                
                if self.player.seek(position):
                    self.current_time = position
                    
                    if hasattr(self, 'ids') and 'progress_slider' in self.ids:
                        self.ids.progress_slider.value = slider_value
                    
                    self._update_time_labels()
                    
                    print(f"Перемотка завершена: позиция {position:.1f}с ({slider_value:.1f}%)")

        return True
    
    def on_track_end(self):
        """Обрабатывает окончание трека."""
        print(f"on_track_end: Трек полностью завершен, контекст: {self.current_context}")
        
        self.is_playing = False
        self.current_time = self.total_time
        
        if hasattr(self, 'ids') and 'progress_slider' in self.ids:
            self.ids.progress_slider.value = 100
        
        self._update_time_labels()
        
        # Автопереключение на следующий трек
        if self.current_context in ['album', 'favorites']:
            print("Автопереключение на следующий трек через 1 секунду")
            Clock.schedule_once(lambda dt: self.next_track(), 1.0)
    
    def load_track(self, track_id, context='single'):
        """Загружает трек для воспроизведения."""
        print(f"Загрузка трека: {track_id}, контекст: {context}")
        self.current_context = context
        self._track_ended = False
        
        # Загружаем информацию о треке
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.title, ar.name, a.cover_url, t.audio_url, t.duration, t.album_id
            FROM tracks t
            JOIN albums a ON t.album_id = a.id
            JOIN artists ar ON a.artist_id = ar.id
            WHERE t.id = ?
        ''', (track_id,))
        
        track_data = cursor.fetchone()
        conn.close()
        
        if not track_data:
            print(f"Трек {track_id} не найден")
            return
        
        title, artist, cover_url, audio_url, duration, album_id = track_data
        
        # Останавливаем текущий трек
        self.player.stop()
        
        # Устанавливаем данные
        self.track_title = title
        self.track_artist = artist
        self.album_cover = ensure_file_exists(cover_url)
        self.total_time = duration
        self.current_track_id = track_id
        self.current_time = 0
        self.is_playing = False
        self.current_album_id = album_id
        
        self.check_favorite_status()
        self._update_time_labels()
        
        if hasattr(self, 'ids') and 'progress_slider' in self.ids:
            self.ids.progress_slider.value = 0
        
        # Создаем плейлист
        self._create_playlist_for_context(context, track_id)
        
        # Загружаем аудиофайл
        if audio_url and os.path.exists(audio_url):
            if self.player.load(audio_url):
                print(f"Трек загружен: {title}")
                self.start_progress_updater()
                
                # Автозапуск
                if self.player.play():
                    self.is_playing = True
            else:
                print(f"Ошибка загрузки аудио")
        else:
            print(f"Аудиофайл не найден: {audio_url}")
    
    def _create_playlist_for_context(self, context, current_track_id):
        """Создает плейлист для контекста воспроизведения."""
        self.playlist = Playlist()
        
        if context == 'album' and hasattr(self, 'current_album_id'):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM tracks 
                WHERE album_id = ? 
                ORDER BY track_number
            ''', (self.current_album_id,))
            
            tracks = cursor.fetchall()
            conn.close()
            
            for track in tracks:
                self.playlist.append(track[0])
            
            self.playlist.set_current(current_track_id)
            
        elif context == 'favorites' and self.app.current_user_id:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT track_id FROM favorites 
                WHERE user_id = ?
                ORDER BY added_at DESC
            ''', (self.app.current_user_id,))
            
            tracks = cursor.fetchall()
            conn.close()
            
            for track in tracks:
                self.playlist.append(track[0])
            
            self.playlist.set_current(current_track_id)
            
        else:
            self.playlist.append(current_track_id)
            self.playlist.set_current(current_track_id)
    
    def check_favorite_status(self):
        """Проверяет, находится ли текущий трек в избранном."""
        if not self.app.current_user_id:
            self.is_favorite = False
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM favorites WHERE user_id = ? AND track_id = ?",
            (self.app.current_user_id, self.current_track_id)
        )
        result = cursor.fetchone()
        self.is_favorite = result is not None
        conn.close()
    
    def toggle_play(self):
        """Включает/выключает воспроизведение."""
        try:
            if self.is_playing:
                if self.player.pause():
                    self.is_playing = False
            else:
                if self.player.play():
                    self.is_playing = True
                    self._track_ended = False
                
        except Exception as e:
            print(f"Ошибка переключения воспроизведения: {e}")
    
    def toggle_favorite(self):
        """Добавляет/удаляет текущий трек из избранного."""
        if not self.app.current_user_id:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if self.is_favorite:
            cursor.execute(
                "DELETE FROM favorites WHERE user_id = ? AND track_id = ?",
                (self.app.current_user_id, self.current_track_id)
            )
            self.is_favorite = False
        else:
            cursor.execute(
                "INSERT OR IGNORE INTO favorites (user_id, track_id) VALUES (?, ?)",
                (self.app.current_user_id, self.current_track_id)
            )
            self.is_favorite = True
        
        conn.commit()
        conn.close()
    
    def next_track(self):
        """Переходит к следующему треку в плейлисте."""
        print("Следующий трек")
        
        if self.playlist and self.playlist.length > 1:
            next_track_id = self.playlist.next()
            if next_track_id and next_track_id != self.current_track_id:
                self.load_track(next_track_id, self.current_context)
            else:
                print("Следующий трек не доступен")
        else:
            print("В плейлисте только один трек")
    
    def prev_track(self):
        """Переходит к предыдущему треку в плейлисте."""
        print("Предыдущий трек")
        
        if self.current_time > 3:
            if self.player.seek(0):
                self.current_time = 0
                self._track_ended = False
                self._update_time_labels()
                if hasattr(self, 'ids') and 'progress_slider' in self.ids:
                    self.ids.progress_slider.value = 0
            return
        
        if self.playlist and self.playlist.length > 1:
            prev_track_id = self.playlist.prev()
            if prev_track_id and prev_track_id != self.current_track_id:
                self.load_track(prev_track_id, self.current_context)
            else:
                print("Предыдущий трек не доступен")
        else:
            print("В плейлисте только один трек")
    
    def go_back(self):
        """Возвращается на главный экран."""
        self.stop_progress_updater()
        self.player.stop()
        self.manager.current = 'main'


class Playlist:
    """
    Простой кольцевой плейлист.
    """
    def __init__(self):
        self.head = None
        self.current = None
        self.length = 0
    
    def append(self, track_id):
        new_node = TrackNode(track_id)
        
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node
        else:
            tail = self.head.prev
            
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node
        
        self.length += 1
    
    def set_current(self, track_id):
        if self.head is None:
            return False
        
        node = self.head
        for _ in range(self.length):
            if node.track_id == track_id:
                self.current = node
                return True
            node = node.next
        
        return False
    
    def next(self):
        if self.current:
            self.current = self.current.next
            return self.current.track_id
        return None
    
    def prev(self):
        if self.current:
            self.current = self.current.prev
            return self.current.track_id
        return None


class TrackNode:
    """
    Узел двусвязного списка для плейлиста.
    """
    def __init__(self, track_id):
        self.track_id = track_id
        self.next = None
        self.prev = None