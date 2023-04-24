from pathlib import Path

APP_ID = 'Rundsoft.foogie.desktop.2023.4.4-dev'

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / 'resources'
ICONS_DIR = RESOURCES_DIR / 'icons'
SOURCES_DIR = BASE_DIR / 'src'
LAYOUTS_DIR = SOURCES_DIR / 'gui'
