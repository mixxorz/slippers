import os
import sys

from django.core.management import execute_from_command_line

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"

if __name__ == "__main__":
    command, *rest = sys.argv
    execute_from_command_line([command, "test", *rest])
