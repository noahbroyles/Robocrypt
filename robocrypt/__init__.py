"""
---------------------------------------------------------
-     ____        __                                __  -
-    / __ \____  / /_  ____  ____________  ______  / /_ -
-   / /_/ / __ \/ __ \/ __ \/ ___/ ___/ / / / __ \/ __/ -
-  / _, _/ /_/ / /_/ / /_/ / /__/ /  / /_/ / /_/ / /_   -
- /_/ |_|\____/_.___/\____/\___/_/   \__, / .___/\__/   -
-                                   /____/_/            -
---------------------------------------------------------
A simple encryption library that handles the background details for you.

Supports file and folder encryption, as well as raw data bytes encryption.
"""

from .library import *
from .cli import command_line as main
from .info import (
    version as __version__,
    author as __author__,
    email as __email__
)
