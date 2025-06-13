from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, db, Post

admin = Admin()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
