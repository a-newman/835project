# Back-end/data processing readme 

This folder contains files dealing with saving, loading, and storing data collected by our application: that is, the gesture sequences recorded by the Kinect. 

This folder contains the following files and folders:
- `sets/`: a folder that contains the data itself. `sets/index.json` is an index of all datasets that are currently defined by mapping a dataset name to a file name. The rest of the files are data files, with one `.json` file per dataset containing a serialized version of the `DataSet` object representing that set. 
- `dset_ops.py`: helper functions to access the data stored in `sets/`. Names are fairly self-explanatory. 
- `Gesture.py`: data model for our data. We use `Gesture`, `Sequence`, and `Frame` objects very similar to those from MiniProject2, with some additional features; we also have a `DataSet` object that maps vocab terms to gestures and translations. 
