from enum import Enum
from pathlib import Path

from dotenv import dotenv_values

DEBUG = False

BASE_PATH = Path(__file__).resolve().parent.parent
ENVS_PATH = BASE_PATH / 'envs'
MEDIA_PATH = BASE_PATH.parent / 'media'
AVATARS_PATH = MEDIA_PATH / 'avatars'
GAMES_ASSETS_PATH = MEDIA_PATH / 'assets'
GAMES_ASSETS_CAPSULE_DIR = 'capsule'
GAMES_ASSETS_SCREENSHOTS_DIR = 'screenshots'
GAMES_ASSETS_BUILDS_DIR = 'builds'

if DEBUG:
    ENVS_PATH = ENVS_PATH / 'dev'
else:
    ENVS_PATH = ENVS_PATH / 'prod'

# Databases

admin_config = dotenv_values(ENVS_PATH / ".admin")
redis_config = dotenv_values(ENVS_PATH / ".redis")
database_config = dotenv_values(ENVS_PATH / ".db")

if DEBUG:
    CONNECTION_STRING = f"sqlite:///{BASE_PATH / database_config['NAME']}"
else:
    CONNECTION_STRING = f'postgresql://{database_config["USER"]}:{database_config["PASSWORD"]}' \
                        f'@{database_config["HOST"]}:{database_config["PORT"]}/{database_config["NAME"]}'

# Versions

API_VERSION_1_PREFIX = '/v1'
SESSION_TTL = 3 * 24 * 60 * 60

# Strings
AUTH_ROUTER_PREFIX = '/auth'
GAMES_ROUTER_PREFIX = '/games'
COMPANIES_ROUTER_PREFIX = '/companies'
ASSETS_ROUTER_PREFIX = '/{game_id}/assets'
BUILDS_ROUTER_PREFIX = '/builds'
LIBRARY_ROUTER_PREFIX = '/library'
CART_ROUTER_PREFIX = '/cart'


# Tags


class Tags(str, Enum):
    HOME = 'Home'
    V1 = 'V1'
    AUTH = 'Auth'
    GAMES = 'Games'
    COMPANIES = 'Companies'
    LIBRARY = 'Library'
    USERS = 'Users'
    CART = 'Cart'


tags_metadata = [
    {'name': Tags.HOME, 'description': 'General information describing the API'},
    {'name': Tags.V1, 'description': 'API version 1'},
    {'name': Tags.AUTH, 'description': 'Describes an authentication API'},
    {'name': Tags.GAMES, 'description': 'Describes an API to manage games'},
    {'name': Tags.COMPANIES, 'description': 'Describes an API to manage companies'},
    {'name': Tags.LIBRARY, 'description': 'Describes an API to manage library records'},
    {'name': Tags.USERS, 'description': 'Describes an API to manage users'},
    {'name': Tags.CART, 'description': 'Describes an API to manage cart records'},
]


# Types


class RoleType(Enum):
    ADMIN = "admin"
    USER = "user"


class GameStatusType(Enum):
    NOT_SEND = 'Not send'
    SEND = 'Send'
    NOT_APPROVED = 'Not approved'
    APPROVED = 'Approved'
    NOT_PUBLISHED = 'Not published'
    PUBLISHED = 'Published'


class AgeType(Enum):
    PEGI_3 = 'PEGI 3'
    PEGI_7 = 'PEGI 7'
    PEGI_12 = 'PEGI 12'
    PEGI_16 = 'PEGI 16'
    PEGI_18 = 'PEGI 18'


# From https://docs.python.org/3/library/sys.html
PLATFORMS = [
    'aix',
    'emscripten',
    'linux',
    'wasi',
    'win32',
    'cygwin',
    'darwin'
]

DEFAULT_AVATAR_FILENAME = 'default.webp'
