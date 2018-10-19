from __future__ import print_function
import subprocess
import os

import args


def get_darknet_lib(darknet_home):
    return os.path.join(darknet_home, "libdarknet.so")


def get_darknet_wrap(darknet_home):
    return os.path.join(darknet_home, 'python/darknet.py')


def is_valid_darknet():
    darknet_home = os.environ[args.DARKNET_HOME]
    darknet_home = os.path.expanduser(darknet_home)
    if not os.path.isdir(darknet_home):
        print("Given darknet folder path is invalid")
        i = str(input("Do you want to download darknet (Y/n): "))
        if i.lower() == 'y':
            return darknet_home, 1
        else:
            raise ValueError("darknet folder given cannot be found. %s " % darknet_home)
    elif os.path.exists(get_darknet_lib(darknet_home)) and os.path.exists(get_darknet_wrap(darknet_home)):
        if args.REBUILD in os.environ and int(os.environ[args.REBUILD]) == 1:
            return darknet_home, 1
        return None
    elif not os.path.exists(get_darknet_wrap(darknet_home)):
        print("Given darknet version doesn't include python wrapper")
        i = str(input("Do you want to download darknet (Y/n): "))
        if i.lower() == 'y':
            return darknet_home, 1
        else:
            raise ValueError("Given darknet folder doesn't contail vaild wrapper. %s" % darknet_home)
    else:
        return darknet_home, 0


def build_darknet():
    darknet_home = './darknet'
    if args.DARKNET_HOME in os.environ:
        temp_darknet_home = is_valid_darknet()
        if temp_darknet_home is None:
            return
        darknet_home, download = temp_darknet_home
    elif os.path.exists(get_darknet_lib(darknet_home)) and os.path.exists(get_darknet_wrap(darknet_home)):
        if args.REBUILD not in os.environ:
            return
        download = 0
    elif not os.path.exists(get_darknet_wrap(darknet_home)):
        download = 1
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
    ret = subprocess.Popen(["bash", "build_darknet.sh", darknet_home, str(download), str(gpu), str(cudnn), str(opencv), str(openmp)],
                           shell=True, stdout=subprocess.PIPE)

    for line in iter(ret.stdout.readline, ''):
        if len(line) != 0:
            print(line.rstrip())
        else:
            break
    print("Here")

    if ret.wait() == 0:
        print("Building Darknet was Successful")
    else:
        raise ValueError('Building darknet was not successful from "%s".\nTry fixing the requirements\n'
                         'If the darknet folder is outdated delete it manually and try again..' % darknet_home)


