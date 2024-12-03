from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
bcrypt = Bcrypt(app)

logging.basicConfig(level=logging.DEBUG)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    year_of_purchase = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('products', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('signin'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating user: {e}")
            flash("Username already exists.", "danger")
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('signin'))

@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username)

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        year_of_purchase = request.form['year_of_purchase']
        condition = request.form['condition']
        description = request.form['description']

        new_product = Product(
            name=name,
            price=float(price),
            year_of_purchase=int(year_of_purchase),
            condition=condition,
            description=description,
            user_id=current_user.id
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            flash("Your bike has been listed for sale!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while listing bike: {e}")
            flash("An error occurred while listing your bike. Please try again.", "danger")
            return redirect(url_for('sell'))

    return render_template('sell.html')

@app.route('/buy')
@login_required
def buy():
    products = Product.query.all()
    return render_template('buy.html', products=products)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit(product_id):
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        flash("You do not have permission to edit this product.", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.year_of_purchase = request.form['year_of_purchase']
        product.condition = request.form['condition']
        product.description = request.form['description']

        try:
            db.session.commit()
            flash("Your bike has been updated!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while updating bike: {e}")
            flash("An error occurred while updating your bike. Please try again.", "danger")
            return redirect(url_for('edit', product_id=product.id))

    return render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete(product_id):
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        flash("You do not have permission to delete this product.", "danger")
        return redirect(url_for('home'))

    try:
        db.session.delete(product)
        db.session.commit()
        flash("Your bike has been deleted from the listings.", "success")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while deleting bike: {e}")
        flash("An error occurred while deleting your bike. Please try again.", "danger")

    return redirect(url_for('home'))

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}")
    return "500 error", 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f"Not Found: {error}")
    return "404 error", 404

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
