import pandas as pd
import matplotlib.pyplot as plt

print("Loading Data")

te_nn_raw = pd.read_csv("nn_data/te_nn.csv")
#te_nn_train = te_nn_raw[te_nn_raw["2023"] == 0]
te_nn_train = te_nn_raw
te_nn_val = te_nn_raw[te_nn_raw["2023"] == 1]

target = te_nn_train["fantasy_points_ppr"]
target = target.fillna(0)
target = target.astype('float')
print(target.head())

features = te_nn_train.drop(columns=["fantasy_points_ppr","2023","id","display_name"])
features = features.fillna(0)
features = features.astype('float')
print(features.head())

te_nn_val_results = te_nn_val["fantasy_points_ppr"]
te_nn_val = te_nn_val.drop(columns=["fantasy_points_ppr","2023","id","display_name"])
te_nn_val = te_nn_val.fillna(0)
te_nn_val = te_nn_val.astype('float')
print(te_nn_val.head())

# Try training on several different sklearn models and methods
import sklearn as sk
from sklearn.model_selection import GridSearchCV, train_test_split
X_train = features
X_test = te_nn_val
y_train = target
y_test = te_nn_val_results

from joblib import dump, load

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

print("Training Random Forest Model")

model = RandomForestRegressor(n_estimators=1000, verbose=2)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae}')

plt.scatter(y_test, predictions)
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("TE NN Model Predictions")
# Graph green line that represents perfect prediction (within 2 points)
plt.plot([0, 50], [2, 52], color="green", linestyle="--")
plt.plot([0, 50], [-2, 48], color="green", linestyle="--")
# Graph yellow lines that bound a difference of 5 between actual and predicted
plt.plot([0, 50], [5, 55], color="yellow", linestyle="--")
plt.plot([0, 50], [-5, 45], color="yellow", linestyle="--")
# Graph red lines that bound a difference of 10 between actual and predicted
plt.plot([0, 50], [10, 60], color="red", linestyle="--")
plt.plot([0, 50], [-10, 40], color="red", linestyle="--")
# Count how many predictions are within 2, 5, and 10 points, as well as outside of 10 points
plt.show()
plt.savefig("limited_models/te_rf.png")

dump(model, "limited_models/te_rf.joblib")