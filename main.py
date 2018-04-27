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

@app.route('/newpost')
def newpost():
    return render_template('entry.html',title="Build a Blog")


@app.route('/newpost', methods=['POST'])
def validation():
    blog_title = str(request.form['blogtitle'])
    blog_body = str(request.form['blogbody'])
    blogtitle_error = ''
    blogbody_error = ''
        
    if len(blog_title) < 1:
        blogtitle_error = 'Please fill in the title'
    
    if len(blog_body) < 1:
        blogbody_error = 'Please fill in the body'
    
    if not blogtitle_error and not blogbody_error:
        new_blogentry = Blog(blog_title, blog_body)
        db.session.add(new_blogentry)
        db.session.commit()
        return redirect ('/blog')
    
    else:
        return render_template('entry.html',title="Build a Blog",blogtitle=blog_title, blogtitle_error=blogtitle_error, blogbody=blog_body,blogbody_error=blogbody_error)

if __name__ == '__main__':
    app.run()