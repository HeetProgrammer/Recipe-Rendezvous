from directory import db
from directory import bcrypt
from directory import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hashed = db.Column(db.String(length=60), nullable=False)
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hashed = bcrypt.generate_password_hash(plain_text_password).decode()
    
    def check_password_correction(self, attempted_pwd):
        return bcrypt.check_password_hash(self.password_hashed, attempted_pwd)