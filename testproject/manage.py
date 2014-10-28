#!/usr/bin/env python
import os
import sys

import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.settings")
    sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

    from django.core.management import execute_from_command_line

    django.setup()

    execute_from_command_line(sys.argv)
