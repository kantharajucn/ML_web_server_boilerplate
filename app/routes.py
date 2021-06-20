import logging
import os

from flask import request
from flask_restx import Resource, Namespace, fields
from werkzeug.datastructures import FileStorage

from app.model import Model, ModelNotFoundError, DatasetNotFoundError, UnknownTargetError
from app.utils import store_datasets

logger = logging.getLogger(__name__)


model_create_api = Namespace('create_model', description='API to create ML model')
parser = model_create_api.parser()
parser.add_argument('file', location='files',
                    type=FileStorage, required=True)
parser.add_argument('target', type=str, required=True)


@model_create_api.expect(parser)
@model_create_api.route('')
class CreateResource(Resource):
    @model_create_api.doc('Create ML model')
    def post(self):
        """
        Receive  dataset file from the body, target column as a url parameter and create ML model.
        """
        args = parser.parse_args()
        print(args)
        uploaded_file = args['file']
        target = args["target"]
        logger.info(f"receiving file: {uploaded_file.filename}")
        file_path = store_datasets(uploaded_file)
        try:
            model_file = Model.train(file_path, target)
        except DatasetNotFoundError:
            return {"Error": "Unexpected error while storing the dataset"}, 500
        except UnknownTargetError:
            return {"Error": "Unknown target column"}, 500
        if not os.path.exists(model_file):
            return {"Error": "Model training failed"}, 500
        return {}, 200


model_inference_api = Namespace('model_inference', description='Model inference API')
inference_model = model_inference_api.model('predict', {
    'Sepal.Length': fields.Float(required=True, description='Sepal Length'),
    'Sepal.Width': fields.Float(description='Sepal Width'),
    'Petal.Length': fields.Float(required=True, description='Petal Length'),
    'Petal.Width': fields.Float(required=True, description='Petal Width')
})


@model_inference_api.route('')
class PredictResource(Resource):
    @model_inference_api.doc('Model inference')
    @model_inference_api.expect(inference_model, validate=True)
    def post(self):
        """
        Receives single input data and return the prediction
        """
        input_data = request.json
        try:
            result = Model.predict(input_data)
        except ModelNotFoundError:
            return {"Error": "Model doesn't exist"}, 400

        return {"Result": result[0]}, 200
