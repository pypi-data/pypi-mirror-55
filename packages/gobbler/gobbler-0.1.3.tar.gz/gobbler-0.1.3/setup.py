from setuptools import setup
import os

VERSION = '0.1.3'

datadir = os.path.join('gobble', 'assets')
datafiles = [(d, [os.path.join(d, f) for f in files])
             for d, folders, files in os.walk(datadir)]

setup(
    name='gobbler', version=VERSION, packages=['gobble'], data_files=datafiles,
    url='https://github.com/rayssharma/gobble',
    download_url='https://github.com/rayssharma/gobble/tarball/{}'.format(
        VERSION), license='MIT', author='Ray Sharma',
    author_email='ramon.sharma1@gmail.com',
    description='Turkey-themed image catalog to boost the holiday mood.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['pillow>=6.2.1', 'pytest'], entry_points={
        'console_scripts': ['gobble=gobble.gobble:main'],
    }, classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ])
