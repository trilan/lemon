import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name = 'Lemon',
    version = '0.5.5',
    url = 'https://github.com/trilan/lemon',
    description = 'A collection of some must have Django apps',
    long_description = read('README.rst') + '\n\n' + read('HISTORY.rst'),
    author = 'TriLan Co.',
    author_email = 'lemon@trilandev.com',
    packages = find_packages(exclude=['test_project', 'test_project.*']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'django-intellipages',
    ],
    test_suite = 'tests.main',
)
