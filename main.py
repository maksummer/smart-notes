from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog
from ui import Ui_MainWindow
import json


app = QApplication([])
win = QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(win)


NOTES = {
    "Ласкаво Просимо":{
        "текст": "Ласкаво просимо до найрозумнішого застосунку із замітками",
        "теги": ["Ласкаво", "Просимо", "допомога", "замітки"]
    }
}




with open("notes_data.json", "r", encoding="utf-8") as file:
    NOTES = json.load(file)

ui.notes_list.addItems(NOTES)



def show_note():
    name = ui.notes_list.currentItem().text()

    ui.textEdit.setText(NOTES[name]["текст"])

    ui.tags_list.clear()
    ui.tags_list.addItems(NOTES[name]["теги"])



ui.notes_list.itemClicked.connect(show_note)

def add_note():
    note_name, ok = QInputDialog.getText(win,"додати замітку", "назва нової замітки?")
    if ok and note_name != "":
        NOTES[note_name] = {"текст": "", "теги":[]}
        ui.notes_list.addItem(note_name)

ui.add_btn.clicked.connect(add_note)

def save_note():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()

        note_text = ui.textEdit.toPlainText()

        NOTES[note_name]["текст"] = note_text

        with open("notes_data.json","w",encoding="utf-8") as file:
            json.dump(NOTES, file)


ui.save_btn.clicked.connect(save_note)

def del_note():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()

        del NOTES[note_name]
        
        ui.textEdit.clear()
        ui.tags_list.clear()

        ui.notes_list.clear()
        ui.notes_list.addItems(NOTES)

        with open("notes_data.json","w",encoding="utf-8") as file:
            json.dump(NOTES,file)

ui.del_btn.clicked.connect(del_note)

def add_tag():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()
        tag = ui.tag_edit.text()

        if not tag in NOTES[note_name]["теги"]: 
            NOTES[note_name]["теги"].append(tag)
            ui.tags_list.addItem(tag)
            ui.tag_edit.clear()

        with open("notes_data.json","w",encoding="utf-8") as file:
            json.dump(NOTES, file)

ui.add_tag_btn.clicked.connect(add_tag)

def del_tag():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()
        if ui.tags_list.selectedItems():
            tag = ui.tags_list.currentItem().text()
            ui.tags_list.clear()
            NOTES[note_name]["теги"].remove(tag)
            ui.tags_list.addItems(NOTES[note_name]["теги"])

            with open("notes_data.json","w",encoding="utf-8")as file:
                json.dump(NOTES,file)

ui.del_tag_btn.clicked.connect(del_tag)


def search_tag():
    if ui.search_btn.text() == "Шукати по теґу":
        tag = ui.tag_edit.text()
        if tag != "" and tag !=" ":
            notes_filtered = {}
            for n in NOTES:
                if tag in NOTES[n]["теги"]:
                    notes_filtered[n] = {
                        "текст": NOTES[n]["текст"],
                        "теги": NOTES[n]["теги"]
                    }
            print(notes_filtered)
            ui.notes_list.clear()
            ui.notes_list.addItems(notes_filtered)
            ui.search_btn.setText("Скинути пошук")
    elif ui.search_btn.text() == "Скинути пошук":
        ui.notes_list.clear()
        ui.notes_list.addItems(NOTES)
        ui.search_btn.setText("Шукати по теґу")
    else:
        print("текст не збігається")
    





ui.search_btn.clicked.connect(search_tag)

win.show()
app.exec()
