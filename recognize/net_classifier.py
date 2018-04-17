import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense, concatenate

from recognize.classifier import Classifier
from recognize.normalize_frames import resize_seq
from data import dset_ops

class NetClassifier(Classifier): 
    """
    ABSTRACT CLASS serving as an interface for a classifier for use in the system 
    """
    def __init__(self, dset_name, num_frames=30, batch_size=12, epochs=100, latent_dim=16): 
        super().__init__()
        self.last_savepath = None
        self.dset_name = dset_name
        self.num_frames = num_frames

        self.g_id_count = 0
        self.g_ids_to_names = {} 
        self.X = None
        self.Y = None
        self.model = None

        # model params 
        self.batch_size = batch_size
        self.epochs = epochs
        self.latent_dim = latent_dim

    def prep(self): 
        """
        Do any pre-processing that needs to happen before it's ready to use
        Will be called on start-up. 
        """
        self._reload()
        self._make_model()

    def update(self, label, sample): 
        """
        Take in a new sample of someone (either teacher or student) performing the action
        Update/improve the model based on this example
        """
        raise NotImplementedError()

    def classify(self, seq): 
        """
        Given a sample, run the model on it and returns label of highest-scoring gesture
        """
        print("seq", seq)
        frames = resize_seq(seq.frames, self.num_frames)
        sample = np.array([np.vstack(list(map(lambda x: x.frame, frames)))])
        print("sample shape", sample.shape)
        print("X shape", self.X.shape)
        print("Y shape", self.Y.shape)

        probs = self.model.predict(sample)[0]
        prediction_id = np.argmax(probs)
        print("prediction id", prediction_id)
        return self.g_ids_to_names[prediction_id]

    def train(self): 
        """
        Train the model
        """
        self.model.fit(
          self.X,
          self.Y,
          epochs=self.epochs,
          batch_size=self.batch_size,
          verbose=1,
          validation_split=0.0, # train on all available data 
          shuffle=True
        )

    def _get_new_gid(self): 
        self.g_id_count += 1
        return self.g_id_count - 1 

    def _reload(self): 
        self.cached_dset = dset_ops._load_dset(self.dset_name)

        samples, labels = [], []
        self.g_ids_to_names = {}
        self.g_id_count = 0 

        for g_name, g in self.cached_dset.gestures.items(): 
            g_id = self._get_new_gid()
            self.g_ids_to_names[g_id] = g_name 

            for seq in g.sequences: 
                frames = resize_seq(seq.frames, self.num_frames)
                sample = np.vstack(list(map(lambda x: x.frame, frames)))
                samples.append(sample)
                labels.append(g_id)

        self.X = np.array(samples) 
        self.Y = np.vstack(labels) 

    def _make_model(self): 
        input_layer = Input(shape=(self.X.shape[1:]))
        lstm = LSTM(self.latent_dim)(input_layer)
        lstm_reversed = LSTM(self.latent_dim, go_backwards=True)(input_layer)
        bidir = concatenate([lstm, lstm_reversed])

        dense = Dense(self.latent_dim, activation='relu')(bidir)
        pred = Dense(len(self.cached_dset.gestures), activation='softmax')(dense)

        self.model = Model(inputs=input_layer, outputs=pred)
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=["acc"])

