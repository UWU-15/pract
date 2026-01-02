from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from presentation.screens.base_screen import BaseScreen
from presentation.widgets.tag_button import TagButton
from presentation.dialogs.error_popup import ErrorPopup
import sqlite3
from config.settings import DB_PATH

Builder.load_string('''
<TagSelectionScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            
            Button:
                text: '< Back'
                size_hint_x: 0.2
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_release: root.go_back()
            
            Label:
                text: 'Select Tags'
                color: 1, 1, 1, 1
                font_size: sp(18)
                size_hint_x: 0.6
            
            Button:
                text: 'Done'
                size_hint_x: 0.2
                background_color: 0.5, 0, 1, 1
                color: 1, 1, 1, 1
                on_release: root.save_tags()
        
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height
                
                Label:
                    text: 'Genres'
                    color: 0.8, 0.8, 0.8, 1
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(30)
                
                GridLayout:
                    id: genres_grid
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                
                Label:
                    text: 'Vibes'
                    color: 0.8, 0.8, 0.8, 1
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(30)
                    padding_top: dp(20)
                
                GridLayout:
                    id: vibes_grid
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
''')

class TagSelectionScreen(BaseScreen):
    """
    Экран для выбора музыкальных предпочтений пользователя.
    """
    selected_tags = set()  # Множество выбранных тегов
    
    def on_pre_enter(self):
        """
        Вызывается перед показом экрана.
        Загружает список тегов из базы данных.
        """
        self.load_tags()
    
    def load_tags(self):
        """
        Загружает теги жанров и настроений из базы данных.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name FROM tags WHERE type = 'genre' ORDER BY name")
        genres = cursor.fetchall()
        
        cursor.execute("SELECT id, name FROM tags WHERE type = 'vibe' ORDER BY name")
        vibes = cursor.fetchall()
        
        conn.close()
        
        genres_grid = self.ids.genres_grid
        genres_grid.clear_widgets()
        
        for tag_id, name in genres:
            btn = TagButton(tag_id=tag_id, tag_name=name)
            genres_grid.add_widget(btn)
        
        vibes_grid = self.ids.vibes_grid
        vibes_grid.clear_widgets()
        
        for tag_id, name in vibes:
            btn = TagButton(tag_id=tag_id, tag_name=name)
            vibes_grid.add_widget(btn)
    
    def on_tag_toggle(self, tag_id, selected):
        """
        Обрабатывает выбор/отмену выбора тега.
        
        Параметры:
            tag_id (int): ID тега
            selected (bool): Флаг выбранного состояния
        """
        if selected:
            self.selected_tags.add(tag_id)
        else:
            self.selected_tags.discard(tag_id)
    
    def save_tags(self):
        """
        Сохраняет выбранные теги пользователя.
        """
        if len(self.selected_tags) < 3:
            error_popup = ErrorPopup(title='Selection Error', message='Please select at least 3 tags')
            error_popup.open()
            return
        
        app = MDApp.get_running_app()
        if not app.current_user_id:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Сохраняем выбранные теги пользователя
        for tag_id in self.selected_tags:
            cursor.execute(
                "INSERT OR IGNORE INTO user_tags (user_id, tag_id) VALUES (?, ?)",
                (app.current_user_id, tag_id)
            )
        
        # Отмечаем, что пользователь установил предпочтения
        cursor.execute(
            "UPDATE users SET preferences_set = 1 WHERE id = ?",
            (app.current_user_id,)
        )
        
        conn.commit()
        conn.close()
        
        # Переходим на главный экран
        self.manager.current = 'main'
    
    def go_back(self):
        """
        Возвращается на экран авторизации.
        """
        self.manager.current = 'login'