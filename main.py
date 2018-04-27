from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog_main.html',title="Build a Blog", 
        blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def main_blog():

    blogs = Blog.query.all()
    return render_template('blog_main.html',title="Build a Blog", 
        blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blogtitle']
        blog_body = request.form['blogbody']
        new_blogentry = Blog(blog_title, blog_body)
        db.session.add(new_blogentry)
        db.session.commit()

        return redirect ('/blog')
    
    else:
        return render_template('entry.html',title="Build a Blog")

if __name__ == '__main__':
    app.run()