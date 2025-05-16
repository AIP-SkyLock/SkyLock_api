from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from src.routes import main_routes  # Import the routes

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# Register the routes
app.register_blueprint(main_routes)