import pandas as pd
import matplotlib.pyplot as plt

print("Loading Data")

wr_nn = pd.read_csv("limited_nn_data/wr_nn.csv")

target = wr_nn["fantasy_points_ppr"]
target = target.fillna(0)
target = target.astype('float')
target

features = wr_nn.drop(columns=["fantasy_points_ppr"])
features = features.fillna(0)
features = features.astype('float')
features

print("Loading Tensorflow")

import tensorflow as tf
from tensorflow.keras import layers

EPOCHS = 1000
BATCH_SIZE = 128


model = tf.keras.Sequential([
    layers.Dense(512, activation='relu', input_shape=(features.shape[1],)),
    layers.Dense(512, activation='relu', input_shape=(features.shape[1],)),
    layers.Dense(512, activation='relu', input_shape=(features.shape[1],)),
    layers.Dense(512, activation='relu', input_shape=(features.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
history = model.fit(features, target, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.35)

loss, mae = model.evaluate(features, target)
print(f'Mean Absolute Error: {mae}')

model.save("limited_models/wr_nn.h5")

plt.plot(history.history['loss'], label='MAE (training data)')
plt.plot(history.history['val_loss'], label='MAE (validation data)')
plt.title('MAE for WR NN Model')
plt.ylabel('MAE value')
plt.xlabel('No. epoch')
plt.legend(loc="upper left")
plt.show()
plt.savefig("limited_models/wr_nn.png")