import subprocess
import win32com.client
import config as c
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        #win32com
        
        # メインウィジェットを作成
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # ボタン1を作成
        button1 = QPushButton("リスト作成")
        button1.clicked.connect(self.on_button1_clicked)

        # ボタン2を作成
        button2 = QPushButton("起動")
        button2.clicked.connect(self.on_button2_clicked)

        # レイアウトを作成してボタンを下側に配置
        layout = QVBoxLayout()
        layout.addStretch()  # ボタンを下側に移動するためにストレッチを追加
        layout.addWidget(button1)
        layout.addWidget(button2)

        # メインウィジェットにレイアウトをセット
        main_widget.setLayout(layout)

        # ウィンドウのサイズを固定
        self.setFixedSize(400, 300)

    def on_button1_clicked(self):
        #configを実行する
        self.w = c.Config()
        self.w.show()


    def on_button2_clicked(self):
        self.doing()
    
    def doing(self):
        self.dictionary_list = c.Config.group
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
