import subprocess
import win32com.client
import config as c
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QLabel,QListWidget
from PySide6.QtGui import QFont
import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
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

        button = QPushButton('Click me!')
        button.setFixedSize(100, 50)  # 幅100、高さ50に設定

        # ボタン1を作成
        button1 = QPushButton("リスト作成")
        button1.clicked.connect(self.on_button1_clicked)

        # ボタン2を作成
        button2 = QPushButton("起動")
        button2.clicked.connect(self.on_button2_clicked)

        # ボタン3を作成
        button3 = QPushButton("選択してるジャンルのアプリを起動する")
        button3.clicked.connect(self.on_button3_clicked)
        
        # タスクを表示するリストウィジェット
        self.task_list = QListWidget()


        # レイアウトを作成してボタンを下側に配置
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addStretch()  # ボタンを下側に移動するためにストレッチを追加
        layout.addWidget(self.task_list)
        layout.addWidget(button3)
        layout.addWidget(button1)
        layout.addWidget(button2)

        # メインウィジェットにレイアウトをセット
        main_widget.setLayout(layout)

        # ウィンドウのサイズを固定
        self.setFixedSize(800, 600)

        self.load_tasks()
    # keyをロードする関数
    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
                print(tasks)
                for task in tasks:
                    self.task_list.addItem(task)
        except FileNotFoundError:
            pass

    def on_button1_clicked(self):
        #configを実行する
        self.w = c.Config()
        self.w.show()


    def on_button2_clicked(self):
        self.doing()

    def on_button3_clicked(self):

        # JSONファイルからデータを読み込む
        #with open("data.json", "r") as json_file:
            #loaded_data = json.load(json_file)

        # 読み込んだデータを反映する
        #self.dictionary_list = loaded_data
        #print(loaded_data)
        #self.run_commands()
        # クリックされたToDoリストの要素を取得する関数
        selected_task = self.task_list.currentItem().text()
        print("Selected Task:", selected_task)
        # ユーザーからキーを入力
        key = selected_task
        file_name = f"{key}.json"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data = json.load(file)
            print("File contents:", data)
        else:
            print(f"File '{file_name}' does not exist.")
        #対応するアプリを開く
        #if isinstance(data, str):
        print(data)
        for exe_path in data:
           subprocess.Popen(exe_path)
    # keyを保存する関数
    def save_tasks(self):
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
        with open('tasks.json', 'w') as file:
            json.dump(tasks, file)

    
    def doing(self):
        self.dictionary_list = c.Config.group
        for key, value_list in c.Config.group.items():
            self.task_list.addItem(key)
            self.save_tasks()
            with open(f"{key}.json", "w") as file:
                json.dump(value_list, file)

        self.run_commands()

    def run_commands(self):
        key = "test"
        for value in self.dictionary_list[key]:
            if isinstance(value, str):
                print(value)
                subprocess.Popen(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
    #runner = TestRunner()
    #runner.run_commands()
