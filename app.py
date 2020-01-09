from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///post.db'
db = SQLAlchemy(app)

# creation of models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100),nullable=False, default='Unknown')
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'blog post '+str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

all_post = [
    {
        'title':'the post 1',
        'content':'this the ruch hour book',
        'author': 'Grace B.',
    },
    {
        'title':'the post 2',
        'content':'this is the time of cutting down',
    },
    {
        'title':'the post 3',
        'content':'this is to know all about Sierra',
        'author': 'Efo Perso'
    },
]

@app.route('/post', methods=['POST','GET'])
def blog():
    if(request.method == 'POST'):
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post')
    else:
        all_post = BlogPost.query.order_by(BlogPost.date_pub).all()
        return render_template('posts.html', posts=all_post)

@app.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if(request.method == 'POST'):
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('edit.html', post=post)
@app.route('/post/new')
def new_post():
    if (request.method == 'POST'):
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('new_post.html')
if(__name__ == '__main__'):
    app.run(debug=True)
