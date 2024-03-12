import subprocess
import config as c
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QLabel,QListWidget,QMessageBox,QFrame,QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt  # Qtモジュールをインポートする
import os
import random
import pickle

class MainWindow(QMainWindow):
    def __init__(self):
        global mw
        mw = self
        self.taskdic = {}
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
        button1 = QPushButton("リスト作成")
        button1.clicked.connect(self.on_button1_clicked)

        # ボタン3を作成
        button3 = QPushButton("選択しているジャンルのアプリを起動する")
        button3.clicked.connect(self.on_button3_clicked)
        
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
        self.task_list.itemDoubleClicked.connect(self.doubleclicked)
        self.task_list.currentItemChanged.connect(self.about)

        # 詳細表示
        self.detail = QListWidget()
        
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

        list_layout = QHBoxLayout()
        list_layout.addWidget(self.task_list)
        list_layout.addWidget(self.detail)

        sabu_layout = QHBoxLayout()
        sabu_layout.addWidget(add_button2)
        sabu_layout.addWidget(button3)
        sabu_layout.addWidget(button1)

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
            self.taskdic = pickle.load(f)
          keys = self.taskdic.keys()
          for i in keys:
            self.task_list.addItem(f'{i}')

    def on_button1_clicked(self):
        #configを実行する
        self.w = c.Config()
        self.w.show()

    def on_button3_clicked(self):
        # クリックされたToDoリストの要素を取得する関数
        selected_task = self.task_list.currentItem().text()
        print("Selected Task:", selected_task)
        #対応するアプリを開く
        for exe_path in self.taskdic[selected_task]:
           subprocess.Popen(exe_path)

    # keyを保存する関数
    def save_tasks(self):
        with open("taskdata.pickle", "wb") as f:
            pickle.dump(self.taskdic, f)

    def doubleclicked(self,item):
        # クリックされたToDoリストの要素を取得する関数
        selected_task = item.text()
        print("Selected Task:", selected_task)
        #対応するアプリを開く
        for exe_path in self.taskdic[selected_task]:
           subprocess.Popen(exe_path)

    def about(self,now,before):
        self.detail.clear()
        for i in self.taskdic[now.text()]:
            self.detail.addItem(i[i.rfind("\\")+1:])

    def get_application_names(self,*exe_paths):
        application_names = []
        for exe_path in exe_paths:
            # ファイルパスを分割してリストにする
            parts = exe_path.split(os.sep)
            try:
            # ファイルパスから\\Applicationのインデックスを取得する
                app_index = parts.index('C:')
                # アプリケーション名の直前の要素を取得
                app_name = parts[app_index + 2]
                application_names.append(app_name)
            except ValueError:
            # 'Application'が見つからない場合は例外処理を行う
                print(f"'Application'が {exe_path} で見つかりませんでした。")
                continue
        return application_names

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
    #runner = TestRunner()
    #runner.run_commands()
