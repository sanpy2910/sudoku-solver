import tensorflow as tf
from keras.models import load_model
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np
import random

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Display a sample image
plt.imshow(x_test[0])

input_img_rows = x_train[0].shape[0]
input_img_cols = x_train[0].shape[1]

# Reshape and normalize the test data
x_test = x_test.reshape(x_test.shape[0], input_img_rows, input_img_cols, 1)
x_test = x_test.astype("float32") / 255

# One-hot encode the labels
y_test = to_categorical(y_test)

# Load the pre-trained model
model_path = input('Enter the file path (with .h5 extension) containing the saved model:')
loaded_model = load_model(model_path)

# Make predictions on the test data
predictions = loaded_model.predict([x_test])

# Evaluate the model's effectiveness
while True:
    # Select a random index
    index = random.randint(0, 10000)

    # Display the predicted number
    print('Prediction:', np.argmax(predictions[index]))

    # Display the corresponding image
    plt.imshow(x_test[index], cmap="gray")

    # Show the image
    plt.show()
