# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


setup(
    name='pytest-docker-fixtures',
    version='1.3.0',
    description='pytest docker fixtures',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    keywords=['pytest', 'fixtures', 'docker'],
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/guillotinaweb/pytest-docker-fixtures',
    license='BSD',
    zip_safe=True,
    include_package_data=True,
    # ext_modules=ext_modules,
    packages=find_packages(),
    install_requires=[
        'pytest',
        'docker',
        'requests'
    ],
    extras_require={
        'pg': [
            'psycopg2'
        ],
        'rabbitmq': [
            'pika==0.12.0'
        ],
        'kafka': [
            'kafka-python'
        ]
    }
)
