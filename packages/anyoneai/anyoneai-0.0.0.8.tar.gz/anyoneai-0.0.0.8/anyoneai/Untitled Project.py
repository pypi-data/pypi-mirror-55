import tensorflow as tf
from tensorflow.keras.optimizers import Adam
model = tf.keras.models.Sequential([(tf.keras.layers.Dense(units=1, input_shape=[1]))])

model.compile(loss=("categorical_crossentropy"), optimizer=(Adam(lr=0.01)),metrics=["acc"])
os.popen("unzip ")
