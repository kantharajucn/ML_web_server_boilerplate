import pytest


@pytest.mark.run(order=1)
def test_create_model_success(test_client, dataset):
    """
    API /create?target=Species' with the valid dataset file results model creation success and return the status code 200
    """
    response = test_client.post('/create?target=Species',
                                data={"file": dataset},
                                content_type="multipart/form-data")
    assert response.status_code == 200


def test_create_model_with_wrong_target(test_client, dataset):
    """
    API /create?target=Test should result status code 500 because invalid target column
    """
    response = test_client.post('/create?target=Test',
                                data={"file": dataset},
                                content_type="multipart/form-data")
    assert response.status_code == 500


def test_create_model_without_file(test_client, dataset):
    """
    API /create?target=Species without dataset file in formData should result status code 400.
    """
    response = test_client.post('/create?target=Species',
                                data={"file": "No file"},
                                content_type="multipart/form-data")
    assert response.status_code == 400


def test_create_model_without_target(test_client, dataset):
    """
    API /create with valid dataset file in formData should result status code 400.
    """
    response = test_client.post('/create',
                                data={"file": dataset},
                                content_type="multipart/form-data")
    assert response.status_code == 400
