from __future__ import print_function
import subprocess
import os

import args


def get_darknet_lib(darknet_home):
    return os.path.join(darknet_home, "libdarknet.so")


def create_build_file():
    body = '''#!/usr/bin/env bash

# arguments order
# darknet_home, download_again, GPU, CUDNN, OPENCV, OPENMP

mkdir /media/rog/disk11/do_not_delete/test_projects/pyyolo/filename

DARKNET_HOME=$1
DOWNLOAD_AGAIN=$2

command -v git >/dev/null 2>&1 || { echo >&2 "This requires git, but it's not installed.  Aborting.."; exit 1; }
command -v make >/dev/null 2>&1 || { echo >&2 "This requires make, but it's not installed.  Aborting.."; exit 1; }

mkdir -p ${DARKNET_HOME}
cd ${DARKNET_HOME}

if [ "${DOWNLOAD_AGAIN}" -eq "1" ]; then
    cd ..
    rm -rf darknet
    git clone https://github.com/pjreddie/darknet.git
    cd darknet
fi

sed -i "1s/.*/GPU=$3/" Makefile
sed -i "1s/.*/CUDNN=$4/" Makefile
sed -i "1s/.*/OPENCV=$5/" Makefile
sed -i "1s/.*/OPENMP=$6/" Makefile

make -j$(nproc)
    '''
    file_name = os.path.abspath('./build_darknet.sh')
    with open(file_name, 'w') as f:
        f.write(body)
    return file_name


def is_valid_darknet():
    darknet_home = os.environ[args.DARKNET_HOME]
    darknet_home = os.path.abspath(os.path.expanduser(darknet_home))
    if not os.path.isdir(darknet_home):
        print("Given darknet folder path is invalid")
        return darknet_home, 1
    elif os.path.exists(get_darknet_lib(darknet_home)):
        if args.REBUILD in os.environ and int(os.environ[args.REBUILD]) == 1:
            return darknet_home, 1
        return None
    else:
        return darknet_home, 0


def build_darknet():
    darknet_home = os.path.abspath('./darknet')
    if args.DARKNET_HOME in os.environ:
        temp_darknet_home = is_valid_darknet()
        if temp_darknet_home is None:
            return
        darknet_home, download = temp_darknet_home
    elif os.path.exists(get_darknet_lib(darknet_home)):
        if args.REBUILD not in os.environ:
            return
        download = 0
    else:
        download = 0

    gpu = 0
    cudnn = 0
    opencv = 0
    openmp = 0
    if args.GPU in os.environ:
        gpu = os.environ[args.GPU]
    if args.CUDNN in os.environ:
        cudnn = os.environ[args.CUDNN]
    if args.OPENCV in os.environ:
        opencv = os.environ[args.OPENCV]
    if args.OPENMP in os.environ:
        openmp = os.environ[args.OPENMP]

    print("Building Darknet...")
    cmd = ['/bin/bash', create_build_file(), darknet_home, str(download), str(gpu), str(cudnn), str(opencv), str(openmp)]
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    with open('/media/rog/disk11/do_not_delete/test_projects/pyyolo/file', 'w') as f:
        f.write('initial')
        f.write(str(cmd))
        f.write(str(os.path.isfile(cmd[1])))
        f.write(str(os.path.isfile('./thisisfile')))
        for line in iter(ret.stdout.readline, ''):
            if len(line) != 0:
                f.write(line.rstrip())
            else:
                break
    print("Here")

    if ret.wait() == 0:
        print("Building Darknet was Successful")
    else:
        raise ValueError('Building darknet was not successful from "%s".\nTry fixing the requirements\n'
                         'If the darknet folder is outdated delete it manually and try again..' % darknet_home)


