# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['aws_credential_process']
install_requires = \
['boto3>=1.10,<2.0',
 'click>=7.0,<8.0',
 'keyring>=19.2,<20.0',
 'yubikey-manager==3.0.0']

entry_points = \
{'console_scripts': ['aws-credential-process = aws_credential_process:main']}

setup_kwargs = {
    'name': 'aws-credential-process',
    'version': '0.1.0',
    'description': 'AWS Credential Process',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
