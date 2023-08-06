import os
from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='os-package-registry',
    version='0.0.21',
    description=(
        'Manage a registry of packages on an ElasticSearch instance'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/openspending/os-package-registry',

    author='Open Knowledge International',
    author_email='info@okfn.org',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='fdp fiscal data package openspending elasticsearch',

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'elasticsearch>=5.0.0,<6.0.0',
        'os-api-cache>=0.0.7'
    ],
)
