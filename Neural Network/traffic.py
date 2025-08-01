import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    for cat in range(NUM_CATEGORIES):
        cat_folder = os.path.join(data_dir, str(cat))

        if not os.path.isdir(cat_folder):
            continue
        # read every picture in the folder
        for pic_name in os.listdir(cat_folder):
            pic_path = os.path.join(cat_folder, pic_name)
            pic = cv2.imread(pic_path)
        # error handing for invalid pictures
            if pic is None:
                continue
        # resize pic and add pic and labels to list
            pic_small = cv2.resize(pic, (IMG_WIDTH, IMG_HEIGHT))
            images.append(pic_small)
            labels.append(cat)

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # first conv layer
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(8, (5, 5), activation="relu",
              input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # second conv layers
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu",
              input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu",
              input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # flatten to connect layers
    model.add(tf.keras.layers.Flatten())

    # fully connected layers
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    # compile it
    model.compile(optimizer="adam",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])

    return model


if __name__ == "__main__":
    main()
