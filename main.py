# import required libraries 
import os
from flask import Flask, render_template, request, redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy # imports flask version of alchemy
from sqlalchemy.exc import IntegrityError
# import form libraries
from flask import Flask, url_for, render_template, redirect
from forms import add


project_dir = os.path.dirname(os.path.abspath(__file__)) # set up database file
database_file = "sqlite:///{}".format(os.path.join(project_dir, "backpack_challege.db"))


app = Flask(__name__)
app.config["backpack_challenge.db"] = database_file # tells the program where our database will be stored 
app.config["SECRET_KEY"] = "0"



db = SQLAlchemy(app) # initialise connection to database

class Item_class(db.Model): # creates new class called item_class
  # this will create a table called "item_class"
  Item1 = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

  def __repr__(self):
    return "<Item: {}".format(self.Item1)

db.create_all()

# home route
@app.route('/', methods=["GET", "POST"])
def home():
  form = add()
  if request.form:
    item = Item_class(Item1=request.form.get("item")) # gets item input from form and save to new variable 
    try:
      db.session.add(item) # add item to database
      db.session.flush()
    except IntegrityError:
      db.session.rollback()
    else:
      db.session.commit() # commit changes 
  items = Item_class.query.all()
  return render_template("backpack.html", items = items, form=form)
  
#update item
@app.route("/update", methods=["POST"])
def update():
  newitem = request.form.get("newitem")
  olditem = request.form.get("olditem")
  itemquery = Item_class.query.filter_by(Item1=olditem).first()
  itemquery.Item1 = newitem
  db.session.commit() # commit to database 
  return redirect("/")

# delete item
@app.route("/delete", methods=["POST"])
def delete():
    item = request.form.get("item")
    itemquery = Item_class.query.filter_by(Item1=item).first()
    db.session.delete(itemquery) # delete itemquery 
    db.session.commit()
    return redirect("/")

# error handling page 
@app.errorhandler(404)
def error404(e):
  return render_template("404.html", page_title="error_404"), 404

if __name__ == '__main__':
  app.run(debug=True)