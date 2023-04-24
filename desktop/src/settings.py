from pathlib import Path

APP_ID = 'Rundsoft.foogie.desktop.2023.4.4-dev'

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / 'resources'
ICONS_DIR = RESOURCES_DIR / 'icons'
SOURCES_DIR = BASE_DIR / 'src'
LAYOUTS_DIR = SOURCES_DIR / 'gui'

API_VERSION = 1

SERVER_URL = f"http://localhost:8000/v{API_VERSION}/"
AUTH_URL = SERVER_URL + "auth/"
REGISTER_URL = AUTH_URL + "sign-up/"
LOGIN_URL = AUTH_URL + "sign-in/"
LOGOUT_URL = AUTH_URL + "sign-out/"
ME_URL = AUTH_URL + "me/"
