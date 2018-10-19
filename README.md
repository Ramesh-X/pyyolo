# pyyolo
A Python Wrapper for Yolo

## Requirements

This application is tested on Ubuntu 64bit environment. You will need `git` and `make` in order
to build this application.

```bash
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install git-core
```

Then you will need `numpy` and `opencv-python` packages as 3rd party python packages. 
You can build `OpenCV` from sources for `python` and `C++` and enable `OpenCV` while building
darknet (Recommended way).

Or you can install `OpenCV` directly from `pip`. Then you won't be able to build darknet with
`OpenCV`

```bash
pip install opencv-python
```

## Building and Installing

First you need to download and build darknet.

```bash
git clone https://github.com/Ramesh-X/pyyolo.git
cd pyyolo
python setup.py build_ext
```

This will download [darknet](http://pjreddie.com/darknet) from its original
[repository](https://github.com/pjreddie/darknet) and build the shared library.

You can pass the following additional options while you building the darknet sources.

```bash
# To provide custom darknet location
# If you did not provide this, darknet will be downloaded to current location
DARKNET_HOME=/home/user/darknet python setup.py build_ext

# To force rebuilding sources
REBUILD=1 python setup.py build_ext

# To enable OpenCV
OPENCV=1 python setup.py build_ext

# To enable GPU
GPU=1 python setup.py build_ext

# To enable OpenMP
OPENMP=1 python setup.py build_ext

# To enable cuDNN
CUDNN=1 python setup.py build_ext

# You can combine more than one option for building.
CUDNN=1 GPU=1 python setup.py build_ext
```

Then you can install the `pyyolo` to the system by:

```bash
pip install -U .
```

## Examples

Need to add examples and how to use guide


