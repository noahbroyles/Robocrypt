#!/usr/bin/env python3

import subprocess


subprocess.call(['rm', '-fr', 'build/', 'dist/'])
subprocess.call(['python3', '-m', 'build'])
subprocess.call(['twine', 'upload', 'dist/*'])
