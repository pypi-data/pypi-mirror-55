"""
Netmath
-------

A native python library for doing network/subnetting math.
"""
from distutils.util import convert_path
from setuptools import setup, find_packages
from unittest import TestLoader


def get_test_suite():
    test_loader = TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


main_ns = {}
ver_path = convert_path('netmath/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="netmath",
    version=main_ns['__VERSION__'],
    description="Netmath",
    long_description=__doc__,
    keywords="network library",

    author="Matthew Pounsett",
    author_email="matt@conundrum.com",
    license="Apache Software License 2.0",
    url="https://github.com/mpounsett/netmath",
    download_url="https://pypi.org/project/netmath/",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking',
    ],

    test_suite='setup.get_test_suite',
    packages=find_packages(),
)
