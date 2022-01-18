#!/usr/bin/env python3

import subprocess


subprocess.call(['rm', '-fr', 'build/', 'dist/'])
subprocess.call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
subprocess.call(['twine', 'upload', 'dist/*'])
