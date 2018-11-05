from setuptools import setup
from distutils.command.build_ext import build_ext
from build_darknet import build_darknet

exec(open('./pyyolo/version.py').read())


class YoloBuildExt(build_ext):
    def run(self):
        build_darknet(self)
        build_ext.run(self)


setup(
    name='pyyolo',
    version=__version__,
    description='Python Wrapper for YOLO',
    url='https://github.com/Ramesh-X/pyyolo',
    author='Ramesh Rathnayake',
    author_email='rsoft.ramesh@gmail.com',
    license='Proprietary',
    cmdclass={
        'build_ext': YoloBuildExt,
    },
    packages=['pyyolo'],
    data_files=[('', ['pyyolo/libdarknet.so'])],
    include_package_data=True,
    zip_safe=False,
    install_requires=['numpy>=1.14.3', 'typing']
)
