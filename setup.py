import pathlib

from setuptools import setup
from robocrypt.info import version, email

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='robocrypt',
    version=version,
    packages=['robocrypt'],
    url='https://github.com/noahbroyles/Robocrypt',
    license='MIT',
    author='Noah Broyles',
    author_email=email,
    description='Simple encryption library that handles the background details for you.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        "console_scripts": ["robocrypt=robocrypt.cli:robocrypt_main"]
    },
    install_requires=['cryptography==3.4']
)
