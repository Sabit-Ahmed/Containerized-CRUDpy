import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Blogs(db.Model):
    def __init__(self, title, body):
        self.title = title
        self.body = body
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text())

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/blogs', methods=['POST']) 
def create():
    title = request.form['title']
    body = request.form['body']
    q = Blogs(title, body)
    db.session.add(q)
    db.session.commit()
    blogs = [{ 'id':q.id, 'title':q.title, 'body':q.body}]

    return render_template('Results.html', blogs = blogs)

@app.route('/blogs', methods=['GET']) 
def read():
    q = Blogs.query.all()
    all_rec = []   ### Have to serialize the JSON object
    for i in q:
        all_rec.append({
            'id':i.id,
            'title':i.title,
            'body':i.body
            })
        
    return render_template('Results.html', blogs = all_rec)

@app.route('/blogs/search', methods=['POST']) 
def read_one():
    searchstr = request.form['str']
    q = Blogs.query.filter_by(title=searchstr).first()
    if q:
        blogs = [{'id':q.id, 'title':q.title, 'body':q.body}]
        return render_template('Results.html', blogs = blogs)
    else:
        return "404, Entry not found!"


@app.route('/blogs/update', methods=['POST'])
def update():
    id = request.form['up']
    q = Blogs.query.filter_by(id=id).first()
    blogs = [{'id':q.id, 'title':q.title, 'body':q.body}]
    return render_template('UpdatedForm.html', blogs = blogs)

@app.route('/blogs/update_successfull', methods=['POST'])
def update_successfull():
    id = request.form['beforeId']
    q = Blogs.query.filter_by(id=id).first()
    q.title = request.form['updatedTitle'] if request.form['updatedTitle'] else q.title
    q.body = request.form['updatedBody'] if request.form['updatedBody'] else q.body
    db.session.commit()
    blogs = [{'id':q.id, 'title':q.title, 'body':q.body}]

    return render_template('Results.html', blogs = blogs)


@app.route('/blogs/delete', methods=['POST']) 
def delete():
    id = request.form['del']
    q = Blogs.query.get(id)
    db.session.delete(q)
    db.session.commit()

    return render_template('Results.html', blogs = None)

