import os
import sys

path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

from src.app import app as application

if __name__ == "__main__":
    application.run()
