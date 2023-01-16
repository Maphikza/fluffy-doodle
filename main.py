from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response
from datetime import datetime
import os
from registration_request_notice import NotificationManager
from mongo import UserAccess

app = Flask(__name__)
database = UserAccess()

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

year = datetime.now().year

# Creating database for regulations.

notification_manager = NotificationManager()

ADMIN = os.environ.get('admin')


def register_user(name, email, password):
    database.register_user(name, email, password)


# For registration requests
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email').lower()
        message = request.form.get('message')
        notification_manager.send_email_notification(name=name, email=email, message=message)
        return redirect(url_for('home'))
    return render_template("register.html")


@app.route("/")
def home():
    if "authorised" in session:
        return render_template("index.html", year=year, authorised=session["authorised"])
    else:
        session["current_user"] = "unknown"
        session["authorised"] = False

    return render_template("index.html", year=year, authorised=session["authorised"])


@app.route("/approve", methods=["GET", "POST"])
def approvals():
    if session["current_user"] != str(ADMIN):
        return redirect(url_for('home'))
    if session["current_user"] == str(ADMIN) and request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email').lower()
        password = request.form.get('password')
        register_user(name=name, email=email, password=password)
        return redirect(url_for('home'))
    return render_template('dashboard.html', authorised=session["authorised"])


@app.route("/update", methods=["GET", "POST"])
def updates():
    if session["current_user"] != str(ADMIN):
        return redirect(url_for('home'))
    if session["current_user"] == str(ADMIN) and request.method == "POST":
        email = request.form.get('email').lower()
        valid_user = database.is_user(email)
        new_password = request.form.get('password')
        if not valid_user:
            flash("This user is not in our user list.")
            return redirect(url_for('updates'))
        elif valid_user:
            if database.update(email, new_password)[0]:
                flash(database.update(email, new_password)[1])
                return redirect(url_for('home'))
    return render_template('updates.html', authorised=session["authorised"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").lower()
        entered_password = request.form.get("password")
        valid_user = database.is_user(email)
        if not valid_user:
            flash("That email doesn't exist, please try again.")
            return redirect(url_for('login'))
        elif valid_user:
            password = database.check_password(email, entered_password)
            if not password:
                flash("password incorrect, please try again")
                return redirect(url_for('login'))
            elif password:
                session["authorised"] = True
                session["current_user"] = str(database.search(email))
                return redirect(url_for('home'))
    return render_template("login.html", year=year)


@app.route('/logout')
def logout():
    session["authorised"] = False
    return redirect(url_for('home'))


@app.route("/fica", methods=["GET", "POST"])
def fica():
    if session["authorised"]:
        if request.method == "POST":
            user_identity_no = session["current_user"]
            message = request.form.get("message")
            notification_manager.send_email_notification(name=user_identity_no, message=message)
        return render_template("fica.html", authorised=session["authorised"])
    else:
        flash("You are not authorised to be on this page.")
        return redirect(url_for('login'))


@app.route("/fais", methods=["GET", "POST"])
def fais():
    if session["authorised"]:
        if request.method == "POST":
            user_identity_no = session["current_user"]
            message = request.form.get("message")
            notification_manager.send_email_notification(name=user_identity_no, message=message)
        return render_template("fais.html", authorised=session["authorised"])
    else:
        flash("You are not authorised to be on this page.")
        return redirect(url_for('login'))


@app.route("/cisca", methods=["GET", "POST"])
def cisca():
    if session["authorised"]:
        if request.method == "POST":
            user_identity_no = session["current_user"]
            message = request.form.get("message")
            notification_manager.send_email_notification(name=user_identity_no, message=message)
        return render_template("cisca.html", authorised=session["authorised"])
    else:
        flash("You are not authorised to be on this page.")
        return redirect(url_for('login'))


@app.route("/insure18", methods=["GET", "POST"])
def insurance_act():
    if session["authorised"]:
        if request.method == "POST":
            user_identity_no = session["current_user"]
            message = request.form.get("message")
            notification_manager.send_email_notification(name=user_identity_no, message=message)
        return render_template("insure18.html", authorised=session["authorised"])
    else:
        flash("You are not authorised to be on this page.")
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
