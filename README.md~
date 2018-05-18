# Louder than Words Documentation 

## Directory breakdown

This repo contains the following files and subfolders: 
- `data/`: contains the training/practice data collected during the running of the application, helpers for loading and accessing this data, and our data model used for interfacing with the data. See `data/README.md` for more details.
- `recognize/`: contains classifiers that we tried for gesture classification. See `recognize/README.md` for more details.
- `ui/`: code for running and displaying our ui. See `ui/README.md` for more details. 
- `misc/`: various helper files that we wrote for convenience or testing the system during the development process. 

## Loading a dataset 
Right now our UI does not provide the ability to add a new dataset, but from a code perspective this is easy to do. To create a clean dataset, edit the file `make_dset.py` so that the variable GESTURES contains a list of (word, translation) tuples that you want the system to use. Run this file to create and install the new dset. Run `python make_dset.py mubarik` to load in mubarik's dataset that we used for our demo. 

## Setup and dependencies

The following libraries/SDKs are required to run this system: 
- python 2 
- numpy 
- pygame 
- SpeechRecognition library (available via pip: https://pypi.org/project/SpeechRecognition/#description) with Google's speech recognition API back-end
- Windows 10 operating system 
- Visual Studio 2015 for C++
- Kinect SDK version 1.7.0
- PyKinect SDK for python (version 1): https://github.com/Microsoft/PTVS/tree/master/Python/Product/PyKinect 

### Instructions: 
- Install python and pip
- Install the official Kinect SDK and Visual Studio using installers on the Microsoft website
- Use pip to install numpy, pygame, pykinect, and the speech recognition library 
- run the system by running `main.py` 

