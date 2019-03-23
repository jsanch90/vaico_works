from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
import re, ast

#get version from version variable in plaid_integration/init.py
_version_re = re.compile(r'version\s+=\s+(.*)')

with open('plaid_integration/init.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
    f.read().decode('utf-8')).group(1)))

requirements = parse_requirements('requirements.txt', session="")

setup(
name='plaid_integration',
version=1,
description='Plaid Integration',
author='Vaico',
author_email='pioneros@github.com',
packages=find_packages(),
zip_safe=False,
include_package_data=True,
dependency_links=[str(ir._link) for ir in requirements if ir._link]
)