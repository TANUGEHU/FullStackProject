from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from forms import UploadForm, UpdateForm
from models import Post, db
from werkzeug.utils import secure_filename
import os

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/')
@login_required
def homepage():
    posts = Post.query.all()
    return render_template('profile/index.html', user=current_user, posts=posts)

@profile.route("/upload", methods=["GET", "POST"])
def uploadpage():
    form = UploadForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        post = form.post.data
        filename = secure_filename(post.filename)
        post.save("media/" + filename)

        post = Post(title=title, description=description, media=filename, media_type=post.mimetype, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("homepage"))

    return render_template("profile/upload.html", form=form)

@profile.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_post(id):
    form = UpdateForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        post.title = title
        post.description = description
        db.session.commit()
        return redirect(url_for("homepage"))

    return render_template("profile/update.html", form=form, post=post)

@profile.route("/delete/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    os.remove("media/" + post.media)
    return redirect(url_for("homepage"))
