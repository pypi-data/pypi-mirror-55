#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages
# https://stackoverflow.com/questions/49837301/pip-10-no-module-named-pip-req
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

if sys.version_info < (3, 6):
    raise NotImplementedError(
        """Nextcode SDK does not support Python versions older than 3.6"""
    )

root_dir = 'nextcodecli'


def get_version():
    with open(os.path.join(root_dir, 'VERSION')) as version_file:
        return version_file.readlines()[0].strip()


version = get_version()
if 'SETUP_BRANCH' in os.environ:
    version += "-%s" % os.environ['SETUP_BRANCH']


setup(
    name='nextcode-cli',
    python_requires=">=3.6",
    version=version,
    description='Nextcode sample processing tool',
    author='WUXI NextCODE',
    author_email='support@wuxinextcode.com',
    url='https://www.wuxinextcode.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={'nextcodecli': ['VERSION', 'PUBLIC_KEY']},
    install_requires=[
        str(i.req)
        for i in parse_requirements('requirements.txt', session=False)
        if i.req
    ],
    entry_points={
        'console_scripts': [
            'nextcode = nextcodecli.__main__:cli',
        ],
        'pytest11': [
            'nc-wf = nextcodecli.pytest.wf_plugin',
        ]
    },
)
