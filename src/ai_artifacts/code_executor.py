import subprocess
import tempfile
import os

class CodeExecutor:
    def __init__(self):
        self.sandbox_dir = tempfile.mkdtemp(prefix="ai_sandbox_")

    def execute(self, code: str):
        # Create a temporary Python file
        temp_file = os.path.join(self.sandbox_dir, "temp_script.py")
        with open(temp_file, "w") as f:
            f.write(code)

        try:
            # Execute the code in a subprocess
            result = subprocess.run(["python", temp_file], 
                                    capture_output=True, 
                                    text=True, 
                                    timeout=30)  # 30-second timeout
            
            if result.returncode == 0:
                print("Code executed successfully:")
                print(result.stdout)
            else:
                print("Error executing code:")
                print(result.stderr)
        
        except subprocess.TimeoutExpired:
            print("Execution timed out after 30 seconds")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up the temporary file
            os.remove(temp_file)

    def __del__(self):
        # Clean up the sandbox directory when the object is destroyed
        for root, dirs, files in os.walk(self.sandbox_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.sandbox_dir)