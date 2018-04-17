import pickle

class Classifier(object): 
	"""
	ABSTRACT CLASS serving as an interface for a classifier for use in the system 
	"""
	def __init__(self): 
		super().__init__()
		self.last_savepath = None

	def prep(self): 
		"""
		Do any pre-processing that needs to happen before it's ready to use
		Will be called on start-up. 
		"""
		raise NotImplementedError()

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
		raise NotImplementedError()

	def train(self): 
		"""
		Train the model
		"""
		raise NotImplementedError()

	def save(self, savepath=None): 
		"""
			Save it
		"""
		sp = None
		if (savepath): 
			sp = savepath
		elif self.last_savepath: 
			sp = self.last_savepath
		else: 
			raise RuntimeError("No save path provided")

		with open(sp, 'wb') as outfile: 
			pickle.dump(self, outfile)