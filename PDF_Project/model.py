from PDF_Project import db,login_manager
from flask_login import UserMixin
from datetime import datetime,date
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    users = db.relationship('PDFDetails', backref='uploader',lazy=True)
    # created_on = db.Column(db.DateTime,nullable=False,unique=False)


    def set_password(self,password):
        self.password = generate_password_hash(password,method='sha256')

    def check_password(self,password):
        return check_password_hash(self.password,password)



    def __repr__(self):
        return '<User %r>' % self.username



class PDFDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdflocation = db.Column(db.String(100), unique=False, nullable=False)
    pdfname = db.Column(db.String(40), unique=True, nullable=False)
    pdfdata = db.Column(db.LargeBinary)
    uploaded_on = db.Column(db.DateTime, default=datetime.now())
    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    uploaded_by = db.Column(db.String(50), unique=False, nullable=False)



    def set_username(self,username):
        self.uploaded_by = username

    def get_path(self):
        return self.pdflocation