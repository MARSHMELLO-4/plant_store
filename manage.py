import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_store.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
           "Import Error"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    #pehchan kon
