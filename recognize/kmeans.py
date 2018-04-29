from sklearn.cluster import KMeans
import numpy as np
from data import dset_ops
from classifier import Classifier
from normalize_frames import resize_seq
import pandas as pd 
class GestureMap:
  def __init__(self,X=[],label=1):
    self.label = label;
    self.data = X;

class Kmeans(Classifier):
  def __init__(self, dset_name, n_clusters=10):
    self.n_clusters = n_clusters;
    self.dset_name = dset_name
    self.cached_dset = dset_ops._load_dset(self.dset_name).gestures 
    self.gesture_set = []
    self.labels_array = []
    self.labels = []
    self.label_map = {}
    
    
    self.X = [];
    self.prep()
    
    self.cluster_map = self.train(clusters = self.n_clusters);
    self.label()
    df = pd.DataFrame(self.label_map);
    df.to_csv("recognize/cluster_results/"+dset_name+".csv");
    
    
  def prep(self): 
    """
    Do any pre-processing that needs to happen before it's ready to use
    Will be called on start-up. 
    """


    for word in self.cached_dset:
      print "word: ", word
      self.labels.append(word)
      d_frame = self.gesture_to_dataFrame(self.cached_dset[word],word=word)
      gesture_map = GestureMap(X=d_frame,label=word);
      self.gesture_set.append(gesture_map)


  def gesture_to_dataFrame(self,gesture,word=None):

    d_frame = [self.seq_to_array(seq,word=word) for seq in gesture.sequences]
  def seq_to_array(self,seq,word=None):
    self.labels_array.append(word)
    array = [frame.frame for frame in seq.normalize().frames]
    array = np.array(resize_seq(array,60)).flatten()
    #print "array: ", len(array)
    self.X.append(array);
    return array
  def frame_to_array(self,frame):
    data = []
    print "frame: ", frame.frame
    for point in frame.frame:
      data.extend(point)
    return data




  def train(self,clusters = 2): 
    """
    Train the model
    """
    print "shape of X:",np.array(self.X).shape
    return KMeans(n_clusters=clusters, random_state=0).fit(self.X)
  def classify(self, sample): 
    """
    Given a sample, run the model on it and returns label of highest-scoring gesture
    """
    self.kmeans.predict(sample)
  def label(self):
    '''
    Label the clusters according to the most common label
    '''
    for i in range(self.n_clusters):
      self.label_map[i]={}
      for _label in self.labels:
        self.label_map[i][_label]=0



    for i,clust in enumerate(self.cluster_map.labels_):
      self.label_map[clust][self.labels_array[i]]+=1
    



    

