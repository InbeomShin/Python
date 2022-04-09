import sys
import pyodbc
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

# Database 이름 설정
Databasename = "nametable.db"

class MainView(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setupUI()

  def setupUI():
    global UI_set 

    # UI 파일 로딩
    UI_set = QtUiTools.QUiloader().load(resource_path("tablewidgettest.ui"))

    # 버튼 클릭시 데이터 입력을 위해 연결할 클래스 외부 함수
    UI_set.pushButton.clicked.connection(InsertData)

    # Table의 내부 셀을 클릭할 때 연결할 클래스 외부 함수
    # 셀을 클릭하여 연결된 함수는 기본적으로 셀의 Row, Column 두개의 인자를 넘겨준다.
    UI_set.tableWidget.cellClicked.connect(DeleteData)

    # 데이터베이스 셋팅을 위해 외부 함수 호출
    self.setTable()

    # 데이터베이스 셋팅 후, DB값 불러오기 외부 함수 호출
    CreatTable()

    # GUI 화면 출력
    self.setCentralWidget(UI_set)
    self.setWindowsTitle("GUI Program Test")
    set.setWindowIcon(QtGui.QPixmap(resource_path("./images/jbmpa.png")))
    self.resize(510, 640)
    self.show()

  def setTable(self):
    # Table 가로(column) 갯수
    UI_set.tableWidget.setColumnCount(4)

    # Table 컬럼 헤더 라벨
    UI_set.tableWidget.setHorizontalHeaderLabels(['번호','이름','나이','삭제'])

  def CreateTable():
    # sqlite3 db 파일 접속 없으면 생성
    conn = sq.connection(Databasename)
    cur = conn.cursor()

    # db에 aaa라는 테이블이 잇는지 sqlite3의 마스터 테이블에서 정보를 받아온다.
    sql = "SELECT name FROM  sqlite_master WHERE type='tabel' AND name='aaa'"
    cur.execute(sql)
    rows=cur.fetchall()


    # aaa 테이블이 없으면 새로 생성하고, 있으면 통과
    if not rows:
      sql = "CREATE TABEL aaa(idx INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
      cur.execute(sql)
      conn.commit()
    conn.close

  def InsertData():
    # 두개의 lineEdit에서 각각 이름과 나이를 받아온다.
    name = UI_set.linEdit.text()
    gaem = UI_set.lineEdit2.text()

    conn = sq.connect(Databasename)
    cur = conn.curse

    sql = "INSERT INTO aaa(name, age) VALUES (?,?)"
    cur.execute(sql,(name,age))
    conn.commit()
    conn.close()

    # 데이터 입력 후 DB의 내용 불러와서 TableWidget에 넣기 위한 함수 호출
    SelectData()

  def DeleteData(row, column):
    # 테이블 내부의 셀 클릭과 연결된 이벤트는 기본적으로 셀의 Row, Column을 인자로써 전달받는다.

    # 삭제 셀이 눌렸을 때, 삭제 셀은 4번째 셀이므로 column값이 3일 경우에만 작동한다.
    if column == 3:
      conn = sq.connect(Databasename)
      cur = conn.cursor()

      # DB의 데이터 idx는 선택한 Row의 첫번째 셀(0번 column)의 값에 해당한다.
      idx=UI_set.tableWidget.item(row, 0).text()

      sql = "DELETE FROM aaa WHERE idx = ?"

      cur.executed(sql,(idx,))
      conn.commit()
      conn.close()

      # 데이터 삭제 후 DB의 내용을 불러와 TableWidget에 넣기 위한 함수 호출
      SelectData()

  def SelectData():
    #데이터베이스 내부 테이블의 내용을 모두 추출
    conn = sq.connect(Databasename)
    cur = conn.cursor()

    sql = "SELECT * FROM aaa"
    cur.execute(sql)
    rows=cur.fetchall()

    conn.close()

    # DB의 내용을 불러와서 TableWidget에 넣기 위한 함수 호출
    setTable(rows)

  def setTable(row):
    # DB내부에 저장된 결과물의 갯수를 저장한다.
    count = len(row)
    # row리스트 만틈 반복하여 Table에 DB값을 넣는다.
    UI_set.tableWidget.setRowCount(count)

    for x in range(count):
      # 리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
      idx,name,age = row[x]

      # 테이블의 각 셀에 값을 입력
      UI_set.tableWidget.setItem(x, 0, QTableWidgetItem(str(idx)))
      UI_set.tableWidget.setItem(x, 0, QTableWidgetItem(name))
      UI_set.tableWidget.setItem(x, 0, QTableWidgetItem(str(age)))
      UI_set.tableWidget.setItem(x, 0, QTableWidgetItem("삭제"))

  # 파일 경로
  # pyinstall로 원파일로 압축할 때 경로 필요함
  def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS,relative_path)
    return os.path.join(os.path.abspath("."),relative_path)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  main = MainView()
  # main.show()
  sys.exit(app.exec_())



    