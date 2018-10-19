from __future__ import print_function
import os

import args


def get_darknet_lib(darknet_home):
    return os.path.join(darknet_home, "libdarknet.so")


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


def build_darknet(install):
    darknet_home = os.path.abspath('./darknet')
    if args.DARKNET_HOME in os.environ:
        temp_darknet_home = is_valid_darknet()
        if temp_darknet_home is None:
            return
        darknet_home, download = temp_darknet_home
    elif not os.path.exists(darknet_home):
        download = 1
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
    cmd = ['/bin/bash', os.path.abspath('./build_darknet.sh'), darknet_home, str(download), str(gpu), str(cudnn), str(opencv), str(openmp)]
    try:
        install.spawn(cmd)
    except:
        print('Building darknet was not successful from "%s".\nTry fixing the requirements\n'
              'If the darknet folder is outdated delete it manually and try again..' % darknet_home)
