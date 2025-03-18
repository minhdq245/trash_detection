import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.app import app

if __name__ == "__main__":
    app.run()
