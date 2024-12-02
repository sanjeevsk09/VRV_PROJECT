from flask_sqlalchemy import SQLAlchemy
from main import db,bcrypt

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