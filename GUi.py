from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy

import os
import shutil
import glob

from computer_vision import huntface
from FileListWidget import FileListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FaceHunter")

        # Создание основного виджета и вертикального компоновщика
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Создание элементов интерфейса
        label = QLabel("FaceHunter")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Установка выравнивания по центру
        label_textbox1 = QLabel("Enter your path to you image.")
        label_textbox2 = QLabel("Enter ferst and second name the person in the image.")
        textbox1 = QLineEdit()
        textbox2 = QLineEdit()
        button_send = QPushButton("Send")
        self.label_confirmation = QLabel("", self)
        file_list_widget = FileListWidget()
        update_button = QPushButton("Update")
        Label_texbox_delete = QLabel("Enter ferst and second name with file type, for delete photo from database.")
        textbox_delete = QLineEdit()
        button_delete = QPushButton("Delete")
        self.label_confirmation_del = QLabel("", self)
        button_start = QPushButton("Start hunting")

        # Создание горизонтального компоновщика для меток и полей ввода
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label_textbox1)
        hbox1.addWidget(label_textbox2)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(textbox1)
        hbox2.addWidget(textbox2)


        # Растягивающийся элемент для выравнивания по центру
        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Установка выравнивания по правому краю для label_textbox2
        label_textbox2.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Установка выравнивания по левому краю
        label_textbox1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Добавление элементов в компоновщик
        layout.addWidget(label)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(button_send)
        layout.addWidget(self.label_confirmation)
        layout.addWidget(file_list_widget)
        layout.addWidget(update_button)
        layout.addWidget(Label_texbox_delete)
        layout.addWidget(textbox_delete)
        layout.addWidget(button_delete)
        layout.addWidget(self.label_confirmation_del)
        layout.addWidget(button_start)

        # Подключение слота к сигналу нажатия кнопки
        button_start.clicked.connect(self.button_start_clicked)
        button_send.clicked.connect(lambda: self.send_path_to_image(textbox1.text(), textbox2.text()))
        button_delete.clicked.connect(lambda: self.delete_image(textbox_delete.text()))
        update_button.clicked.connect(file_list_widget.update_file_list)

        # Установка виджета в качестве центрального
        self.setCentralWidget(widget)
        self.label_confirmation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_confirmation_del.setAlignment(Qt.AlignmentFlag.AlignCenter)



        # Изменение размера окна
        self.resize(650, 300)  # Установите требуемые размеры окна

    # Обработчик запуска распознования по лицу 
    def button_start_clicked(self):
        huntface()


    # Функция добаления фотографии в папку knowfaces
    def send_path_to_image(self, text1, text2):
        # Проверка существования файла
        if not os.path.exists(text1):
            print(f"Файл '{text1}' не существует")
            self.label_confirmation.setText(f"Файл '{text1}' не существует")
            return

        # Имя файла и расширение
        file_name, file_extension = os.path.splitext(text1)

        # Создание нового пути с новым именем файла
        new_path = os.path.join("knowFaces", f"{text2}{file_extension}")

        try:
            # Перемещение файла в папку "knowFaces"
            shutil.move(text1, new_path)
            print(f"Файл успешно перемещен в папку 'knowFaces' с именем '{text2}{file_extension}'")
            self.label_confirmation.setText(f"Файл успешно перемещен в папку 'knowFaces' с именем '{text2}{file_extension}'")
        except Exception as e:
            print(f"Ошибка при перемещении файла: {e}")
            self.label_confirmation.setText(f"Ошибка при перемещении файла: {e}")

    
    def delete_image(self, textbox_delete):
        # Получение названия файла из текстового поля
        filename = textbox_delete

        # Поиск файлов с указанным именем в папке "knowFaces"
        file_paths = glob.glob(os.path.join("knowFaces", filename))

        if file_paths:
            try:
                # Удаление каждого найденного файла
                for file_path in file_paths:
                    os.remove(file_path)
                print(f"Файлы с названием {filename} успешно удалены.")
                self.label_confirmation_del.setText(f"Файлы с названием {filename} успешно удалены.")
            except Exception as e:
                print("Ошибка при удалении файлов:", str(e))
                self.label_confirmation_del.setText("Ошибка при удалении файлов:", str(e))
        else:
            print(f"Файлы с названием {filename} не найдены.")
            self.label_confirmation_del.setText(f"Файлы с названием {filename} не найдены.")




if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
