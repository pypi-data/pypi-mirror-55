#!python3

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='reqqie',
    version="0.0.4",
    author="Jesper Ribbe",
    description="Text based Requirements management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=["reqqie"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    entry_points={
        'console_scripts': [
            'reqqie = reqqie.app:main',
        ]
    },
    install_requires=[
        "tdbase>=0.0.4",
        "typing>=3.7",
        "pygit2>=0.28.2",
        "reportlab>=3.5.21",
    ],
    python_requires='>=3.6',
)
