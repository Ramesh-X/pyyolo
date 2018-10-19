from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

from build_darknet import build_darknet
from pyyolo import __version__


def configure():
    print "This is what hepps"


class YoloBuildExt(build_ext):
    def run(self):
        build_darknet()
        build_ext.run(self)


class YoloInstall(install):
    def run(self):
        install.run(self)
        configure()


setup(
    name='pyyolo',
    version=__version__,
    description='Python Wrapper for YOLO',
    url='https://github.com/Ramesh-X/pyyolo',
    author='Ramesh Rathnayake',
    author_email='rsoft.ramesh@gmail.com',
    license='Proprietary',
    cmdclass={
        'install': YoloInstall,
        'build_ext': YoloBuildExt
    },
    packages=['pyyolo'],
    zip_safe=False,
    install_requires=['numpy>=1.14.3']
)
