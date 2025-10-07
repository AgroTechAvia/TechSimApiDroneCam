from setuptools import setup, find_packages

setup(
    name='drone_control_api',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "transforms3d==0.4.2",
    ],
    description='description',
    author='DroneCam',
    author_email='some@example.com',
    url='.',
)