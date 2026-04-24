from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.tree_routes import tree_bp
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    # enable cors
    CORS(app)

    # create tables
    Base.metadata.create_all(bind=engine)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tree_bp)

    return app
