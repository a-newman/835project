from sklearn.hmm import MultinomialHMM

class MMClassifier(Classifier): 
    """
    ABSTRACT CLASS serving as an interface for a classifier for use in the system 
    """
    def __init__(self, dset_name): 
        self.last_savepath = None
        self.dset_name = dset_name 

        self.mm = None
        self.gestures = None
        self.labels = None


    def prep(self): 
        """
        Do any pre-processing that needs to happen before it's ready to use
        Will be called on start-up. 
        """
        self._reload()

    def update(self, label, sample): 
        """
        Take in a new sample of someone (either teacher or student) performing the action
        Update/improve the model based on this example
        """
        raise NotImplementedError()

    def classify(self, sample): 
        """
        Given a sample, run the model on it and returns label of highest-scoring gesture
        """
        sample = np.hstack([f.frame for f in seq.frames])
        return self.mm.predict([sample])

    def train(self): 
        """
        Train the model
        """
        samples = [] 

        for label, g in cached_dset.gestures.items(): 
            for seq in g.sequences: 
                samples.append(np.hstack([f.frame for f in seq.frames]))

        self.mm.fit(samples)
        

    def _reload(self): 
        self.cached_dset = dset_ops._load_dset(self.dset_name)

        self.mm = MultinomialHMM(n_components=len(self.cached_dset.gestures)) #hidden states are equal to the # of gestures

        self.g_ids_to_names = {}
        self.g_id_count = 0

