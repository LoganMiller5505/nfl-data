import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("limited_models/qb_nn.h5")
print(model.summary())

# Run model inference on new data
import pandas as pd

hashmap = pd.read_csv("hashmap/hashmap.csv")

print("Loading Data")
raw_qb_data = pd.read_csv("nn_data/qb_nn.csv")
qb_data = raw_qb_data[raw_qb_data["2023"] == 1]

features = qb_data.drop(columns=["fantasy_points", "2023", "id"])
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
plt.scatter(results["Actual"], results["Predicted"])

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

plt.show()