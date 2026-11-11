from flask import render_template, redirect, url_for, flash, abort, request, session
from app import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm

@post_bp.route("/post", methods=["GET"])
def list_posts():
    posts = Post.query.all()
    return render_template("all_posts.html", posts=posts)

@post_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author_name = session.get("username", "Anonymous")

        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            author=author_name,
            category=form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.list_posts"))
    return render_template("add_post.html", form=form, legend="New Post")

@post_bp.route("/post/<int:id>", methods=["GET"])
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)

@post_bp.route("/post/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("add_post.html", form=form, legend="Редагувати пост")

@post_bp.route("/post/<int:id>/delete", methods=["POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    flash("Пост видалено успішно!", "success")
    return redirect(url_for("posts.list_posts"))