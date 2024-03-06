import win32com.client
import sys
import re
from pathlib import Path
import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
import mainwindow as m
import getpass
import json

# PySide6.QtWidgets.MainWindow を継承した MainWindow クラスの定義
class Config(Qw.QScrollArea):
  user = getpass.getuser()
  group:dict = {}
  desktop = Path(f"C:\\Users\\{user}\\Desktop")
  startmenu = Path(f"C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
  def __init__(self):
    wshell = win32com.client.Dispatch("WScript.Shell")
    super().__init__()
    sp_exp = Qw.QSizePolicy.Policy.Expanding
    # ウィンドウタイトル設定
    self.setWindowTitle('グループ分け') 

    # ウィンドウのサイズ(640x240)と位置(X=100,Y=50)の設定
    self.setGeometry(100, 50, 640, 240)
    self.setMinimumSize(320,200) 

    # メインレイアウトの設定
    central_widget = Qw.QWidget(self)
    main_layout = Qw.QVBoxLayout(central_widget) # 要素を垂直配置
    main_layout.setAlignment(Qc.Qt.AlignmentFlag.AlignTop) # 上寄せ
    main_layout.setContentsMargins(15,10,10,10)
    button_layout = Qw.QHBoxLayout()
    button_layout.setAlignment(Qc.Qt.AlignmentFlag.AlignLeft) # 左寄せ
    main_layout.addLayout(button_layout) # メインレイアウトにボタンレイアウトを追加

    #「グループを追加」ボタンの生成と設定
    self.btn_add = Qw.QPushButton('グループを追加')
    self.btn_add.setMinimumSize(50,20)
    self.btn_add.setMaximumSize(100,20)
    self.btn_add.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_add)
    self.btn_add.clicked.connect(self.add)

    #「全選択」ボタンの生成と設定
    self.btn_Allcheck = Qw.QPushButton('全選択')
    self.btn_Allcheck.setMinimumSize(50,20)
    self.btn_Allcheck.setMaximumSize(100,20)
    self.btn_Allcheck.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_Allcheck)
    self.btn_Allcheck.clicked.connect(self.Allcheck)

    #「全選択解除」ボタンの生成と設定
    self.btn_Alluncheck = Qw.QPushButton('全選択解除')
    self.btn_Alluncheck.setMinimumSize(50,20)
    self.btn_Alluncheck.setMaximumSize(100,20)
    self.btn_Alluncheck.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_Alluncheck)
    self.btn_Alluncheck.clicked.connect(self.Alluncheck)

    #「エクスプローラーで選択」ボタンの生成と設定
    self.btn_exp = Qw.QPushButton('エクスプローラーで選択')
    self.btn_exp.setMinimumSize(70,20)
    self.btn_exp.setMaximumSize(100,20)
    self.btn_exp.setSizePolicy(sp_exp,sp_exp)
    button_layout.addWidget(self.btn_exp)
    self.btn_exp.clicked.connect(self.exp)

    # # ナビゲーション情報を表示するラベル
    # self.init_navi_msg = \
    #     "グループ化するexeファイルを選択"
    # self.lb_navi = Qw.QLabel(self.init_navi_msg,self)
    # self.lb_navi.setMinimumSize(100,15)
    # self.lb_navi.setMaximumSize(100,15)
    # self.lb_navi.setSizePolicy(sp_exp,sp_exp)
    # main_layout.addWidget(self.lb_navi)

    # 入力フィールド
    self.tb_name = Qw.QLineEdit('',self)
    self.tb_name.setPlaceholderText('グループ名を入力')
    self.tb_name.setMinimumSize(10,10)
    self.tb_name.setSizePolicy(sp_exp,sp_exp)
    self.tb_name.setAcceptDrops(False)
    main_layout.addWidget(self.tb_name)

    # チェックボックス形式
    #region
    l = \
    [wshell.CreateShortcut(str(p.resolve())).TargetPath for p in self.desktop.glob('**/*.lnk') \
    if re.search(r'.*\.[eE][xX][eE]', wshell.CreateShortcut(str(p.resolve())).TargetPath)]\
   +[wshell.CreateShortcut(str(p.resolve())).TargetPath for p in self.startmenu.glob('**/*.lnk') \
    if re.search(r'.*\.[eE][xX][eE]', wshell.CreateShortcut(str(p.resolve())).TargetPath)]
    l = sorted(list(set(l)))

    # チェックボックスの生成と設定
    self.checkboxes : list[Qw.QCheckBox] = []
    for file in l:
      cb = Qw.QCheckBox(self)
      cb.setText(file)
      cb.file = file
      cb.setCursor(Qc.Qt.CursorShape.PointingHandCursor)
      self.checkboxes.append(cb)
      main_layout.addWidget(cb)

    inner = central_widget
    layout = main_layout
    inner.setLayout(layout)
    self.setWidget(inner)
    # endregion

  def Allcheck(self):
    for i in self.checkboxes:
      i.setCheckState(Qc.Qt.CheckState.Checked)

  def Alluncheck(self):
    for i in self.checkboxes:
      i.setCheckState(Qc.Qt.CheckState.Unchecked)

  def add(self):
    self.group[self.tb_name.text()] = [i.file[:list(re.finditer(r'\.[eE][xX][eE]', i.file))[-1].end()+1] for i in self.checkboxes if i.isChecked()]
    print(self.group)
    with open("data.json", "w") as json_file:
        json.dump(self.group, json_file)

  def exp(self):
    path = Qw.QFileDialog.getOpenFileNames(
      self,      # 親ウィンドウ
      "複数ファイル選択",     # ダイアログタイトル
      "", # 初期位置（フォルダパス）
      "実行ファイル (*.lnk)"
      )
    self.group[self.tb_name.text()] = path[0]
    print(self.group)


# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = Config()
  main_window.show()
  sys.exit(app.exec())
