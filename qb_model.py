import pandas as pd
import matplotlib.pyplot as plt

print("Loading Data")

qb_nn_raw = pd.read_csv("nn_data/qb_nn.csv")
qb_nn_train = qb_nn_raw[qb_nn_raw["2023"] == 0]
qb_nn_val = qb_nn_raw[qb_nn_raw["2023"] == 1]

target = qb_nn_train["fantasy_points"]
target = target.fillna(0)
target = target.astype('float')
print(target.head())

features = qb_nn_train.drop(columns=["fantasy_points","2023","id"])
# Drop features with low coorelation values
# features = features.drop(columns=["opp_passing_yards_allowed","avg_time_to_throw","attempts","opp_rushing_tds_allowed","expected_completion_percentage","rushing_fumbles","avg_air_distance","opp_passing_tds_allowed","opp_rushing_yards_allowed","pacr","rushing_2pt_conversions","passing_2pt_conversions","opp_receiving_fumbles","avg_air_yards_differential","opp_sack_fumbles_recovered","opp_receiving_fumbles_recovered","opp_sack_fumbles","opp_special_teams_tds_allowed","opp_sacks","opp_sack_yards","sack_fumbles","sacks","opp_interceptions"])
features = features.fillna(0)
features = features.astype('float')
print(features.head())

qb_nn_val_results = qb_nn_val["fantasy_points"]
qb_nn_val = qb_nn_val.drop(columns=["fantasy_points","2023","id"])
# qb_nn_val = qb_nn_val.drop(columns=["opp_passing_yards_allowed","avg_time_to_throw","attempts","opp_rushing_tds_allowed","expected_completion_percentage","rushing_fumbles","avg_air_distance","opp_passing_tds_allowed","opp_rushing_yards_allowed","pacr","rushing_2pt_conversions","passing_2pt_conversions","opp_receiving_fumbles","avg_air_yards_differential","opp_sack_fumbles_recovered","opp_receiving_fumbles_recovered","opp_sack_fumbles","opp_special_teams_tds_allowed","opp_sacks","opp_sack_yards","sack_fumbles","sacks","opp_interceptions"])
qb_nn_val = qb_nn_val.fillna(0)
qb_nn_val = qb_nn_val.astype('float')
print(qb_nn_val.head())

# Try training on several different sklearn models and methods
import sklearn as sk
from sklearn.model_selection import train_test_split
X_train = features
X_test = qb_nn_val
y_train = target
y_test = qb_nn_val_results

from joblib import dump, load

from sklearn.ensemble import RandomForestRegressor
# MAE: 5.9327
from sklearn.metrics import mean_absolute_error

print("Training Random Forest Model")
model = RandomForestRegressor(n_estimators=500, random_state=0, verbose=1)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae}')

plt.scatter(y_test, predictions)
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
plt.show()
plt.savefig("limited_models/qb_rf.png")

dump(model, "limited_models/qb_rf.joblib")

from sklearn.linear_model import LinearRegression
# MAE: 5.8725
print("Training Linear Regression Model")
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae}')

plt.scatter(y_test, predictions)
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
plt.show()
plt.savefig("limited_models/qb_lr.png")

dump(model, "limited_models/qb_lr.joblib")

from sklearn.ensemble import GradientBoostingRegressor
# MAE: 5.975330
print("Training Gradient Boosting Model")
model = GradientBoostingRegressor(n_estimators=500, random_state=0, verbose=1)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae}')

plt.scatter(y_test, predictions)
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
plt.show()
plt.savefig("limited_models/qb_gb.png")

from sklearn.neural_network import MLPRegressor
# MAE: 5.8451
print("Training Neural Network Model")
model = MLPRegressor(hidden_layer_sizes=(1024,1024,1024), max_iter=700, verbose=True)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae}')

plt.scatter(y_test, predictions)
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
plt.show()
plt.savefig("limited_models/qb_nn.png")

dump(model, "limited_models/qb_nn.joblib")


'''import tensorflow as tf
from tensorflow.keras import layers

print("Version: " + tf.__version__)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

EPOCHS = 700
BATCH_SIZE = 32

model = tf.keras.Sequential()

model.add(layers.Dense(256, activation='relu', input_shape=[len(features.keys())]))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
# Run the model using qb_nn_val as validation data
history = model.fit(features, target, validation_data=(qb_nn_val, qb_nn_val_results), epochs=EPOCHS, batch_size=BATCH_SIZE)

loss, mae = model.evaluate(features, target)
print(f'Mean Absolute Error: {mae}')

model.save("limited_models/qb_nn.h5")

plt.plot(history.history['loss'], label='MAE (training data)')
plt.plot(history.history['val_loss'], label='MAE (validation data)')
plt.title('MAE for QB NN Model')
plt.ylabel('MAE value')
plt.xlabel('No. epoch')
plt.legend(loc="upper left")
plt.show()
plt.savefig("limited_models/qb_nn.png")'''