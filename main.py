# Этот файл создан Кондратенко Алексеем Александровичем. Авторские права защищены.
# Попытка использования без разрешения автора будет преследоваться по закону!
# 

import sys
from PyQt5.QtWidgets import QApplication
from first import First
from PyQt5 import QtCore

class Main(object):
    def __init__(self):
        super().__init__()
        self.first = First()
        self.first.initUi()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ### added styles ###
    file = QtCore.QFile("theme.css")                              
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    mainwin = Main()
    sys.exit(app.exec_())

