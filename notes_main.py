#начни тут создавать приложение с умными заметками
import json
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QLayout, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog, QInputDialog, QMessageBox
#заметки в джэйсон
notes = {
    "Добро пожаловать!":{
        "текст" : "Это самое лучшее приложение для заметок!",
        "теги" : ["добро", "инструкция"]
    }
}

with open("notes_data.json", "w") as file:
    json.dump(notes, file, ensure_ascii=False)

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Умные заметки")
main_win.resize(900, 600)

#виджеты
field_text = QTextEdit()

list_notes_label = QLabel("Список заметок")
list_notes = QListWidget()

button_note_create = QPushButton("Создать заметку")
button_note_delete = QPushButton("Удалить заметку")
button_note_save = QPushButton("Сохранить заметку")

list_tags_label = QLabel("Список тегов")
list_tags = QListWidget()
field_tag = QLineEdit("")
field_tag.setPlaceholderText("Введи тег пж...")

button_tag_add = QPushButton("Добавить тег")
button_tag_delete = QPushButton("Открепить тег")
button_tag_search = QPushButton("Искать заметки по тегу")

#постановка виджетов
main_layout = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_delete)
col_2.addLayout(row_1)
col_2.addWidget(button_note_save)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_2 = QHBoxLayout()
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_delete)
col_2.addLayout(row_2)
col_2.addWidget(button_tag_search)

main_layout.addLayout(col_1, stretch=2)
main_layout.addLayout(col_2, stretch=1)
main_win.setLayout(main_layout)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(main_win, "Добавить заметку", "Название заметки:")
    if ok and note_name != "":
        notes[note_name]= {"текст": "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, ensure_ascii=False)
        print(notes)
    else:
        mb = QMessageBox()
        mb.setText("Выберите заметку, которую вы хотите анигилировать.")
        mb.setWindowTitle("Ошибка")
        mb.exec_()

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        mb = QMessageBox()
        mb.setText("Выберите заметку, которую вы хотите сохранить.")
        mb.setWindowTitle("Ошибка")
        mb.exec_()

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        mb = QMessageBox()
        mb.setText("Выберите заметку, которую вы хотите сохранить.")
        mb.setWindowTitle("Ошибка")
        mb.exec_()

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        mb = QMessageBox()
        mb.setText("Выберите тег, который вы хотите анигилировать.")
        mb.setWindowTitle("Ошибка")
        mb.exec_()

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")
    else:
        pass



button_tag_search.clicked.connect(search_tag)
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_delete.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_delete.clicked.connect(del_tag)

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

main_win.show()
app.exec()