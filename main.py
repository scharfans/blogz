from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'abcdefg12345'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.username = username
        self.password = password

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect ('/newpost')
        else:
            flash('User password is incorrect, or username does not exist', 'error')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/newpost')
        else:
            flash('Username already exists', 'error')



@app.route('/blog', methods=['POST', 'GET'])
def main_blog():
    blog_id = ""
    
    if (request.args.get('id')) != None:
        blog_id = int(request.args.get('id'))
        Blog_ind = Blog.query.get(blog_id)
        blog_body = str(Blog_ind.body)
        blog_title = str(Blog_ind.title)
        return render_template('individual.html',blogtitle=blog_title,
        blogbody=blog_body)

    else:
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
    owner = User.query.filter_by(username=session['username'.first])
        
    if len(blog_title) < 1:
        blogtitle_error = 'Please fill in the title'
    
    if len(blog_body) < 1:
        blogbody_error = 'Please fill in the body'
    
    if not blogtitle_error and not blogbody_error:
        new_blogentry = Blog(blog_title, blog_body, owner)
        db.session.add(new_blogentry)
        db.session.commit()
        
        new_blogentry_id_ = '/blog?id='+str(new_blogentry.id)
        return redirect(new_blogentry_id_)
    
    else:
        return render_template('entry.html',title="Build a Blog",blogtitle=blog_title, blogtitle_error=blogtitle_error, blogbody=blog_body,blogbody_error=blogbody_error)

if __name__ == '__main__':
    app.run()