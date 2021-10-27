#!/usr/bin/python3

import os
import sys

try:
    length = int(sys.argv[1])
    with open('/var/secure/robocrypt.salt', 'wb') as sf:
        sf.write(os.urandom(length))
except IndexError:
    print("USAGE: \n\tgenerateSalt <length>")
except ValueError:
    print("Salt length must be an integer")
