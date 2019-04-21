from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
import re, ast

#get version from version variable in plaid_integration/init.py
_version_re = re.compile(r'version\s+=\s+(.*)')

requirements = parse_requirements('requirements.txt', session="")

setup(
name='vaico_works',
version=1,
description='Vaico Works',
author='Vaico',
author_email='pioneros@github.com',
packages=find_packages(),
zip_safe=False,
include_package_data=True,
#dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
