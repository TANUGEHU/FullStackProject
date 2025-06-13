from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, jsonify, request, g
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from models import db, User, Post, Like, Comment
from admin import admin
from flask_cors import CORS
from forms import LoginForm, SignupForm, LogoutForm
from blueprints import profile
from flask_wtf import CSRFProtect
from flask_talisman import Talisman
import secrets

app = Flask(__name__)
CSRFProtect(app)

csp = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        'https://code.jquery.com',
        'https://ajax.googleapis.com',
        'https://cdnjs.cloudflare.com'
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        'https://cdnjs.cloudflare.com'
    ],
    'font-src': [
        "'self'",
        'https://fonts.gstatic.com',
        'https://cdnjs.cloudflare.com'
    ],
    'img-src': [
        "'self'",
        'data:',
        'https:'
    ]
}

Talisman(app, content_security_policy=csp)

app.register_blueprint(profile)

app.secret_key = "thisissecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
admin.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = "loginpage"

@app.before_request
def set_nonce():
    g.nonce = secrets.token_urlsafe(16)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    posts = Post.query.all()
    return render_template("index.html", user=current_user, posts=posts)

@app.route("/watch/<int:id>")
@login_required
def watch(id):
    post = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(post_id=id).all()
    return render_template("watch.html", post=post, comments=comments)

@app.route("/like/<int:id>", methods=["POST"])
@login_required
def like_post(id):
    post = Post.query.get_or_404(id)
    like = Like.query.filter_by(post_id=id, user_id=current_user.id).first()

    if like:
        # Unlike
        db.session.delete(like)
        liked = False
    else:
        # Like
        new_like = Like(post_id=id, user_id=current_user.id)
        db.session.add(new_like)
        liked = True

    db.session.commit()
    like_count = Like.query.filter_by(post_id=id).count()

    return jsonify({"likes": like_count, "liked": liked})

@app.route("/comment", methods=["POST"])
@login_required
def add_comment():
    data = request.get_json()
    content = data.get("comment")
    post_id = data.get("post_id")

    if not content or not post_id:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "status": "success",
        "comment": {
            "username": current_user.username,
            "content": new_comment.content
        }
    })

@app.route("/signup", methods=['GET', 'POST'])
def loginpage():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("You already have an account", category='warning')
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        return redirect(url_for("homepage"))

    return render_template("register/signup.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("homepage"))

    return render_template("register/login.html", form=form)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for("homepage"))
    return render_template("register/logout.html", form=form)

@app.route("/get-medias/<int:id>")
@login_required
def get_media(id):
    media = Post.query.get_or_404(id)
    return send_from_directory("media", media.media)


if __name__=='__main__':
    app.run(debug=True)
