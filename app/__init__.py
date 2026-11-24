import os
from app.config import config_dict
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, instance_relative_config=True)

    current_config = config_dict.get(config_name, config_dict['default'])
    app.config.from_object(current_config)
    app.config["SQLALCHEMY_ECHO"] = True

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    from app.posts.models import Post
    from app.posts.models import Tag
    from app.users.models import User
    from app import views
    from app.products import product_bp
    from app.users import user_bp
    from app.resume import resume_bp
    from app.views import main_bp

    from app.posts import post_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(resume_bp)

    app.register_blueprint(post_bp)

    return app



