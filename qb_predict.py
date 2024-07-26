import tensorflow as tf
from tensorflow.keras.models import load_model

from joblib import dump, load

import pandas as pd

from sklearn.linear_model import LinearRegression

# Load the model
model = load("limited_models/qb_lr.joblib")

# Load the data
qb_nn = pd.read_csv("nn_data/qb_nn.csv")
qb_nn = qb_nn[qb_nn["2023"] == 1]

# Drop the columns that are not needed
features = qb_nn.drop(columns=["fantasy_points", "2023", "id"])
features = features.fillna(0)

target = qb_nn["fantasy_points"]

# Run the model on the data
predictions = model.predict(features)

# Combine Predictions and Actual into a DataFrame
results = pd.DataFrame()

results["Player"] = qb_nn["id"]

results["Actual"] = target
results["Predicted"] = predictions


results["Difference"] = results["Actual"] - results["Predicted"]
results["Difference"] = results["Difference"].abs()
results["Difference"] = results["Difference"].round(2)
print(results)
print(f"Mean Absolute Error: {results['Difference'].mean()}")
print(f"Mean Squared Error: {results['Difference'].pow(2).mean()}")
print(f"Root Mean Squared Error: {results['Difference'].pow(2).mean() ** 0.5}")

# Create a plot of the results
import matplotlib.pyplot as plt

# Take random distribution of points to plot
plt.scatter(results["Actual"], results["Predicted"], color="blue")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("QB LR Model Predictions")
# Graph green line that represents perfect prediction (within 2 points)
plt.plot([0, 40], [2, 42], color="green", linestyle="--")
plt.plot([0, 40], [-2, 38], color="green", linestyle="--")
# Graph yellow lines that bound a difference of 5 between actual and predicted
plt.plot([0, 40], [5, 45], color="yellow", linestyle="--")
plt.plot([0, 40], [-5, 35], color="yellow", linestyle="--")
# Graph red lines that bound a difference of 10 between actual and predicted
plt.plot([0, 40], [10, 50], color="red", linestyle="--")
plt.plot([0, 40], [-10, 30], color="red", linestyle="--")
plt.show()
# Count how many predictions are within 2, 5, and 10 points, as well as outside of 10 points
print("Within 2: ", len(results[results["Difference"] <= 2]), "out of", len(results))
print("Within 2 and 5: ", len(results[results["Difference"] <= 5]) - len(results[results["Difference"] <= 2]), "out of", len(results))
print("Within 5 and 10: ", len(results[results["Difference"] <= 10]) - len(results[results["Difference"] <= 5]), "out of", len(results))
print("Outside 10: ", len(results[results["Difference"] > 10]), "out of", len(results))
print("Outside 15: ", len(results[results["Difference"] > 15]), "out of", len(results))
print("Outside 20: ", len(results[results["Difference"] > 20]), "out of", len(results))


'''model = load_model("limited_models/qb_nn.h5")
print(model.summary())

# Run model inference on new data
import pandas as pd

hashmap = pd.read_csv("hashmap/hashmap.csv")

print("Loading Data")
raw_qb_data = pd.read_csv("nn_data/qb_nn.csv")
qb_data = raw_qb_data[raw_qb_data["2023"] == 1]

features = qb_data.drop(columns=["fantasy_points", "2023", "id"])
features = features.drop(columns=["opp_passing_yards_allowed","avg_time_to_throw","attempts","opp_rushing_tds_allowed","expected_completion_percentage","rushing_fumbles","avg_air_distance","opp_passing_tds_allowed","opp_rushing_yards_allowed","pacr","rushing_2pt_conversions","passing_2pt_conversions","opp_receiving_fumbles","avg_air_yards_differential","opp_sack_fumbles_recovered","opp_receiving_fumbles_recovered","opp_sack_fumbles","opp_special_teams_tds_allowed","opp_sacks","opp_sack_yards","sack_fumbles","sacks","opp_interceptions"])
features = features.fillna(0)

target = qb_data["fantasy_points"]

print("Running Inference")
predictions = model.predict(features)
print(predictions)

# Combine Predictions and Actual into a DataFrame
results = pd.DataFrame()

# results["Player"] = qb_data["id"] passed through hashmap
results["Player"] = qb_data["id"].map(hashmap.set_index("id")["name"])

results["Actual"] = target
results["Predicted"] = predictions
results["Difference"] = results["Actual"] - results["Predicted"]
results["Difference"] = results["Difference"].abs()
results["Difference"] = results["Difference"].round(2)
print(results)
print(f"Mean Absolute Error: {results['Difference'].mean()}")

# Create a plot of the results
import matplotlib.pyplot as plt

# Take random distribution of points to plot
#plt.scatter(results["Actual"], results["Predicted"])
plt.scatter(results["Actual"], results["Predicted"], color="blue")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("QB NN Model Predictions")
# Graph green line that represents perfect prediction (within 2 points)
plt.plot([0, 40], [2, 42], color="green", linestyle="--")
plt.plot([0, 40], [-2, 38], color="green", linestyle="--")
# Graph yellow lines that bound a difference of 5 between actual and predicted
plt.plot([0, 40], [5, 45], color="yellow", linestyle="--")
plt.plot([0, 40], [-5, 35], color="yellow", linestyle="--")
# Graph red lines that bound a difference of 10 between actual and predicted
plt.plot([0, 40], [10, 50], color="red", linestyle="--")
plt.plot([0, 40], [-10, 30], color="red", linestyle="--")
# Count how many predictions are within 2, 5, and 10 points, as well as outside of 10 points
print("Within 2: ", len(results[results["Difference"] <= 2]), "out of", len(results))
print("Within 2 and 5: ", len(results[results["Difference"] <= 5]) - len(results[results["Difference"] <= 2]), "out of", len(results))
print("Within 5 and 10: ", len(results[results["Difference"] <= 10]) - len(results[results["Difference"] <= 5]), "out of", len(results))
print("Outside 10: ", len(results[results["Difference"] > 10]), "out of", len(results))
print("Outside 15: ", len(results[results["Difference"] > 15]), "out of", len(results))
print("Outside 20: ", len(results[results["Difference"] > 20]), "out of", len(results))

plt.show()'''