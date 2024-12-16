from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Database Configuration
# Replace placeholders with your actual database details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example Table Models (Optional if tables are ready in DB)
class User(db.Model):
    __tablename__ = 'users'  # Existing table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Client(db.Model):
    __tablename__ = 'clients'  # Existing table name
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))

@app.route("/")
def index():
    return render_template("index.html")

# Login Route
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    # Check User in Database
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        flash("Login successful!", "success")
        return redirect(url_for("new_client"))
    else:
        flash("Invalid credentials. Try again.", "danger")
        return redirect(url_for("index"))

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Insert into users table
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists!", "danger")
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("index"))
    return render_template("register.html")

# New Client Route
@app.route("/submit-client", methods=["POST"])
def submit_client():
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

        # Insert into clients table
        new_client = Client(
            client_id=client_id, firstname=firstname, lastname=lastname,
            dob=dob, email=email, phone=phone, address=address, city=city, state=state
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Client information submitted successfully!", "success")
        return redirect(url_for("new_client"))
    return render_template("new_client.html")

@app.route("/new-client", methods=["GET"])
def new_client():
    return render_template("new_client.html")

if __name__ == "__main__":
    app.run(debug=True)
