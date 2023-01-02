import keras
import numpy as np
import random
import matplotlib.pyplot as plt

data = np.load("synth_data_22_10000.npz")
X_data = data['X_data']
y_data = data["y_data"]

X_data = np.expand_dims(X_data, axis=-1)
X_data = X_data.astype('float')/255
n_classes = len(X_data)
print(X_data.shape)
X_data = np.concatenate(X_data, axis=0)
print(X_data.shape)
#y_data = np.array([d[0] for d in y_data])

print(y_data.shape)

print(y_data[:2])

# Thanks ChatGPT. Too lazy to think !
# Zip the lists together to create a list of tuples
zipped_lists = zip(X_data, y_data)

# Convert the list of tuples to a list of lists
zipped_lists = list(zipped_lists)

# Shuffle the list of lists
random.shuffle(zipped_lists)

# Unzip the shuffled list of lists back into two lists
X_data, y_data = zip(*zipped_lists)

X_data = np.array(X_data)
y_data = np.array(y_data)

plt.imshow(X_data[0], cmap='gray')
plt.show()

input_shape = (35, 50, 1)
num_classes = n_classes

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

print(model.summary())


model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

callbacks = [
    keras.callbacks.ModelCheckpoint("mymodel_temp_1_save.h5", save_best_only=True)
]

model.fit(X_data, y_data, batch_size=32, epochs=30,  validation_split=0.1, shuffle=True, callbacks=callbacks)

model.save('synth_model_22_10000.h5')
