# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
readme_file = os.path.join(here, 'README.md')


def read_text(file_path):
    """
    fix the default operating system encoding is not utf8.
    """
    if sys.version_info.major < 3:
        with open(file_path) as f:
            return f.read()
    with open(file_path, encoding="utf8") as f:
        return f.read()


README = read_text(os.path.join(here, 'README.md'))

requires = [

]

test_requirements = [

]


setup(
    name='servos-framework',
    description='Pure-Python SM2/SM3/SM4 implementation',
    version='2.7.1',
    author='jingh',
    author_email='jingh.lib@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/knitmesh/gmssl',
    install_requires=requires,
    tests_require=test_requirements,
    platforms='all platform',
    license='BSD',
    setup_requires=['nose>=1.0', 'pbr>=1.8'],
    test_suite='nose.collector',
    package_data={
        '': ['locale/en/LC_MESSAGES/*.mo', 'locale/zh_CN/LC_MESSAGES/*.mo'],
    },
    pbr=True
)
