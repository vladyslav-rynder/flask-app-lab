from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")

from app import views
from app.products import product_bp
from app.users import user_bp
from app.resume import resume_bp

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(resume_bp)