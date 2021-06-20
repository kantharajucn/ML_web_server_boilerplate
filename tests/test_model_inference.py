from json import dumps

import pytest
import os


def test_model_inference_success(test_client, input_line):
    """
    API /predict' with the valid input results model inference success and return the status code 200
    """
    response = test_client.post('/predict',
                                data=dumps(input_line),
                                content_type="application/json")
    assert response.status_code == 200


def test_model_inference_fails(test_client, input_line):
    """
    API /predict' with the invalid input results model inference fails and return the status code 400
    """
    response = test_client.post('/predict',
                                data=dumps({"test": 123}),
                                content_type="application/json")
    assert response.status_code == 400


@pytest.mark.run(order=-1)
def test_model_inference_no_model_fails(test_client, input_line):
    """
    API /predict' with the invalid input but model doesn't exists in the model directory results response code 400
    """

    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    MODEL_FILE = os.path.join(CUR_DIR, "..", "models", "classifier.joblib")
    os.remove(MODEL_FILE)

    response = test_client.post('/predict',
                                data=dumps(input_line),
                                content_type="application/json")
    assert response.status_code == 400
