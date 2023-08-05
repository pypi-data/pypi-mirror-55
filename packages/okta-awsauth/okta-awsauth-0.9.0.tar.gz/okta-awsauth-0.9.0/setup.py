from setuptools import setup, find_packages, os

APP = ['oktaawscli/okta_awscli.py']
DATA_FILES = ['oktaawscli/aws_auth.py','oktaawscli/version.py' ,'oktaawscli/okta_auth_config.py', 'oktaawscli/okta_auth.py', 'oktaawscli/__init__.py']
OPTIONS = {}

here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'oktaawscli/version.py')).read())

setup(
    name='okta-awsauth',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version=__version__,
    description='Provides a wrapper for Okta authentication to awscli',
    packages=find_packages(),
    license='Apache License 2.0',
    author='Franco Papalardo',
    author_email='franco.papalardo@ownzones.com',
    url='https://github.com/OwnZones/okta-awscli',
    entry_points={
        'console_scripts': [
            'okta-awscli=oktaawscli.okta_awscli:main',
        ],
    },
    install_requires=[
        'requests',
        'click',
        'bs4',
        'boto3',
        'ConfigParser',
        'keyring',
        ],
    extras_require={
        'U2F': ['python-u2flib-host']
    },
    python_requires='>=3.6',
)
