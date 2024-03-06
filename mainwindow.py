import subprocess
import config as c
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        
        # メインウィジェットを作成
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # ボタン1を作成
        button1 = QPushButton("Button 1")
        button1.clicked.connect(self.on_button1_clicked)

        # ボタン2を作成
        button2 = QPushButton("Button 2")
        button2.clicked.connect(self.on_button2_clicked)

        # レイアウトを作成してボタンを配置
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)

        # メインウィジェットにレイアウトをセット
        main_widget.setLayout(layout)

    def on_button1_clicked(self):
        print("Button 1 clicked")

    def on_button2_clicked(self):
        print("Button 2 clicked")
    
    def __init__(self):
        self.dictionary_list = c.Config.group
        print(c.Config.group)

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
