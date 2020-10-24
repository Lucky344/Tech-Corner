from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail
import os
import math
import json
import datetime



app = Flask(__name__)
app.secret_key = 'Admin123'
app.config['UPLOAD_FOLDER'] = "C:\\Users\\shomi\\OneDrive\\Desktop\\Flask\\static"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/coderoad"

db = SQLAlchemy(app)

class Contacts(db.Model):
    
    # sno, name, email, message, date
    
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    
    # sno, title, slug, content, date
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    tagline = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    image = db.Column(db.String(12), nullable=True)

@app.route("/")
def index ():
    posts = Posts.query.filter_by().all()[0:2]
    
    return render_template('index.html', posts=posts)

@app.route("/login/", methods = ['GET', 'POST'])
def sign_in ():
    if 'user' in session and session['user'] == "":
        posts = Posts.query.all()
        return render_template('dashboard.html', posts=posts)

    if request.method == 'POST':
        # redirect user
        username = request.form.get('user_name')
        userpass = request.form.get('pass')
        if username == "" and userpass == "":
            # session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', posts=posts)

    else:
        return render_template('login.html')

@app.route("/logout/")
def logout():
    session.pop('user')
    return redirect('/login/')

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
     if 'user' in session and session['user'] == "":
         post = Posts.query.filter_by(sno=sno).first()
         db.session.delete(post)
         db.session.commit()
     return redirect('/login/')



@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route (post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', post=post)

@app.route("/about/")
def about():
    return render_template('about.html') 

@app.route("/uploader/", methods = ['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == "":
      if(request.method=='POST'):
          f = request.files['file1']
          f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
          return "Uploaded Successfully"


@app.route("/contact/", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        # Add entry to the database
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contacts(name=name, message=message, date=datetime.date.today(), email=email )
        db.session.add(entry)
        db.session.commit()
        #mail.send_message('Message from ' + name, sender=email, recipients='luckyverma873@gmail.com', body = message )
    return render_template('contact.html')

@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == "":
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.date.today()

            if sno == '0':
                post = Posts(title=box_title, tagline=tline, slug=slug, content=content, image=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.tagline = tline
                post.slug = slug
                post.content = content
                post.image = img_file
                post.date = date
                db.session.commit()
                return redirect('/edit/'+ sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', post=post)


app.run(debug=True)

