import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit

class FileListWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создание виджета списка
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)  # Разрешение выбора нескольких элементов
        self.list_widget.setEditTriggers(QListWidget.EditTrigger.NoEditTriggers)  # Отключение редактирования элементов списка

        # Создание текстового поля для поиска
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.update_file_list)  # Обработчик изменения текста поиска

        # Создание вертикального компоновщика
        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.list_widget)

        # Установка компоновщика в виджет
        self.setLayout(layout)

    def update_file_list(self):
        self.list_widget.clear()

        folder_path = "KnowFaces"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = os.listdir(folder_path)

            # Фильтрация файлов по поисковому тексту
            search_text = self.search_box.text().lower()
            filtered_files = [file for file in files if search_text in file.lower()]

            # Добавление отфильтрованных файлов в виджет списка
            for file in filtered_files:
                item = QListWidgetItem(file)
                self.list_widget.addItem(item)

