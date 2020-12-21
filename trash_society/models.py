from trash_society import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    green_score = db.Column(db.Integer, nullable=False, unique=False, default=0)
    heart_score = db.Column(db.Integer, nullable=False, unique=False, default=0)
    posts = db.relationship('Product', backref='seller', lazy=True)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price_per_kg = db.Column(db.Integer, nullable=False, unique=False)
    points_per_kg = db.Column(db.Integer, nullable=False, unique=False)
    produts = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(160), unique=False, nullable=False, default="")
    weight = db.Column(db.Integer, nullable=False, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')

db.create_all()

