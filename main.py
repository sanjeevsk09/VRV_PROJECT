from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from service import role_required


# Initialize Flask app and extensions
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sanjeev%40123@localhost:3306/your_db_vrv"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    role = db.relationship("Role", backref="users")

    @property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, raw_password):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def verify_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)
    
def setup_db():
    db.create_all()

    if not Role.query.first():
        admin_role = Role(name="Admin", description="Administrator role")
        user_role = Role(name="User", description="Regular user role")
        db.session.add_all([admin_role, user_role])
        db.session.commit()


# Utility function: Role-based Access Control (RBAC)


# Routes
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"]  # Ensure valid role ID is provided
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.verify_password(data["password"]):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role.name})
    return jsonify(access_token=access_token), 200

@app.route("/admin", methods=["GET"])
@jwt_required()
@role_required("Admin")
def admin_panel():
    return jsonify({"msg": "Welcome, Admin!"})

@app.route("/user", methods=["GET"])
@jwt_required()
@role_required("User")
def user_panel():
    return jsonify({"msg": "Welcome, User!"})

# Database setup


if __name__ == "__main__":
    with app.app_context():  # Ensure an application context is active
        setup_db()  # Initialize the database and seed roles
    app.run(port=8080)
