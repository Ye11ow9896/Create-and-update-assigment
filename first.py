# Этот файл создан Кондратенко Алексеем Александровичем. Авторские права защищены.
# Попытка использования без разрешения автора будет преследоваться по закону! 

from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton, QGridLayout, QScrollArea, QMainWindow, QCommandLinkButton, QInputDialog, QApplication, QCheckBox)
from PyQt5.QtCore import (QRect)
from second import Second
from db import SQLiteDB

class First(QMainWindow):
    def __init__(self):
        super().__init__()
        self.secwin = None
        self.filter_text = None
        self.filter_btn_names = {0:("Фильтровать по дате", "Введите дату"), 1:("Фильтровать по автору", "Введите автора"), 2:("Фильтровать по исполнителю", "Введите исполнителя")} 
        self.flag_admin = False 
        self.showdb_flag = False

    def initUi(self):
        self.db = SQLiteDB()
        self.table_db = self.db.get_database_table('db.sqlite')
        self.setWindowTitle('Служба создания поручений')
        self.resize(700, 450)

        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(50, -1, -1, 0)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 410, 247))
        self.linkslayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 4, 2)
        self.setCentralWidget(self.centralwidget)

        for i in range(len(self.filter_btn_names)):
            filter_btn = QPushButton(self.filter_btn_names[i][0])
            self.gridLayout.addWidget(filter_btn, i, 0, 1, 1)
            filter_btn.lineText = self.filter_btn_names[i][1]
            filter_btn.is_filter = self.filter_btn_names[i][0]
            filter_btn.clicked.connect(self._filter_clicked)
        
        reset_filter_btn = QPushButton("Сброс фильтров")
        self.gridLayout.addWidget(reset_filter_btn, 3, 0, 1, 1)
        reset_filter_btn.clicked.connect(self._reset_filter_clicked)

        self.create_assigment_btn = QPushButton("Создать поручение")
        self.gridLayout.addWidget(self.create_assigment_btn, 4, 1, 1, 1)
        self.create_assigment_btn.setEnabled(False)
        self.create_assigment_btn.clicked.connect(self._create_assigment_window)

        admin_mode_btn = QCheckBox(self.centralwidget)
        self.gridLayout.addWidget(admin_mode_btn, 4, 2, 1, 1)
        admin_mode_btn.setText("Режим администратора")
        admin_mode_btn.stateChanged['int'].connect(self._admin_mode_clicked)

        self._create_links_buttons(self.table_db)
        self.show()

    def _create_links_buttons(self, data):
        for i in range(len(data)):
            link_btn = QCommandLinkButton(self.scrollAreaWidgetContents)
            self.linkslayout.addWidget(link_btn, i, 0, 1, 2)
            link_btn.setText(str(data[i][1]) + ' от ' + str(data[i][2]))
            link_btn.setObjectName(str(i))
            link_btn.table_db_i = data[i]
            link_btn.clicked.connect(self._link_clicked)

    def _filter_clicked(self):
        #get params
        param = self.sender().lineText
        filter = self.sender().is_filter
        filter_text = None
        text, ok = QInputDialog.getText(self, "Фильтр", str(param))
        if ok:
            filter_text = str(text)

        if filter_text is not None:
            # if data filter
            filtred_data = None
            if filter == self.filter_btn_names[0][0]: 
                filtred_data = self.db.search_in_DB(self.db.search_date_assigment, filter_text)
            # if filter of author
            if filter == self.filter_btn_names[1][0]: 
                filtred_data = self.db.search_in_DB(self.db.search_author, filter_text)
            # if filter of executor
            if filter == self.filter_btn_names[2][0]: 
                filtred_data = self.db.search_in_DB(self.db.search_executor, filter_text)
            # if DB hasnt input data
            if len(filtred_data) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Введенных данных нет в базе')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                # delete objects in linkslayout
                for i in range(self.linkslayout.count()):
                    self.linkslayout.itemAt(i).widget().deleteLater()
                self._create_links_buttons(self.table_db)
        
    def _link_clicked(self):
        db = self.sender().table_db_i
        self.secwin = Second(self.flag_admin, First, db)
        self.secwin.show()
        self.close()

    def _reset_filter_clicked(self):
        # delete objects in linkslayout
        for i in range(self.linkslayout.count()):
            self.linkslayout.itemAt(i).widget().deleteLater()
        # added filtred objects
        self._create_links_buttons(self.table_db)
    
    def _admin_mode_clicked(self, state):
        if state == 2.:
            self.create_assigment_btn.setEnabled(True)
            self.flag_admin = True
        else:
            self.create_assigment_btn.setEnabled(False)
            self.flag_admin = False
    
    def _create_assigment_window(self):
        self.secwin = Second(self.flag_admin, First)
        self.secwin.show()
        self.close()