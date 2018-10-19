from setuptools import setup
from setuptools.command.install import install

from build_darknet import build_darknet
from pyyolo import __version__


def configure():
    print "This is what hepps"


class YoloInstall(install):
    def run(self):
        install.run(self)
        build_darknet()
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
    },
    packages=['pyyolo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['numpy>=1.14.3']
)
