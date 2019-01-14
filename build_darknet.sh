#!/usr/bin/env bash

# arguments order
# darknet_home, download_again, GPU, CUDNN, OPENCV, OPENMP

DARKNET_HOME=$1
DOWNLOAD_AGAIN=$2
HERE=`pwd -P`

command -v git >/dev/null 2>&1 || { echo >&2 "This requires git, but it's not installed.  Aborting.."; exit 1; }
command -v make >/dev/null 2>&1 || { echo >&2 "This requires make, but it's not installed.  Aborting.."; exit 1; }

mkdir -p "${DARKNET_HOME}"
cd "${DARKNET_HOME}"

if [ "${DOWNLOAD_AGAIN}" -eq "1" ]; then
    cd ..
    rm -rf darknet
    git clone https://github.com/pjreddie/darknet.git
    cd darknet
fi

sed -i "1s/.*/GPU=$3/" Makefile
sed -i "2s/.*/CUDNN=$4/" Makefile
sed -i "3s/.*/OPENCV=$5/" Makefile
sed -i "4s/.*/OPENMP=$6/" Makefile

make -j$(nproc)
cp libdarknet.so "${HERE}/pyyolo"



