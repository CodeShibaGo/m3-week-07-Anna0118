# from app import routes, models
from flask import Flask
from dotenv import load_dotenv
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models