from flask_restx import Api
from flask import Blueprint
from flask import Flask

from app.routes import model_create_api, model_inference_api


def create_app():
    flask_app = Flask(__name__)
    blueprint = Blueprint('api', __name__)

    api = Api(blueprint,
              title='ML Server',
              version='0.0.1',
              description='Endpoints to communicate with the frontend.'
              )

    api.add_namespace(model_create_api, path='/create')
    api.add_namespace(model_inference_api, path='/predict')

    flask_app.register_blueprint(blueprint)
    return flask_app
