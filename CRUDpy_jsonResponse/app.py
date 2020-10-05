import os
from flask import Flask, request, jsonify
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
    return jsonify(message='Hello world!'), 200

@app.route('/blogs', methods=['POST']) 
def create():
    title = request.json['title']
    body = request.json['body']
    q = Blogs(title, body)
    db.session.add(q)
    db.session.commit()

    return jsonify(message='Blog is created!', data={ 'title':q.title, 'body':q.body }), 201

# @app.route('/blogs', methods=['GET']) 
# def read():
#     q = Blogs.query.all()
#     return jsonify(message='Existing blogs are here', data=str(q)), 200

@app.route('/blogs', methods=['GET']) 
def read():
    q = Blogs.query.all()
    all_rec = []   ### Have to serialize the JSON object
    for i in q:
        all_rec.append({
            'title':i.title,
            'body':i.body
            })
        
    return jsonify(message='Existing blogs are here', data=all_rec), 200

@app.route('/blogs/<id>') 
def read_one(id):
    q = Blogs.query.get(id)
    return jsonify(message='The specified blog is here', data={ 'id':q.id, 'title':q.title, 'body':q.body }), 200

@app.route('/blogs/<id>', methods=['PUT']) 
def update(id):
    q = Blogs.query.filter_by(id=id).first()
    q.title = request.json['title'] if request.json['title'] else q.title
    q.body = request.json['body'] if request.json['body'] else q.body
    db.session.commit()

    return jsonify(message='Blog is updated!', data={'title':q.title, 'body':q.body }), 200

@app.route('/blogs/<id>', methods=['DELETE']) 
def delete(id):
    q = Blogs.query.get(id)
    db.session.delete(q)
    db.session.commit()
    return jsonify(message='Blog is deleted!'), 200
