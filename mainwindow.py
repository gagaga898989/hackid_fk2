import subprocess
import config as c
import sys
from PySide6.QtWidgets import \
    QMainWindow, QPushButton,QApplication,QVBoxLayout, QWidget,QLabel,QListWidget,QFrame,QHBoxLayout,\
    QFileIconProvider,QListWidgetItem,QAbstractItemView
from PySide6.QtGui import QFont,QKeyEvent
from PySide6.QtCore import Qt,QFileInfo
import os
import random
import pickle

class MainWindow(QMainWindow):
    def __init__(self):
        global mw
        mw = self
        self.taskdic = {}
        self.can = True
        super().__init__()
        self.setWindowTitle("Main Window")
        #win32com
        
        # メインウィジェットを作成
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # QLabelを作成して、テキストを設定します
        self.label = QLabel("複数同時起動アプリ", self)

        # フォントを設定して、テキストの大きさを変更します
        font = QFont()
        font.setPointSize(50)  # フォントサイズを設定します
        self.label.setFont(font)

        # ラベルの位置とサイズを設定します
        self.label.setGeometry(150, 0, 800, 300)

        # ボタン1を作成
        self.editlist_button = QPushButton("リスト作成")
        self.editlist_button.clicked.connect(self.editlist)

        # ボタン3を作成
        self.open_button = QPushButton("選択しているジャンルのアプリを起動する")
        self.open_button.clicked.connect(self.fileopen)
        
        #おみくじ関係
        # QLabelを作成して、テキストを設定します
        self.sabu_label = QLabel("Miniゲーム:おみくじ", self)

        # フォントを設定して、テキストの大きさを変更します
        font = QFont()
        font.setPointSize(30)  # フォントサイズを設定します
        self.sabu_label.setFont(font)
        self.sabu_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        # フレームの作成
        self.result_frame = QFrame(self)
        self.result_frame.setFrameShape(QFrame.Box)  # 枠線のスタイルを指定
        self.result_frame.setLineWidth(2)  # 枠線の太さを指定

        # ラベルの作成
        self.result_label = QLabel('ここに結果が表示されます', self.result_frame)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # フレーム内のレイアウトを設定
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.result_label)
        self.result_frame.setLayout(frame_layout)

        # ボタンの作成
        self.draw_button = QPushButton('おみくじを引く', self)
        self.draw_button.clicked.connect(self.drawFortune)

        # タスクを表示するリストウィジェット
        self.task_list = QListWidget()
        self.task_list.setMaximumSize(200,400)
        self.task_list.setMovement(QListWidget.Snap)
        self.task_list.itemDoubleClicked.connect(self.doubleclicked)
        self.task_list.currentItemChanged.connect(self.about)
        self.task_list.itemChanged.connect(self.moved)
        self.task_list.itemPressed.connect(self.taskpressed)

        # 詳細表示
        self.detail = QListWidget()
        self.detail.itemPressed.connect(self.detailpressed)
        self.detail.setMovement(QListWidget.Snap)
        self.detail.itemChanged.connect(self.detailmoved)
        self.detail.itemDoubleClicked.connect(self.detaildoubleclicked)
        self.detail.setAcceptDrops(True)
        
        #リスト定義の削除ボタン
        add_button2 = QPushButton('リスト削除')
        add_button2.clicked.connect(self.delete_todo)


        # レイアウトを作成してリストを配置
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addStretch()  # ボタンを下側に移動するためにストレッチを追加
        layout.addWidget(self.sabu_label)
        layout.addWidget(self.result_frame)
        layout.addWidget(self.draw_button)

        # ボタンの作成
        self.rename_button = QPushButton('グループの名前を変更')
        self.rename_button.clicked.connect(self.rename)

        tasklist_layout = QVBoxLayout()
        tasklist_layout.addWidget(self.task_list)
        tasklist_layout.addWidget(self.rename_button)


        #リストレイアウトを作成
        list_layout = QHBoxLayout()
        list_layout.addLayout(tasklist_layout)
        list_layout.addWidget(self.detail)


        sabu_layout = QHBoxLayout()
        sabu_layout.addWidget(add_button2)
        sabu_layout.addWidget(self.open_button)
        sabu_layout.addWidget(self.editlist_button)

        layout.addLayout(list_layout)
        layout.addLayout(sabu_layout)

        # メインウィジェットにレイアウトをセット
        main_widget.setLayout(layout)

        # ウィンドウのサイズを固定
        self.setFixedSize(800, 600)

        
        # スタイルシートを適用
        self.setStyleSheet("""
            QWidget {
                background-color: #001933;
                color: #fff;
            } 
            #resultFrame {
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 20px;
            }
            QPushButton {
                background-color: #007bff;
                color: #fff;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QListWidget {
                background-color: #fff;
                color: #000;
            }
        """)
        # ToDoリストのアイテムの文字の大きさを変更
        self.task_list.setStyleSheet("font-size: 16px;")

        self.load_tasks()
    #リスト削除
    def delete_todo(self, item):
        selected_task = self.task_list.currentItem().text()
        print("Selected Task:", selected_task)
        # 選択されたToDoアイテムを削除
        for item in self.task_list.selectedItems():
            self.task_list.takeItem(self.task_list.row(item))
        del self.taskdic[selected_task]
        print(self.taskdic)
        # リストを保存
        self.save_tasks()

    def drawFortune(self):
        fortunes = ['大吉', '中吉', '小吉', '吉', '末吉', '凶', '大凶']
        fortune = random.choice(fortunes)
        self.result_label.setText(fortune)

    # keyをロードする関数
    def load_tasks(self):
        if os.path.isfile("taskdata.pickle"):
          with open("taskdata.pickle",'rb') as f:
            dic = pickle.load(f)
          self.taskdic = dic[0]
          keys = dic[1]
          for i in keys:
            self.task_list.addItem(f'{i}')

    def editlist(self):
        #configを実行する
        self.w = c.Config()
        self.w.show()

    def taskpressed(self):
        self.activelist = self.task_list

    def detailpressed(self):
        self.activelist = self.detail

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Delete:
            try:
                for i in self.activelist.selectedItems():
                    if self.activelist == self.task_list:
                        del self.taskdic[i.text()]
                    elif self.activelist == self.detail:
                        del self.taskdic[self.task_list.selectedItems()[0].text()][self.activelist.row(i)]
                    self.activelist.takeItem(self.activelist.row(i))
                self.save_tasks()
            except AttributeError:
                pass

    def fileopen(self):
        # クリックされたToDoリストの要素を取得する関数
        selected_task = self.task_list.currentItem().text()
        print("Selected Task:", selected_task)
        #対応するアプリを開く
        for exe_path in self.taskdic[selected_task]:
           subprocess.Popen(exe_path)

    # keyを保存する関数
    def save_tasks(self):
        keys = [self.task_list.item(i).text() for i in range(self.task_list.count())]
        dic = [self.taskdic,keys]
        print(type(dic))
        with open("taskdata.pickle", "wb") as f:
            pickle.dump(dic, f)

    def doubleclicked(self,item):
        # クリックされたToDoリストの要素を取得する関数
        selected_task = item.text()
        print("Selected Task:", selected_task)
        #対応するアプリを開く
        for exe_path in self.taskdic[selected_task]:
           subprocess.Popen(exe_path,shell = True)

    def detaildoubleclicked(self,item):
        selected_task = self.task_list.selectedItems()[0].text()
        subprocess.Popen(self.taskdic[selected_task][self.detail.row(item)],shell = True)

    def about(self,now):
        self.detail.clear()
        for i in self.taskdic[now.text()]:
            QListWidgetItem(QFileIconProvider().icon(QFileInfo(i)), i[i.rfind("\\")+1:], self.detail)

    def moved(self,item):
        if not len(self.taskdic) == self.task_list.count():
            old = self.task_list.row(self.task_list.selectedItems()[0])
            self.task_list.takeItem(old)
            item.setSelected(True)
            self.save_tasks()
            self.about(item)
        elif self.task_list.isPersistentEditorOpen(item):
            row = self.task_list.row(item)
            key = item.text()
            print(row)
            print(key)
            l = self.taskdic.pop(self.oldkey)
            self.taskdic[key] = l
            self.save_tasks()
            self.task_list.closePersistentEditor(item)
            print(self.taskdic)

    def detailmoved(self,now):
        key = self.task_list.selectedItems()[0].text()
        if not len(self.taskdic[key]) == self.detail.count():
            old = self.detail.row(self.detail.selectedItems()[0])
            now = self.detail.row(now)
            dic = self.taskdic
            if old > now:
                old = old - 1
                p = dic[key].pop(old)
                dic[key].insert(now,p)
            elif old < now:
                now = now - 1
                p = dic[key].pop(old)
                dic[key].insert(now,p)
            self.save_tasks()
            self.about(self.task_list.selectedItems()[0])
            self.detail.item(now).setSelected(True)

    # ドラッグ処理
    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls() and not len(self.task_list.selectedItems()) == 0:
            e.accept()

    # ドロップ処理
    def dropEvent(self, e):
        urls = e.mimeData().urls()
        for i in urls:
            url = i.path()[1:].replace('/',"\\")
            self.taskdic[self.task_list.selectedItems()[0].text()].append(url)
        self.about(self.task_list.selectedItems()[0])
        self.save_tasks()

    def rename(self):
        self.task_list.openPersistentEditor(self.task_list.selectedItems()[0])
        self.oldkey = self.task_list.selectedItems()[0].text()
        self.task_list.setFocus()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
    #runner = TestRunner()
    #runner.run_commands()
