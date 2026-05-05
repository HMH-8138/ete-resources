import os
import sys

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
from app import app

# This is the application object that PythonAnywhere will use
application = app
