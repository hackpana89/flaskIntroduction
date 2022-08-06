#from asyncio import Task
#from crypt import methods
#from email.policy import default
from urllib import request
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) #to initiate the database in the terminal type 1.python 2.from app import db

class toDo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' % self.id

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = toDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding the new task'
    else:
        tasks = toDo.query.order_by(toDo.date_created).all()
        return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = toDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting that task'


@app.route('/update/<int:id>',methods= ['GET','POST'])
def update(id):
    task = toDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating your task'
    else:
        return render_template('update.html',task=task)


#if there are any erros will pop up
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0',port=5000)
