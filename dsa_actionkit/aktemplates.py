#!/usr/bin/env python
import os
import sys
from pathlib import Path


def serve_templates():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dsa_actionkit.settings")
    sys.path.append(
        Path.cwd(),
    )
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    serve_templates()
