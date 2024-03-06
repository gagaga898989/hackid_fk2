import subprocess
import config as t2
import copy

class TestRunner:
    def __init__(self):
        self.dictionary_list = copy.deepcopy(t2.deepcopy)

    def run_commands(self):
        for value in self.dictionary_list.values():
            if isinstance(value, list):
                print(value)
                commands_list = value
                for command in commands_list:
                    subprocess.Popen(command)

if __name__ == "__main__":
    runner = TestRunner()
    runner.run_commands()
