from msilib.schema import RadioButton
import sys
from xml.etree.ElementTree import tostring
import pyodbc
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from PyQt5 import QtWidgets

from_class = uic.loadUiType("db_exam.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.currentDateTime = QDateTime.currentDateTime() # PyQt5.QtCore import *
        self.dateEdit.setDateTime(self.currentDateTime)

        # Radio Button default "rad1"

        self.rad1.setChecked(True)
        

        self.btn_insert.clicked.connect(self.insertdb)
        
    #     self.btn_display.clicked.connect(self.grouboxRadFuntion)

    # def grouboxRadFuntion(self):
    #     if self.rad1.isChecked() : i_sex ="남성"
    #     elif self.rad2.isChecked() :  i_sex = "F"
    #     elif self.rad3.isChecked() :  i_sex = "o"
    #     print(i_sex)
    

    def insertdb(self):
        try:
            con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\Python Qt Designer & DB\db_exam.accdb;'
            conn = pyodbc.connect(con_string)
            print("DB 연결 성공")
            # QMessageBox.about(self,"Title","Message")
            c = conn.cursor()

            i_memo = self.txt_memo.toPlainText()

            # 날짜 입력            
            self.dateVar = self.dateEdit.date()
            self.idate = self.dateVar.toString("yyyy-MM-dd")
          
            print(i_memo)
            print(self.idate)
            
            # r1 = self.groupBox.text()

            print (r1)
            print (type(r1))

            if self.rad1.isChecked() : i_sex = "남"
            elif self.rad2.isChecked() : i_sex = "여"
            elif self.rad3.isChecked() : i_sex = "중성"

            self.r1 = self.i_sex.text()

            c.execute("INSERT INTO tt ([a_memo], a_date, a_sex) VALUES (?,?,?)", ([i_memo], self.idate, self.r1))

            print("입력되었습니다.")            
            conn.commit()
            conn.close()

        except Exception as error:
            print("연걸이 되지 않았습니다.", error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()