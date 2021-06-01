from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField,SubmitField,FileField
from wtforms.validators import Email,DataRequired,Length,EqualTo

class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=25,message='UserName must macth with the criteria')])
    email = StringField('Email ID', validators=[DataRequired(),Email()])
    password = PasswordField('New Password',validators=[DataRequired(),EqualTo('confirm', message='Passwords must match'),Length(min=4, max=25)])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Submit")


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log In")

class UploadFile(FlaskForm):
    file = FileField('Please Select PDF File From Your System')
    submit = SubmitField('Upload')




class PdfSearch(FlaskForm):
    pdfname = StringField('Kindly Enter PDFName', validators=[DataRequired()])
    submit = SubmitField("Search")