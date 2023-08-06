import os
from distutils.core import setup

from setuptools import find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


def copy_dir():
    dir_path = 'policies'
    base_dir = os.path.join('rex_gym', dir_path)
    for (dirpath, dirnames, files) in os.walk(base_dir):
        for f in files:
            yield os.path.join(dirpath.split('/', 1)[1], f)

setup(
    name='rex_gym',
    version='0.1',
    license='Apache 2.0',
    packages=find_packages(),
    author='Nicola Russo',
    author_email='dott.nicolarusso@gmail.com',
    url='https://github.com/nicrusso7/rex-gym',
    download_url='https://github.com/nicrusso7/rex-gym/archive/v_01.tar.gz',
    install_requires=requirements,
    package_data={
        '': [f for f in copy_dir()]
    },
    keywords=['openai', 'gym', 'robot', 'quadruped', 'pybullet', 'ai', 'reinforcement', 'learning', 'machine', 'RL',
              'ML', 'tensorflow', 'spotmicro', 'rex'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7']
)
