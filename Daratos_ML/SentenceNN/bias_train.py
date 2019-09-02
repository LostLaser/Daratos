from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras import optimizers
from keras import callbacks
from keras import layers
from datetime import datetime
import read

#####################
# Load data from csvs
top_words = 15000
(X_train, y_train), (X_test, y_test), top_words = read.load_data()

max_words = 50
X_train = sequence.pad_sequences(X_train, maxlen=max_words)
X_test = sequence.pad_sequences(X_test, maxlen=max_words)
print(X_train[0])
#Setting up tensorboard
logdir="logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = callbacks.TensorBoard(log_dir=logdir)

# create the model
model = Sequential()
model.add(Embedding(top_words, 32, input_length=max_words))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))
optim = optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)
model.compile(loss='categorical_crossentropy', optimizer=optim, metrics=['accuracy'])
print(model.summary())

# Fit the model
model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test), 
        epochs=15, 
        batch_size=16, 
        verbose=1,
        callbacks=[tensorboard_callback],
        validation_split=0.1)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)

print("Accuracy: %.2f%%" % (scores[1]*100))

model.save('sentenceModel.h5')