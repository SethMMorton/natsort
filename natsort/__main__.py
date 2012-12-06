"""Main entry point, based on unittest's"""

import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m natsort"

from .main import main
try:
    main()
except ValueError as a:
    sys.exit(str(a))
except KeyboardInterrupt:
    sys.exit(1)
