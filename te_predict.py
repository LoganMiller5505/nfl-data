import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("models/te_nn.h5")
print(model.summary())