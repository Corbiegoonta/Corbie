import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from zenml import step, pipeline
from typing_extensions import Annotated
import pandas as pd
from typing import Tuple


def train_test() -> None:
    digits = load_digits()
    data = digits.images.reshape(len(digits.images), -1)
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.2, shuffle=False
    )
    model = SVC(gamma=0.001)
    model.fit(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    print(f"Test accuracy: {test_acc}")
    pass

@step
def importer() -> Tuple[
    Annotated[np.ndarray, "X_train"],
    Annotated[np.ndarray, "X_test"],
    Annotated[np.ndarray, "y_train"],
    Annotated[np.ndarray, "y_test"],
]:
    digits = load_digits()
    data = digits.images.reshape(len(digits.images), -1)
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.2, shuffle=False
    )
    return X_train, X_test, y_train, y_test

@step
def svc_trainer(
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> ClassifierMixin:
    model = SVC(gamma=0.001)
    model.fit(X_train, y_train)
    return model

@step
def evaluator(
    X_test: np.ndarray,
    y_test: np.ndarray,
    model: ClassifierMixin,
) -> float:
    test_acc = model.score(X_test, y_test)
    print(f"Test accuracy: {test_acc}")
    return test_acc

@pipeline
def digits_pipeline():
    X_train, X_test, y_train, y_test = importer()
    model = svc_trainer(X_train=X_train, y_train=y_train)
    evaluator(X_test=X_test, y_test=y_test, model=model)

# digits_svc_pipeline = digits_pipeline()


