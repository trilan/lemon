from setuptools import setup, find_packages


setup(
    name = 'Lemon',
    version = '0.5.dev',
    url = 'http://lemoncmf.ru/',
    author = 'TriLan Co.',
    author_email = 'lemon@trilandev.com',
    description = 'A CMF based on Django.',
    packages = find_packages(exclude=['test_project', 'test_project.*']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'django-intellipages',
    ],
    test_suite = 'tests.main',
)
