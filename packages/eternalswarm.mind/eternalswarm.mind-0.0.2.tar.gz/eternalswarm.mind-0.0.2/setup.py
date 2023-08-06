import os

from setuptools import setup

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    name="eternalswarm.mind",
    version=version,
    packages=['eternalswarm.mind'],
    namespace_packages=['eternalswarm'],
    install_requires=['grpcio'],
    author='Matthijs Gielen',
    author_email='eternalswarm@mwgielen.com',
    url='https://gitlab.com/eternal-swarm/mind',
    description='The protobuf files to talk to the eternalswarm drone.'
)
