import os

from setuptools import setup

setup(
    name="eternalswarm.mind",
    version='0.0.4',
    packages=['eternalswarm.mind'],
    namespace_packages=['eternalswarm'],
    install_requires=['grpcio'],
    author='Matthijs Gielen',
    author_email='eternalswarm@mwgielen.com',
    url='https://gitlab.com/eternal-swarm/mind',
    description='The protobuf files to talk to the eternalswarm drone.',
    package_data={"eternalswarm.mind": ["py.typed", "*.pyi"]},
    zip_safe=False
)
