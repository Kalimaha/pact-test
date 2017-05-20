from setuptools import setup
from setuptools import find_packages

setup(
    name='pact-test',
    version='0.1.0',
    author='Guido Barbaglia',
    author_email='guido.barbaglia@gmail.com',
    packages=find_packages(),
    license='LICENSE',
    long_description=open('README.rst').read(),
    description='Python implementation for Pact (http://pact.io/)',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3.0', 'pytest-pep8', 'pytest-sugar', 'pytest-mock'],
    url='https://github.com/Kalimaha/pact-test/'
)
