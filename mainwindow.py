import subprocess
import config as c
import sys
import PySide6.QtWidgets as Qw

class TestRunner:
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
    runner = TestRunner()
    runner.run_commands()