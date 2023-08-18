from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_name.db'
# 24 character Secret Key for Protection. To generate a key, run secrets.token_hex()
app.config['SECRET_KEY'] = '14909cf5d30977cc13b50ed7'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
with open('directory/api_key.txt') as f:
    api_key = f.read()





from directory import routes
from directory import models









