"""_____________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 python3 communication library setup*

:details: SiLA2 python3 libray setup. This installs the SiLA2 Python3 commuincation library.

:authors: mark doerr (mark@uni-greifswald.de)

:date: (creation)    2019-11-06

.. todo:: - testing !!
________________________________________________________________________
"""

__version__ = "0.2.0"

from typing import List
import os

from setuptools import setup, find_packages

package_name = 'sila2comlib'

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
        return file.read()

def generate_package_data(input_path: str, ending: str = '') -> List[str]:
    paths = []
    for (path, _, files) in os.walk(input_path):
        paths.extend([os.path.join('..', path, file) for file in files if file.endswith(ending)])

    return paths

setup(
    name=package_name,
    version=__version__,
    description='sila2comlib - a SiLA 2 python3 communication library ',
    long_description=read('README.rst'),
    author=', '.join([
        'Mark Doerr'
    ]),
    author_email='mark.doerr@uni-greifswald.de',
    keywords=('SiLA 2, lab automation, laboratory, instruments,'
              'experiments, evaluation, visualisation, serial interface, robots'),
    url='https://gitlab.com/SiLA2/sila_python',
    license='MIT',
    packages=find_packages(),
    install_requires=["pyserial"],
    test_suite='',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Utilities',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                 'Topic :: Scientific/Engineering :: Information Analysis'],
    include_package_data=False, #True,
    #package_data={  #package_name:  },
    setup_requires=['wheel']
)
