from recognize.kmeans import Kmeans
import numpy as np
cluster = Kmeans('test')

print "cluster_map:",cluster.cluster_map
print "centers: ", cluster.cluster_map.cluster_centers_
print "labels: ", len(cluster.cluster_map.labels_),cluster.cluster_map.labels_
print "x_shape: ", np.array(cluster.X).shape
print "labels map:", cluster.label_map