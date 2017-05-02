from setuptools import setup
from setuptools import find_packages

setup(
    name='pytest-pact',
    version='0.1.0',
    author='Guido Barbaglia',
    author_email='guido.barbaglia@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Python implementation for Pact (http://pact.io/)',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    url='https://github.com/Kalimaha/pytest-pact/',
    entry_points = {
        'pytest11': [
            'pytest-pact = pact',
        ]
    }
)
