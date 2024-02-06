import tensorflow as tf
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.optimizers import SGD
import matplotlib.pyplot as plt

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Display a sample image
plt.imshow(x_train[0])

# Input image row and column
input_img_row = x_train[0].shape[0]
input_img_cols = x_train[0].shape[1]

x_train = x_train.reshape(x_train.shape[0], input_img_row, input_img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], input_img_row, input_img_cols, 1)

input_shape = (input_img_row, input_img_cols, 1)

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# One-hot encode the labels
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

num_classes = y_train.shape[1]
num_pixels = x_train.shape[1] * x_train.shape[2]

model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3, 3), activation="relu", input_shape=input_shape))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(units=128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(units=num_classes, activation="softmax"))

model.compile(optimizer=SGD(0.01), loss="categorical_crossentropy", metrics=["accuracy"])

model.summary()

history = model.fit(
    x=x_train,
    y=y_train,
    batch_size=35,
    epochs=10,
    verbose=1,
    validation_data=(x_test, y_test)
)

test_score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', test_score[0])
print('Test accuracy:', test_score[1])

model_path = input('Enter a file path (with .h5 extension) to save the model:')
model.save(model_path)

loaded_model = load_model(model_path)

loaded_score = loaded_model.evaluate(x_test, y_test, verbose=0)
print("Test loss (loaded model):", loaded_score[0])
print("Test accuracy (loaded model):", loaded_score[1])
print('Code execution completed successfully!')
