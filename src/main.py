import sys
import os
import logging
import yaml
from claude_engineer.cli import CLI
from ai_artifacts.visualizer import Visualizer

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yml')
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def setup_logging(config):
    log_dir = os.path.dirname(config['logging']['file'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        filename=config['logging']['file'],
        level=getattr(logging, config['logging']['level']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    try:
        config = load_config()
        setup_logging(config)
        
        logging.info("Starting Claude Engineer Extended")
        print("Welcome to Claude Engineer Extended!")
        
        cli = CLI()
        visualizer = Visualizer()
        
        while True:
            try:
                command = input("Claude Engineer > ").strip()
                if command == "exit":
                    break
                cli.process_command(command, visualizer)
            except Exception as e:
                logging.error(f"Error processing command: {str(e)}")
                print(f"An error occurred: {str(e)}")
        
        logging.info("Exiting Claude Engineer Extended")
        print("Thank you for using Claude Engineer Extended!")
    except Exception as e:
        print(f"A critical error occurred: {str(e)}")
        logging.critical(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()