# Classification docs 

This folder contains files dealing with training classifiers and predicting gestures. 

This folder contains the following files and folders:
- `classifier.py`: an abstract base class from which our classifiers inherit, which allows us to easily swap them out and test them 
- `normalize_frames.py`: helper for downsampling sequences, from MiniProject2
- `nn_classifier.py`: a nearest neighbor classifier, which is what we used in our final project. 
- `net_classifier.py`: a neural net classifier implemented in Keras
- `decision_tree.py`: a decision-tree based classifier. 
- `kmeans.py`: a k-means classifier 
