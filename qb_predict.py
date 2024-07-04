# Load QB model
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model("models/qb_nn.h5")
print(model.summary())