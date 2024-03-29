import win32com.client
import sys
import os
import re
from pathlib import Path
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
import getpass
import mainwindow as m
import pickle

# PySide6.QtWidgets.MainWindow を継承した MainWindow クラスの定義
class Config(Qw.QMainWindow):
  user = getpass.getuser()
  group:dict = {}
  desktop = Path(f"C:\\Users\\{user}\\Desktop")
  startmenu = Path(f"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs")
  def __init__(self):
    wshell = win32com.client.Dispatch("WScript.Shell")
    super().__init__()
    sp_exp = Qw.QSizePolicy.Policy.Expanding
    # ウィンドウタイトル設定
    self.setWindowTitle('グループ分け') 
    self.setAcceptDrops(True)

    # ウィンドウのサイズ(640x240)と位置(X=100,Y=50)の設定
    self.setGeometry(100, 50, 850, 500)
    self.setMinimumSize(320,200) 

    # メインレイアウトの設定
    central_widget = Qw.QWidget(self)
    self.setCentralWidget(central_widget)
    main_layout = Qw.QVBoxLayout(central_widget) # 要素を垂直配置
    main_layout.setAlignment(Qc.Qt.AlignmentFlag.AlignTop) # 上寄せ
    main_layout.setContentsMargins(15,10,10,10)
    button_layout = Qw.QHBoxLayout()
    button_layout.setAlignment(Qc.Qt.AlignmentFlag.AlignLeft) # 左寄せ
    main_layout.addLayout(button_layout) # メインレイアウトにボタンレイアウトを追加

    self.setStyleSheet("""
      QWidget {
      background-color: #001933;
      color: #fff;
      } 
      QPushButton {
        background-color: #007bff;
        color: #fff;
      }
      QPushButton:hover {
        background-color: #0056b3;
      }
      QLineEdit {
        background-color: #fff;
        color: #000;
      }
      QListWidget{
        background-color: #fff;
        color: #000;
      }
      QLabel{
        color: #ff0000;
      }
    """)

    # QLabelを作成して、テキストを設定します
    self.label = Qw.QLabel("", self)
    main_layout.addWidget(self.label)

    # 入力フィールド
    self.tb_name = Qw.QLineEdit('',self)
    self.tb_name.setPlaceholderText('グループ名を入力')
    self.tb_name.setMinimumSize(10,30)
    self.tb_name.setMaximumHeight(30)
    self.tb_name.setSizePolicy(sp_exp,sp_exp)
    self.tb_name.setAcceptDrops(False)
    main_layout.addWidget(self.tb_name)

    #リスト
    self.listview = Qw.QListWidget()
    self.listview.setResizeMode(Qw.QListWidget.ResizeMode.Adjust)
    self.listview.setSelectionMode(Qw.QAbstractItemView.MultiSelection)
    self.listview.setMinimumSize(250,100)
    self.listview.setSizePolicy(sp_exp,sp_exp)
    self.listview.setIconSize( Qc.QSize(32, 32) )
    main_layout.addWidget( self.listview )

    #「グループを追加」ボタンの生成と設定
    self.btn_add = Qw.QPushButton('グループを追加')
    self.btn_add.setMaximumSize(100,20)
    self.btn_add.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_add)
    self.btn_add.clicked.connect(self.add)

    #「全選択」ボタンの生成と設定
    self.btn_Allcheck = Qw.QPushButton('全選択')
    self.btn_Allcheck.setMaximumSize(100,20)
    self.btn_Allcheck.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_Allcheck)
    self.btn_Allcheck.clicked.connect(self.Allcheck)

    #「全選択解除」ボタンの生成と設定
    self.btn_Alluncheck = Qw.QPushButton('全選択解除')
    self.btn_Alluncheck.setMaximumSize(100,20)
    self.btn_Alluncheck.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_Alluncheck)
    self.btn_Alluncheck.clicked.connect(self.Alluncheck)

    #「エクスプローラーで選択」ボタンの生成と設定
    self.btn_exp = Qw.QPushButton('リストに項目を追加')
    self.btn_exp.setMaximumSize(200,20)
    self.btn_exp.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_exp)
    self.btn_exp.clicked.connect(self.exp)

    #「候補から削除」ボタンの生成と設定
    self.btn_delete = Qw.QPushButton('候補から削除')
    self.btn_delete.setMaximumSize(120,20)
    self.btn_delete.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_delete)
    self.btn_delete.clicked.connect(self.delete)

    # チェックボックス形式
    if os.path.isfile("listdata.pickle"):
      with open("listdata.pickle",'rb') as file:
        l = pickle.load(file)
    else:
      l = \
      [wshell.CreateShortcut(str(p.resolve())).TargetPath for p in self.desktop.glob('**/*.lnk') \
      if re.search(r'.*\.[eE][xX][eE]', wshell.CreateShortcut(str(p.resolve())).TargetPath)]\
      +[wshell.CreateShortcut(str(p.resolve())).TargetPath for p in self.startmenu.glob('**/*.lnk') \
      if re.search(r'.*\.[eE][xX][eE]', wshell.CreateShortcut(str(p.resolve())).TargetPath)]
      l = sorted(list(set(l)))
    for path in l:
      print(path)
      Qw.QListWidgetItem(Qw.QFileIconProvider().icon(Qc.QFileInfo(path)), path, self.listview)
    self.save()

  def save(self):
    l = [self.listview.item(i).text() for i in range(self.listview.count())]
    with open("listdata.pickle", mode='wb') as file:
      pickle.dump(l, file)

  def Allcheck(self):
    for i in range(self.listview.count()):
      self.listview.item(i).setSelected(True)

  def Alluncheck(self):
    for i in range(self.listview.count()):
      self.listview.item(i).setSelected(False)

  def add(self):
    key = self.tb_name.text()
    d = m.mw.taskdic
    if key == "":
      self.label.setText("key名を入力してください")
      return
    if key in d:
      reply = Qw.QMessageBox.question(self, 'key名が重複しています',
              "内容を上書きしますか？",
              Qw.QMessageBox.Yes | Qw.QMessageBox.No)
      if reply == Qw.QMessageBox.No:
        return
      else:
        m.mw.task_list.takeItem(m.mw.task_list.row(m.mw.task_list.findItems(key,Qc.Qt.MatchCaseSensitive)[0]))
        del d[key]
    d[key] = [i.text() for i in self.listview.selectedItems()]
    self.label.setText("")
    self.tb_name.setText("")
    self.Alluncheck()
    m.mw.task_list.addItem(f'{key}')
    m.mw.save_tasks()

  def exp(self):
    path = Qw.QFileDialog.getOpenFileNames(
      self,      # 親ウィンドウ
      "複数ファイル選択",     # ダイアログタイトル
      "", # 初期位置（フォルダパス）
      "実行ファイル (*.exe) ;; Allfile (*)"
      )
    for i in path:
      Qw.QListWidgetItem(Qw.QFileIconProvider().icon(Qc.QFileInfo(i)), i, self.listview)

  def delete(self):
    for i in self.listview.selectedItems():
      self.listview.takeItem(self.listview.row(i))
    self.save()

  # ドラッグ処理
  def dragEnterEvent(self,e):
    if e.mimeData().hasUrls():
        e.accept()

  # ドロップ処理
  def dropEvent(self, e):
    urls = e.mimeData().urls()
    for i in urls:
      url = i.path()[1:].replace('/',"\\")
      Qw.QListWidgetItem(Qw.QFileIconProvider().icon(Qc.QFileInfo(url)), url, self.listview)
    self.save()
  
  def keyPressEvent(self, event: Qg.QKeyEvent):
    key = event.key()
    if key == Qc.Qt.Key_Delete:
      self.delete()

# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = Config()
  main_window.show()
  sys.exit(app.exec())