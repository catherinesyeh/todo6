# import statements
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # create new app

# /// = relative path, //// = absolute path
# set config parameters
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # create database


# model class for todo items
class Todo(db.Model):
    # each item has id, title, and flag if it's completed or not
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')  # start page
def home():
    todo_list = Todo.query.all()  # get all todos
    # load page
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])  # add new todo
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)  # update database
    db.session.commit()
    return redirect(url_for("home"))  # reolad page


@app.route("/update/<int:todo_id>")  # update todo
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # get item by id
    todo.complete = not todo.complete  # switch completion status
    db.session.commit()  # update database
    return redirect(url_for("home"))  # reload page


@app.route("/delete/<int:todo_id>")  # remove todo
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # get item by id
    db.session.delete(todo)  # update database
    db.session.commit()
    return redirect(url_for("home"))  # reload page


@app.route("/delete_all/")  # delete all todos
def delete_all():
    todo_list = Todo.query.all()  # get all todos
    for todo in todo_list:
        delete(todo.id)  # call delete method
    return redirect(url_for("home"))  # reload page


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # load database
    # setting makes it so we don't have to reload the server each time we change the code
    app.run(debug=True)
