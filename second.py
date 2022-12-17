from PyQt5.QtWidgets import (QTextEdit, QLabel, QPushButton, QLineEdit, QGridLayout, QDialog)
from PyQt5.QtGui import QFont
from db import SQLiteDB

class Second(QDialog):
    def __init__(self, flag_admin, first, db=None):
        super().__init__()
        self.flag_admin = flag_admin
        self.database = SQLiteDB()
        self.first = first()
        self.db = db

        self.line_edit = {}
        self.lines_names = {0:"Поручение №", 
                            1:"Название",
                            2:"Автор",
                            3:"Исполнитель", 
                            4:"Дата выдачи", 
                            5:"Дата выполнения", 
                            6:"Срок исполнения",
                            7:"Содержание"} 

        self.resize(700,450)
        self.setWindowTitle("Форма поручения")
        ##################### text layout #####################
        lineEditLayout = QGridLayout()
        font = QFont()
        
        for i in range(len(self.lines_names)):
            label = QLabel(self.lines_names[i])
            
            if i == len(self.lines_names) - 1:
                font.setPointSize(12)
                label.setFont(font)
                lineEditLayout.addWidget(label,i,0,1,1)
                self.line_edit[self.lines_names[i]] = QTextEdit()
                lineEditLayout.addWidget(self.line_edit[self.lines_names[i]],i+1,0,1,2)
            else:
                font.setPointSize(10)
                label.setFont(font)
                lineEditLayout.addWidget(label,i,0,1,1)
                self.line_edit[self.lines_names[i]] = QLineEdit()
                lineEditLayout.addWidget(self.line_edit[self.lines_names[i]],i,1,1,1)
                

            # look assigment only mode
            if self.db is not None: 
                self.line_edit[self.lines_names[i]].setText(str(db[i]))
            
            # admin mode
            if self.flag_admin:   
                self.line_edit[self.lines_names[i]].setReadOnly(False)
            # user mode
            else:           
                self.line_edit[self.lines_names[i]].setReadOnly(True)
            if i == 0:
                self.line_edit[self.lines_names[i]].setReadOnly(True)

        ##################### buttons layout ##################### 
        buttonsLayout = QGridLayout()
        back_btn = QPushButton("Назад")
        buttonsLayout.addWidget(back_btn,0,0,1,1)
        back_btn.clicked.connect(self.back_clicked)

        save_btn = QPushButton("Сохранить")
        buttonsLayout.addWidget(save_btn, 0,1,1,1)
        save_btn.clicked.connect(self.save_clicked)

        # user mode - 'save' button not active
        if not self.flag_admin: 
            save_btn.setEnabled(False)
        
        lineEditLayout.addLayout(buttonsLayout,9,0,1,1)
        self.setLayout(lineEditLayout)

    def back_clicked(self):
        self.close()  
        self.first.initUi()
        self.first.show()

    def save_clicked(self):
        texts = {}

        # if create assigment mode
        if self.db is None: 
            for i in range(len(self.lines_names)):
                if i == len(self.lines_names) - 1:
                    texts[i] = str(self.line_edit[self.lines_names[i]].toPlainText())
                else:
                    texts[i] = str(self.line_edit[self.lines_names[i]].text())
            self.database.insert_varible_into_table(texts[1], texts[2], texts[3], texts[4], texts[5], texts[6], texts[7])
        
        # if update data in data base
        else: 
            for i in range(len(self.lines_names)):
                if i == len(self.lines_names) - 1:
                    texts[i] = str(self.line_edit[self.lines_names[i]].toPlainText())
                else:
                    texts[i] = str(self.line_edit[self.lines_names[i]].text())
            self.database.update_sqlite_table(texts[1], texts[2], texts[3], texts[4], texts[5], texts[6], texts[7], texts[0])
        self.close()
        self.first.initUi()
        self.first.show()