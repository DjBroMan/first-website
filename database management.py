from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
os.chdir("C:/Users/divij/OneDrive/Desktop/codes/python codes/Python Lec/udemy learning/backend web developement python/with database/day-69-starting-files-blog-with-users/with relational database")
# Import your forms from the forms.py
from forms import CreatePostForm


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login's Login Manager
login_manager=LoginManager()
login_manager.init_app(app=app)



# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Foreign key column for the author (User)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    # Establishing the many-to-one relationship
    author = relationship("User", back_populates="posts")

    #***************Parent Relationship*************#
    comments = relationship("Comment", back_populates="parent_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text:Mapped[str]= mapped_column(Text,nullable=False)

    # Foreign key column for the author (User)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")    

    # Establishing the many-to-one relationship
    comment_author = relationship("User", back_populates="comments")

    

# TODO: Create a User table for all your registered users. 
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    authority:Mapped[str] = mapped_column(String(100))

    # Establishing the one-to-many relationship
    posts = relationship("BlogPost", back_populates="author")

    # Establishing the one-to-many relationship
    comments = relationship("Comment", back_populates="comment_author")


with app.app_context():
    db.create_all()
