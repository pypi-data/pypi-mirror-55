import setuptools
from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='arab_bot_list',
    url='https://github.com',
    author='Jake',
    author_email='jakediserin@gmail.com',
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    version='2.3.3',
    license='MIT',
    description='The official API package for Arab\'s bot list using Python 3',

)
