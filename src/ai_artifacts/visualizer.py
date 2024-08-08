import os
import json
import subprocess
from typing import List, Dict
import requests

class Visualizer:
    def __init__(self):
        self.artifacts: List[Dict[str, str]] = []
        self.artifacts_file = "artifacts.json"
        self.load_artifacts()
        self.verify_vercel_setup()

    def load_artifacts(self):
        if os.path.exists(self.artifacts_file):
            with open(self.artifacts_file, 'r') as f:
                self.artifacts = json.load(f)

    def save_artifacts(self):
        with open(self.artifacts_file, 'w') as f:
            json.dump(self.artifacts, f, indent=2)

    def add_artifact(self, name: str, artifact_type: str = "generic"):
        self.artifacts.append({"name": name, "type": artifact_type})
        self.save_artifacts()
        print(f"Added artifact: {name}")

    def visualize(self):
        if not self.artifacts:
            print("No artifacts to visualize.")
            return
        print("Visualizing AI Artifacts:")
        for idx, artifact in enumerate(self.artifacts, 1):
            print(f"{idx}. {artifact['name']} (Type: {artifact['type']})")

    def deploy(self, artifact_name: str):
        for artifact in self.artifacts:
            if artifact['name'] == artifact_name:
                print(f"Deploying artifact: {artifact_name}")
                try:
                    # Assurez-vous que Vercel CLI est installé et configuré
                    result = subprocess.run(['vercel', '--yes'], check=True, capture_output=True, text=True)
                    print("Deployment successful!")
                    print(f"Deployment URL: {result.stdout.strip()}")
                    return
                except subprocess.CalledProcessError as e:
                    print(f"Deployment failed: {e}")
                    print(f"Error output: {e.stderr}")
                    return
        print(f"Artifact '{artifact_name}' not found.")

    def list_artifacts(self):
        return [artifact['name'] for artifact in self.artifacts]

    def verify_vercel_setup(self):
        try:
            subprocess.run(['vercel', '--version'], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Vercel CLI not found. Attempting to install...")
            if self.install_vercel_cli():
                print("Vercel CLI installed. Initializing configuration...")
                return self.init_vercel_config()
            return False

    def install_vercel_cli(self):
        try:
            subprocess.run(['npm', 'install', '-g', 'vercel'], check=True)
            print("Vercel CLI installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Vercel CLI: {e}")
            return False

    def init_vercel_config(self):
        try:
            subprocess.run(['vercel', 'init'], check=True, input=b'\n' * 10)  # Appuie sur Entrée pour toutes les questions
            print("Vercel configuration initialized.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to initialize Vercel configuration: {e}")
            return False