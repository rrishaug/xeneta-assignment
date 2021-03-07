from flask import Flask

from . database import database, migrate, SQLALCHEMY_DATABASE_URI

from . index import index_bp
from . rates import rates_bp

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(index_bp)
    app.register_blueprint(rates_bp)

    return app
