from flask import render_template, url_for, redirect, flash, request
from trash_society import app, db, bcrypt
from trash_society.forms import RegistrationForm, LoginForm, AddProduct
from trash_society.models import User, Category, Product
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def home():
    val = 1
    items = [product for product in Product.query.all()]
    image_file = url_for('static', filename='product_images/default.png')
    if request.args.get('type') == 'all':
        val = 1
        items = [product for product in Product.query.all()]
    elif request.args.get('type') == 'metal':
        val = 2
        items = [product for product in Product.query.all() if product.category.name == request.args.get('type')]
    elif request.args.get('type') == 'wood':
        val = 3
        items = [product for product in Product.query.all() if product.category.name == request.args.get('type')]
    elif request.args.get('type') == 'plastic':
        val = 4
        items = [product for product in Product.query.all() if product.category.name == request.args.get('type')]
    elif request.args.get('type') == 'clothes':
        val = 5
        items = [product for product in Product.query.all() if product.category.name == request.args.get('type')]
    return render_template('home.html', title='Home', image_file=image_file, items=items, val=val)

@app.route('/add_items', methods=['GET', 'POST'])
@login_required
def add_items():
    form = AddProduct()
    form.category_type.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        product_name = form.product_name.data
        product_description = form.description.data
        product_weight = form.product_weight.data
        category_id = form.category_type.data
        product = Product(name=product_name, description=product_description, weight=product_weight, category_id=category_id, user_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('Your product has been added!', 'success')
        return redirect(url_for('add_items'))
    else:
        print("error")
    return render_template('addItems.html', title="Add Items", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', title="Login", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    image_file = url_for('static', filename='product_images/default.png')
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', title=product.name, item=product, image_file=image_file)


@app.route("/product/<int:product_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.category.name == 'clothes':
        current_user.heart_score = current_user.heart_score + (product.category.points_per_kg * product.weight)
    else:
        current_user.green_score = current_user.green_score + (product.category.points_per_kg * product.weight)
    db.session.delete(product)
    db.session.commit()
    flash('Your have bought the item!', 'success')
    return redirect(url_for('home'))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

