import pandas as pd
import matplotlib.pyplot as plt

print("Loading Data")

qb_nn = pd.read_csv("nn_data/qb_nn.csv")
qb_nn = qb_nn[qb_nn["2023"] == 0]
print(qb_nn.head())

target = qb_nn["fantasy_points"]
target = target.fillna(0)
target = target.astype('float')
print(target.head())

features = qb_nn.drop(columns=["fantasy_points","2023","id"])
features = features.fillna(0)
features = features.astype('float')
print(features.head())

print("Loading Tensorflow")

import tensorflow as tf
from tensorflow.keras import layers

print("Version: " + tf.__version__)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

EPOCHS = 1000
BATCH_SIZE = 64

model = tf.keras.Sequential()

model.add(layers.Dense(1024, activation='relu', input_shape=[len(features.keys())]))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
history = model.fit(features, target, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2)

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
plt.savefig("limited_models/qb_nn.png")