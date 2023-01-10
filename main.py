from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime
import os
from registration_request_notice import NotificationManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
year = datetime.now().year

# Creating database for regulations.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///legislation.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

notification_manager = NotificationManager()

login_manager = LoginManager()
login_manager.init_app(app)


# Creating Database Table for Legislation
class Legislation(db.Model):
    __tablename__ = "regulations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String, nullable=False)


# Creating Database Table for Users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(100), nullable=False)


# db.create_all()

# To manually register users for now.
def register_user(name, email, password):
    hashed_and_salted_password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=6)
    new_user = User(name=name,
                    email=email,
                    password=hashed_and_salted_password)
    db.session.add(new_user)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# For registration requests
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        notification_manager.send_email_notification(name=name, email=email, message=message)
        return redirect(url_for('home'))
    return render_template("register.html")


@app.route("/")
def home():
    return render_template("index.html", year=year)


@app.route("/approve", methods=["GET", "POST"])
@login_required
def approvals():
    if current_user.id != 1:
        return redirect(url_for('home'))
    if current_user.id == 1 and request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email').lower()
        password = request.form.get('password')
        register_user(name=name, email=email, password=password)
        return redirect(url_for('home'))
    return render_template('dashboard.html')


@app.route("/update", methods=["GET", "POST"])
@login_required
def updates():
    if current_user.id != 1:
        return redirect(url_for('home'))
    if current_user.id == 1 and request.method == "POST":
        email = request.form.get('email').lower()
        user = User.query.filter_by(email=email).first()
        new_password = request.form.get('password')
        if not user:
            flash("This user is not in our user list.")
            return redirect(url_for('updates'))
        elif user:
            user.password = generate_password_hash(password=new_password, method='pbkdf2:sha256', salt_length=6)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('updates.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").lower()
        entered_password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email doesn't exist, please try again.")
            return redirect(url_for('login'))
        elif user:
            password = check_password_hash(pwhash=user.password, password=entered_password)
            if not password:
                flash("password incorrect, please try again")
                return redirect(url_for('login'))
            elif password:
                login_user(user=user)
                return redirect(url_for('home'))
    return render_template("login.html", year=year)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/dashboard", methods=["GET", "POST"])
# @login_required
# def test_dashboard():
#     return render_template("dashboard.html")


@app.route("/fica", methods=["GET", "POST"])
@login_required
def fica():
    if request.method == "POST":
        name = current_user.name
        email = current_user.email
        message = request.form.get("message")
        notification_manager.send_email_notification(name=name, email=email, message=message)
    return render_template("fica.html")


@app.route("/fais", methods=["GET", "POST"])
@login_required
def fais():
    if request.method == "POST":
        name = current_user.name
        email = current_user.email
        message = request.form.get("message")
        notification_manager.send_email_notification(name=name, email=email, message=message)
    return render_template("fais.html")


@app.route("/cisca", methods=["GET", "POST"])
@login_required
def cisca():
    if request.method == "POST":
        name = current_user.name
        email = current_user.email
        message = request.form.get("message")
        notification_manager.send_email_notification(name=name, email=email, message=message)
    return render_template("cisca.html")


@app.route("/insure18", methods=["GET", "POST"])
@login_required
def insurance_act():
    if request.method == "POST":
        name = current_user.name
        email = current_user.email
        message = request.form.get("message")
        notification_manager.send_email_notification(name=name, email=email, message=message)
    return render_template("insure18.html")


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
