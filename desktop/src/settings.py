from pathlib import Path

# TODO: rename URL URI URN, may be it will be better than ...URL_PART

# Paths

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = BASE_DIR / 'src'
LAYOUTS_DIR = SOURCES_DIR / 'gui'

# URLs
SERVER_URL = "http://127.0.0.1:8000/"

# Auth
AUTH_URL = SERVER_URL + "auth/"
REGISTER_URL = AUTH_URL + "sign-up/"
LOGIN_URL = AUTH_URL + "sign-in/"
LOGOUT_URL = AUTH_URL + "sign-out/"
ME_URL = AUTH_URL + "me/"

# Entities
GAMES_URL = SERVER_URL + 'games/'
ASSETS_URL_PART = 'assets/'
BUILDS_URL_PART = 'builds/'

COMPANIES_URL = SERVER_URL + 'companies/'

LIBRARY_URL = SERVER_URL + 'library/'
