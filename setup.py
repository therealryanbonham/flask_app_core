from setuptools import setup

setup(
    name='flask-app-core',    # This is the name of your PyPI-package.
    version='0.0.1',                          # Update the version number for new releases
    # The name of your scipt, and also the command you'll be using for calling it
    packages=['flask_app_core'],
    python_requires='>=3.6',
    author='Ryan Bonham',
    author_email='ryan@transparent-tech.com',
    license='MIT',
    description='Flask Wrapper to setup Flask, and some common Flask Extension via Environtment Variables .',
    url='https://github.com/TransparentTechnologies/flask_app_core',
    install_requires=[
        'Flask>=0.12.0'
    ],
    extras_require={
        'Flask-SQLAlchemy':  ["Flask-SQLAlchemy>=2.3.0"],
        'AWS-XRay':  ["aws-xray-sdk>=1.0"],
        'DebugToolbar': ["flask-debugtoolbar>=0.10.1"],
        'DynamoDBCache': ["Flask-Sessionstore>=0.4.5", "boto3>=1.6.0"],
        "RedisCache": ["Flask-Sessionstore>=0.4.5", "redis>=2.10.0"]
    }
)
