from PDF_Project import app,ALLOWED_EXTENSIONS
from PDF_Project.forms import Registration,Login,PdfSearch
from flask import render_template,redirect,url_for,flash,request,send_file,send_from_directory
from flask_login import logout_user,login_user,login_required,current_user
from PDF_Project.model import db,User,PDFDetails
from werkzeug.utils import secure_filename
from sqlalchemy import func
import os
from calendar import month_name


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/register',methods=['GET','POST'])
@login_required
def register():
    form = Registration()
    if form.validate_on_submit():
        existingUser = User.query.filter_by(username=form.username.data).first()
        if existingUser is None:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User Created Successfully')
            return redirect(url_for('homepage'))
        else:
            flash('Username or Email id is already exists')
    if form.errors.items() != {}:  # if there is no error in validation
        for form_err in form.errors.values():
            flash(('getting error while creating an user {}'.format(form_err)))
    return render_template('register.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        userObject = User.query.filter_by(username=form.username.data).first()
        if userObject and userObject.check_password(password=form.password.data):
            login_user(userObject)
            flash('Login Successfully Done')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid username or password')
    return render_template('login.html',form=form)



@app.route('/usersummary',methods=['POST','GET'])
@login_required
def usersummary():
    data = PDFDetails.query.with_entities(PDFDetails.uploaded_by,
                                          func.count(PDFDetails.pdfname).label("count")).group_by(PDFDetails.uploaded_by).all()
    return render_template('usersummary.html',data=data)

def get_dict_list_from_result(result):
    list_dict = []
    for i in result:
        i_dict = i._asdict()  # sqlalchemy.util._collections.result , has a method called _asdict()
        list_dict.append(i_dict)
    return list_dict

@app.route('/monthsummary')
@login_required
def monthsummary():
    data = db.session.query(func.strftime('%m', PDFDetails.uploaded_on).label("MONTH"),
                             func.strftime('%Y', PDFDetails.uploaded_on).label("YEAR"),
                             func.count(PDFDetails.pdfname).label("count")).group_by("MONTH","YEAR").all()

    dict = get_dict_list_from_result(data)

    for i in dict :
        for key, value in i.items():
            if key == "MONTH":
                i["MONTH"] = month_name[int(i[key])]
    return render_template('monthsummary.html',data=dict)


def allowed_file(filename):
    if (filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS):
        return True
    else:
        return False

@app.route('/uploadpdf',methods=['POST','GET'])
@login_required
def uploadfile():
    if request.method == 'POST':
        file = request.files['file']
        file_data = request.files['file'].read()
        print(file)
        filename = secure_filename(file.filename)
        if filename is None or filename == '':
            flash('No File Selected')
            return redirect(request.url)
        if filename and allowed_file(filename):
            pdfobject = PDFDetails.query.filter_by(pdfname=secure_filename(filename)).first()
            if pdfobject is None:
                filelocation = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
                newFile = PDFDetails(pdflocation=filelocation,pdfname=secure_filename(filename),pdfdata=file_data,uploader=current_user)
                username = current_user.username
                newFile.set_username(username)
                db.session.add(newFile)
                db.session.commit()
                flash('PDF Uploaded Successfully')
                return redirect(request.url)
            else:
                flash('Mentioned PDF is already uploaded')
                return redirect(request.url)
        flash('Only PDF extensions file can be uploaded')
    return render_template('uploadpdf.html')


@app.route('/pdfsearch/<string:filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=True)

@app.route('/pdfsearch',methods=['POST','GET'])
@login_required
def searchpdf():
    form = PdfSearch()
    pdfObject = ''
    if form.validate_on_submit():
        pdfObject = PDFDetails.query.filter_by(pdfname=form.pdfname.data).first()
        if pdfObject is None:
            flash('Mentioned PDF is not available')
            return redirect(url_for('searchpdf'))
        else:
            flash('Mentioned PDF is available')
            # file= download(pdfObject.pdflocation)
            return render_template('search.html',form=form,data=pdfObject)
    return render_template('search.html',form=form,data=pdfObject)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))