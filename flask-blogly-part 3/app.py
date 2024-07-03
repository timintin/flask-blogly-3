
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# Tag routes
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/new', methods=["GET", "POST"])
def new_tag():
    if request.method == "POST":
        name = request.form['name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')
    return render_template('new_tag.html')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "POST":
        tag.name = request.form['name']
        db.session.commit()
        return redirect('/tags')
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

# Update Post routes
@app.route('/posts/new', methods=["GET", "POST"])
def new_post():
    users = User.query.all()
    tags = Tag.query.all()
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        tag_ids = request.form.getlist('tag_ids')
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=new_post.id, tag_id=tag_id)
            db.session.add(post_tag)
        db.session.commit()
        return redirect('/')
    return render_template('new_post.html', users=users, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    users = User.query.all()
    tags = Tag.query.all()
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        post.user_id = request.form['user_id']
        post.tags = []
        tag_ids = request.form.getlist('tag_ids')
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=post.id, tag_id=tag_id)
            db.session.add(post_tag)
        db.session.commit()
        return redirect(f'/posts/{post.id}')
    return render_template('edit_post.html', post=post, users=users, tags=tags)
