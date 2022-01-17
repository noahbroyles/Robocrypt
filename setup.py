import pathlib

from setuptools import setup
from robocrypt import __version__ as version

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='Robocrypt',
    version=version,
    packages=['robocrypt'],
    url='https://github.com/noahbroyles/Robocrypt',
    license='MIT',
    author='Noah Broyles',
    author_email='noah@x3nzpouwu.com',
    description='Simple encryption library that handles the background details for you.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        "console_scripts": ["robocrypt=robocrypt.cli:command_line"]
    }
)