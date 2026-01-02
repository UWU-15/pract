from kivy.core.audio import SoundLoader
from core.interfaces import IAudioPlayer

class KivyAudioPlayer(IAudioPlayer):
    """
    Реализация аудио плеера на основе Kivy's SoundLoader.
    Реализует интерфейс IAudioPlayer.
    """
    def __init__(self):
        """
        Инициализирует аудио плеер.
        """
        self._sound = None  # Объект звука Kivy
    
    def load(self, file_path: str) -> bool:
        """
        Загружает аудио файл для воспроизведения.
        """
        self._sound = SoundLoader.load(file_path)
        return self._sound is not None
    
    def play(self) -> bool:
        """
        Начинает воспроизведение загруженного аудио.
        """
        if self._sound:
            self._sound.play()
            return True
        return False
    
    def pause(self) -> bool:
        """
        Приостанавливает воспроизведение.
        """
        if self._sound:
            self._sound.stop()  # В Kivy нет pause, используем stop
            return True
        return False
    
    def stop(self) -> bool:
        """
        Полностью останавливает воспроизведение.
        """
        if self._sound:
            self._sound.stop()
            return True
        return False
    
    def seek(self, position: float) -> bool:
        """
        Перемещает позицию воспроизведения.
        """
        if self._sound:
            try:
                self._sound.seek(position)
                return True
            except:
                # Некоторые форматы не поддерживают seek
                return False
        return False
    
    def get_position(self) -> float:
        """
        Получает текущую позицию воспроизведения.
        """
        if self._sound:
            return self._sound.get_pos() or 0
        return 0
    
    def get_length(self) -> float:
        """
        Получает общую длительность аудио файла.
        """
        if self._sound:
            return self._sound.length or 0
        return 0