import os

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC


class DatasetNotFoundError(Exception):
    pass


class ModelNotFoundError(Exception):
    pass


class UnknownTargetError(Exception):
    pass


class Model():
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    MODEL_FILE = os.path.join(CUR_DIR, "..", "models", "classifier.joblib")

    @classmethod
    def train(cls, dataset_file, target):
        if not os.path.exists(dataset_file):
            raise DatasetNotFoundError(f"Dataset doesn't exist in the directory {dataset_file}")
        df = pd.read_csv(dataset_file, header=0)

        if target not in df.columns:
            raise UnknownTargetError(f"Unknown target column {target}")

        label_encoder = LabelEncoder()
        df[target] = label_encoder.fit_transform(df[target])
        X = df.loc[:, df.columns != target]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        pipeline = Pipeline([
            ('normalizer', StandardScaler()),
            ('clf', SVC())
        ])
        cv_grid = GridSearchCV(pipeline, param_grid={
            'clf__kernel': ['linear', 'rbf'],
            'clf__C': np.linspace(0.1, 1.2, 12)
        })
        cv_grid.fit(X_train, y_train)
        print(f"Best parameters: {cv_grid.best_params_}")
        print(f"Model score: {cv_grid.score(X_test, y_test)}")
        model_to_store = {"model": cv_grid, "label_encoder": label_encoder}
        dump(model_to_store, Model.MODEL_FILE)
        return Model.MODEL_FILE

    @classmethod
    def predict(cls, input_data):
        if not os.path.exists(Model.MODEL_FILE):
            raise ModelNotFoundError(f"Model doesn't exist in the path {Model.MODEL_FILE}")
        model_classifier = load(Model.MODEL_FILE)
        model = model_classifier["model"]
        label_encoder = model_classifier["label_encoder"]
        input_array = np.array([input_data["Sepal.Length"], input_data["Sepal.Width"],
                                input_data["Petal.Length"], input_data["Petal.Width"]])
        prediction = model.predict(input_array.reshape(1, -1))
        return label_encoder.inverse_transform([prediction])
