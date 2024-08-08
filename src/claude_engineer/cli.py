from ai_artifacts.visualizer import Visualizer
from ai_artifacts.code_executor import CodeExecutor

class CLI:
    def __init__(self):
        self.visualizer = Visualizer()
        self.code_executor = CodeExecutor()

    def process_command(self, command):
        if command.startswith("/visualize"):
            self.visualizer.visualize()
        elif command.startswith("/deploy"):
            _, artifact = command.split(maxsplit=1)
            self.visualizer.deploy(artifact)
        elif command.startswith("/execute"):
            _, code = command.split(maxsplit=1)
            self.code_executor.execute(code)
        elif command.startswith("/add"):
            _, artifact = command.split(maxsplit=1)
            self.visualizer.add_artifact(artifact)
        elif command == "/help":
            self.show_help()
        else:
            print("Unknown command. Type /help for available commands.")

    def show_help(self):
        print("Available commands:")
        print("/visualize - Visualize all artifacts")
        print("/deploy [artifact] - Deploy a specific artifact")
        print("/execute [code] - Execute Python code")
        print("/add [artifact] - Add a new artifact")
        print("/help - Show this help message")
        print("exit - Exit the program")