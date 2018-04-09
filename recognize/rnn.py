import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense, concatenate

from normalize_frames import normalize_frames
from load_gestures import load_gestures

USE_BIDIR = False

# 9. FORMAT DATA
gesture_sets = load_gestures()
gesture_sets = normalize_frames(gesture_sets, 36)

samples = []
labels = []

for gs in gesture_sets:
    for seq in gs.sequences:
        # a sample has num_frames rows and len(frame) columns  (basically a row for each frame)
        sample = np.vstack(list(map(lambda x: x.frame, seq.frames)))
        samples.append(sample)
        labels.append(gs.label)

X = np.array(samples) #X is then a list of samples. So X is num_samples x num_frames x len(frame)
print("X SHAPE", X.shape)
Y = np.vstack(labels) # Y is num_samples 
print("Y SHAPE", Y.shape)

# Shuffle data
p = np.random.permutation(len(X))
X = X[p]
Y = Y[p]

# 10. CREATE AND TRAIN MODEL
batch_size = 12
epochs = 100
latent_dim = 16

input_layer = Input(shape=(X.shape[1:]))
lstm = LSTM(latent_dim)(input_layer)
lstm_reversed = LSTM(latent_dim, go_backwards=True)(input_layer)
bidir = concatenate([lstm, lstm_reversed])

if USE_BIDIR: 
    dense = Dense(latent_dim, activation='relu')(bidir)
else: 
    dense = Dense(latent_dim, activation='relu')(lstm)
pred = Dense(len(gesture_sets), activation='softmax')(dense)

model = Model(inputs=input_layer, outputs=pred)
model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=["acc"])

model.fit(X,
          Y,
          epochs=epochs,
          batch_size=batch_size,
          verbose=1,
          validation_split=0.3,
          shuffle=True)

# Code to test different parameters 
# for latent_dim in range(8, 25, 8): 
#     epochs=400
#     input_layer = Input(shape=(X.shape[1:]))
#     lstm = LSTM(latent_dim)(input_layer)
#     lstm_reversed = LSTM(latent_dim, go_backwards=True)(input_layer)
#     # concat the two lstm outputs
#     bidir = concatenate([lstm, lstm_reversed])
#     #dense = Dense(latent_dim, activation='relu')(bidir)
#     dense = Dense(latent_dim, activation='relu')(lstm)
#     pred = Dense(len(gesture_sets), activation='softmax')(dense)
#     model = Model(inputs=input_layer, outputs=pred)
#     model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=["acc"])
#     for batch_size in range(8, 25, 8): 
#         print("Running with latent_dim: %d, batch_size: %d" % (latent_dim, batch_size))
#         history = model.fit(X,
#                   Y,
#                   epochs=epochs,
#                   batch_size=batch_size,
#                   verbose=0,
#                   validation_split=0.3,
#                   shuffle=True)
#         # try to print the accuracy
#         for ep in range(40, 401, 50): 
#             loss = history.history["loss"][ep]
#             val_loss = history.history["val_loss"][ep]
#             val_acc = history.history["val_acc"][ep]
#             acc = history.history["acc"][ep]
#             print("EPOCH %d" % ep)
#             print("\tLoss: %f, Val Loss: %f" % (loss, val_loss))
#             print("\tAcc: %f, Val Acc: %f" % (acc, val_acc))
