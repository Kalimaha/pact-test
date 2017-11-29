from setuptools import setup
from setuptools import find_packages

setup(
    name='pact-test',
    version='0.3.90',
    author='Guido Barbaglia',
    author_email='guido.barbaglia@gmail.com',
    packages=find_packages(),
    license='LICENSE',
    long_description=open('README.rst').read(),
    description='Python implementation for Pact (http://pact.io/)',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest>=3.0',
        'pytest-pep8',
        'pytest-sugar',
        'pytest-mock'
    ],
    url='https://github.com/Kalimaha/pact-test/',
    scripts=['bin/pact-test'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing'
    ]
)
