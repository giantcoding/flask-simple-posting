from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/pys.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
database = SQLAlchemy(app)

# Database tables
class Post(database.Model):
    __tablename__ = "posts"
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    date = database.Column(database.DateTime, default=datetime.now)
    text = database.Column(database.String, nullable=False)
    database.create_all()

# Routes
@app.route("/")
def home():
    post = Post.query.all()
    return render_template("home.html", posts=post)

@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    post_id = request.form.get("post_id")
    post = database.session.query(Post).filter(Post.id == post_id).first()
    database.session.delete(post)
    database.session.commit()
    return redirect("/")
    


@app.route("/create", methods=["POST"])
def create_post():
    title = request.form.get("title")
    text = request.form.get("text")  
    post = Post(title=title, text=text)  
    database.session.add(post)
    database.session.commit()
    print(title)
    print(text)
    return redirect(url_for("home"))
   

if __name__ == "__main__":
    app.run(debug=True)