# Machine learning Web Server

Boilerplate template to build end-end to machine learning model using scikit-learn and deploy the model as REST api using Flask

This boilerplate template provides two end points, one is `create_model` which takes the dataset file and the target field then build training pipeline and persist the model.
The second endpoint is `predict` for model inference, which takes single record and produces the model prediction.

## Usage

### Run server locally

1. Clone the repository
    
    ```git clone https://github.com/kantharajucn/ML_web_server_boilerplate ```
    
2. change directory into the repo
  
    ```cd  path/to/ML_web_server```
 
3. Install requirements
    
    ```pip install -r requirements.txt```
    
4. Run Flask application
    
    ```make run``` 
5. Run tests 
    
    ```make test```
    

### Run server using Docker

1. Build docker image
    
    ```make docker-build```
    
2. Run docker image
    
    ```make docker-run```

3. Run tests 

    ```make docker-test```

3. Stop docker container
    
    ```make docker-down```
    
    Web server is available on the port 8000.    
    
    
