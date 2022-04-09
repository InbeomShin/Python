import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
import pyodbc

from_class = uic.loadUiType("Qtablewidget.ui")[0]

class WindowClass(QMainWindow, from_class):
  def __init__(self):
    super().__init__()
    self.setupUi(self)

    # 버튼 
    self.btn_insert.clicked.connect(self.insertdb)
    self.btn_display.clicked.connect(self.loaddata1)
    self.btn_exit.clicked.connect(QCoreApplication.instance().quit)
    
    self.displaydata()

  # QtableWidget 데이터 Display
  def displaydata(self):
    try:
      i = 0
      self.tableWidget.clear()
      self.tableWidget.setRowCount(0)

      self.tableWidget.setColumnWidth(0,100)
      self.tableWidget.setColumnWidth(1,50)
      self.tableWidget.setHorizontalHeaderLabels(["name","age"])
      # s_name = self.lineEdit_search.text()     

      con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\Python Qt Designer & DB\dataexam.accdb;'

      conn = pyodbc.connect(con_string)
      c=conn.cursor()

      # c.execute("SELECT * FROM qt_table WHERE a_name = ?", s_name)
      c.execute("SELECT * FROM qt_table")
      tablerow = 0

      for i, row in enumerate (c.fetchall()):
        #print (row) #data를 프린트 한다.
        self.tableWidget.insertRow(i)
        self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
        self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
      
        tablerow+=1 

    except Exception as error:
      print("연결되지 않았습니다.", error)

  def loaddata1(self):
    try:
      i = 0
      self.tableWidget.clear()
      self.tableWidget.setRowCount(0)
      self.tableWidget.setColumnWidth(0,100)
      self.tableWidget.setColumnWidth(1,50)
      self.tableWidget.setHorizontalHeaderLabels(["name","age"])
      s_name = self.lineEdit_search.text()     

      con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\Python Qt Designer & DB\dataexam.accdb;'

      conn = pyodbc.connect(con_string)
      c=conn.cursor()

      c.execute("SELECT * FROM qt_table WHERE a_name = ?", s_name)
      
      tablerow = 0

      for i, row in enumerate (c.fetchall()):
        #print (row) #data를 프린트 한다.
        self.tableWidget.insertRow(i)
        self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
        self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
       
        tablerow+=1 

    except Exception as error:
      print("연결되지 않았습니다.", error)

  # 데이터 입력
  def insertdb(self):
    try:      
      i_name = self.lineEdit_name.text()
      i_age = self.lineEdit_age.text()

      con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\Python Qt Designer & DB\dataexam.accdb;'
      conn = pyodbc.connect(con_string)
      c=conn.cursor()

      data=(i_name, i_age)

      c.execute("INSERT INTO qt_table(a_name, a_age) VALUES (?,?)", (data))      
      QMessageBox.about(self,"data","입력 성공")

      conn.commit()
      conn.close()

      self.dbclear()
      self.displaydata()

    except Exception as error:
      print("연결되지 않았습니다.", error)

  # 입력항목 clear
  def dbclear(self):
    self.lineEdit_name.clear()
    self.lineEdit_age.clear()

if __name__=="__main__":
  app = QApplication(sys.argv)
  myWindow = WindowClass()
  myWindow.show()
  app.exec()