from sklearn.datasets import _california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, mean_absolute_error, r2_score, root_mean_squared_error
import pandas as pd
import numpy as np
from time import time
from datetime import datetime
import matplotlib.pyplot as plt


# retrive the California housing dataset
data = _california_housing.fetch_california_housing()

# retrive the California housing dataset as a pandas DataFrame
df = _california_housing.fetch_california_housing(as_frame=True)

#split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42)

# create a random forest regressor model
estimators = [1, 10, 100, 1000, 10000]
metrics = {"mse": [], "rmse":[], "mae": [], "r2": [], "estimator": [], "time": []}
for estimator in estimators:
    print(f"Evaluating Random Forest Regressor with {estimator} estimators:")
    
    time_start = datetime.now()
    print(f"Start time: {time_start}")

    # create a random forest regressor model with the specified number of estimators
    model = RandomForestRegressor(n_estimators=estimator, random_state=17)

    # fit the model to the training data
    model.fit(X_train, y_train)

    # make predictions on the test data
    y_pred = model.predict(X_test)  

    # evaluate the model using mean squared error
    mse = mean_squared_error(y_test, y_pred)
    metrics["mse"].append(mse)
    print(f"Mean Squared Error: {mse}")

    # evaluate the model using mean squared error
    rmse = root_mean_squared_error(y_test, y_pred)
    metrics["rmse"].append(rmse)
    print(f"Root Mean Squared Error: {rmse}")

    # evaluate the model using mean absolute error
    mae = mean_absolute_error(y_test, y_pred)
    metrics["mae"].append(mae)
    print(f"Mean Absolute Error: {mae}")

    # evaluate the model using r-squared score
    r2 = r2_score(y_test, y_pred)
    metrics["r2"].append(r2)
    print(f"R-squared Score: {r2}")
    print("time taken: ", datetime.now() - time_start)
    print("\n")

    metrics["time"].append(datetime.now() - time_start)
    metrics["estimator"].append(np.log10(estimator))

    # print(metrics.items())
    # print(estimator)
    # for x in metrics.items():
    #     print(x[0])
    #     print(x[1][0])
    # print(metrics.items()[0][1][0])
    # print(metrics["estimator"])
    # print(metrics["mse"])

fig, ax = plt.subplots()

ax.plot(metrics["estimator"], metrics["mse"], label=f'MSE')
ax.plot(metrics["estimator"], metrics["mae"], label=f'MAE')  
ax.plot(metrics["estimator"], metrics["r2"], label=f'R-squared')
ax.plot(metrics["estimator"], metrics["rmse"], label=f'RMSE')
    # ax.plot(metrics["estimator"], metrics["time"], label=f'Time - {estimator} Estimators') 

ax.set_title('Random Forest Regressor Metrics')
ax.set_xlabel('Number of Estimators')
ax.set_ylabel('Metric Value')
ax.legend()
plt.show()
    # ax.plot(y_test, label='Actual', color='blue')
    # ax.plot(y_pred, label='Predicted', color='orange')
    # ax.set_title(f'Random Forest Regressor with {estimator} Estimators')
    # ax.set_xlabel('Sample Index')
    # ax.set_ylabel('Target Value')
    # ax.legend()
    # plt.show()

# evaluate the model using accuracy score
# accuracy_score = accuracy_score(y_test, y_pred)
# print(f"Accuracy Score: {accuracy_score}")

def visualise_metrics(model, X_test, y_test):
    pass

def importance(model, data):
    """
    Evaluate the importance of each feature in the model.  
    """
    # evaluate the importance of each feature
    importances = model.feature_importances_
    d_list = []
    for i in range(len(importances)):
        d_list.append((data.feature_names[i], importances[i]))
    sumt = sum([x[1] for x in d_list])
    print(f"Sum of importances: {sumt}")
    print(d_list)
    n_list = []
    for j in d_list:
        n_list.append(j[1])
    print(n_list)
    n_list.sort(reverse=True)
    print(n_list)
    d_dict = {}
    for k in n_list:
        for l in d_list:
            if k in l:
                d_dict[l[0]] = l[1]
    print(d_dict)
    # print(importances)
    # importances.sort(reverse=True)
    # print(importances)
    # print(type(importances))
    # print("Feature Importances:")
    # for i, feature in enumerate(data.feature_names):
    #     print(f"{feature}: {importances[i]}")

# print the information of the data in dataframes
def understand_data(data_as_frame):
    for i in list(df.keys()):
        print(f"{i}------------------------")
        print(df[i])
    if type(df[i]) == pd.DataFrame or type(df[i]) == pd.Series:
        print(df[i].info())
    else:
        print("Not a DataFrame")

def create_model():
    # weight of the model
    weight = None
    # bias of the model
    bias = None
    # learning rate of the model
    leanrning_rate = 0.01


if __name__ == "__main__":
    understand_data(data)
    pass
