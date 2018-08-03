from setuptools import find_packages, setup

setup(
    name='tinyurls',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/rangertaha/tinyurl',
    license='MIT',
    install_requires=['tornado', 'SQLAlchemy', 'validators', 'fluent',
                      'pycodestyle', 'prometheus-client'],
    author='rangertaha',
    author_email='rangertaha@gmail.com',
    description='URL shortening service to be used in a microservices '
                'environment.',
    scripts=['bin/tinyurls'],
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'),
)
