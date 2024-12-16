from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        flash("Login successful!", "success")
        return redirect(url_for("new_client"))
    else:
        flash("Invalid credentials. Try again.", "danger")
        return redirect(url_for("index"))

@app.route("/new-client", methods=["GET", "POST"])
def new_client():
    if request.method == "POST":
        client_id = request.form["id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dob = request.form["dob"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]

        new_client = Client(
            client_id=client_id,
            firstname=firstname,
            lastname=lastname,
            dob=dob,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Client information saved successfully!", "success")
        return redirect(url_for("new_client"))
    return render_template("new_client.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
