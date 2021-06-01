from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app = Flask(__name__,template_folder='../../PDFUploader/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['SECRET_KEY'] ='d58bc2f472dfa4ea5592ca97'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/abdul/Desktop/PDFUploader/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
# UPLOAD_FOLDER = '../../PDFuploader/uploads/'
ALLOWED_EXTENSIONS = ('pdf')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from PDF_Project import routes
