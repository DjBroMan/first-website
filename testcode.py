import os
os.chdir("C:/Users/divij/OneDrive/Desktop/codes/python codes/Python Lec/udemy learning/backend web developement python/with database/day-69-starting-files-blog-with-users/with relational database")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

def raw_query():
    # Example of executing a raw SQL query
    result = db.session.execute(text("SELECT * FROM blog_posts"))
    comments = result.fetchall()
    
    with open("post_data.txt",'w') as file:
        for row in comments:
            for data in tuple(row):
                file.write(str(data)+'\n')  # Print each row in the result set
       

with app.app_context():
    raw_query()
