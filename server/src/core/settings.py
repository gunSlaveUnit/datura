from enum import Enum, auto
from pathlib import Path

from dotenv import dotenv_values
from starlette.templating import Jinja2Templates

DEBUG = False

BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENVS_PATH = BASE_PATH / 'envs'
MEDIA_PATH = BASE_PATH.parent / 'media'
AVATARS_PATH = MEDIA_PATH / 'avatars'
GAMES_ASSETS_PATH = MEDIA_PATH / 'assets'
GAMES_ASSETS_HEADER_DIR = 'header'
GAMES_ASSETS_CAPSULE_DIR = 'capsule'
GAMES_ASSETS_TRAILERS_DIR = 'trailers'
GAMES_ASSETS_SCREENSHOTS_DIR = 'screenshots'
GAMES_ASSETS_BUILDS_DIR = 'builds'
TEMPLATES_DIR = BASE_PATH / 'templates'
STATIC_PATH = BASE_PATH / 'static'

templates = Jinja2Templates(directory=TEMPLATES_DIR)

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

API_PREFIX = '/api'
API_VERSION_1_PREFIX = API_PREFIX + '/v1'
SESSION_TTL = 3 * 24 * 60 * 60

# Strings
AUTH_ROUTER_PREFIX = '/auth'
GAMES_ROUTER_PREFIX = '/games'
USERS_ROUTER_PREFIX = '/users'
COMPANIES_ROUTER_PREFIX = '/companies'
ASSETS_ROUTER_PREFIX = '/{game_id}'
BUILDS_ROUTER_PREFIX = '/builds'
LIBRARY_ROUTER_PREFIX = '/library'
CART_ROUTER_PREFIX = '/cart'
AGE_CATEGORIES_ROUTER_PREFIX = '/age-categories'
PLATFORMS_ROUTER_PREFIX = '/platforms'
SYSTEM_REQUIREMENTS_ROUTER_PREFIX = '/requirements'
LANGUAGES_ROUTER_PREFIX = '/languages'
GAME_TAGS_ROUTER_PREFIX = '/{game_id}/tags'
TAGS_ROUTER_PREFIX = '/tags'
REVIEWS_ROUTER_PREFIX = '/{game_id}/reviews'
ADMIN_ROUTER_PREFIX = '/admin'
PAYMENTS_ROUTER_PREFIX = '/payments'


# Tags


class Tags(str, Enum):
    HOME = 'Home'
    V1 = 'V1'

    AUTH = 'Auth'
    USERS = 'Users'
    ROLES = 'Roles'

    COMPANIES = 'Companies'

    LIBRARY = 'Library'

    CART = 'Cart'
    PAYMENTS = 'Payments'

    GAMES = 'Games'
    AGE_CATEGORIES = 'Age categories'
    GAME_TAGS = 'Game tags'
    TAGS = 'Tags'
    ASSETS = 'Assets'
    BUILDS = 'Builds'
    PLATFORMS = 'Platforms'
    SYSTEM_REQUIREMENTS = 'System requirements'
    GAME_LANGUAGES = 'Game languages'
    LANGUAGES = 'Languages'
    REVIEWS = 'Reviews'

    ADMIN = 'Admin'


tags_metadata = [
    {'name': Tags.HOME, 'description': 'General information describing the API'},
    {'name': Tags.V1, 'description': 'API version 1'},
    {'name': Tags.AUTH, 'description': ''},
    {'name': Tags.USERS, 'description': ''},
    {'name': Tags.ROLES, 'description': ''},
    {'name': Tags.COMPANIES, 'description': ''},
    {'name': Tags.LIBRARY, 'description': ''},
    {'name': Tags.CART, 'description': ''},
    {'name': Tags.PAYMENTS, 'description': ''},
    {'name': Tags.GAMES, 'description': ''},
    {'name': Tags.AGE_CATEGORIES, 'description': ''},
    {'name': Tags.GAME_TAGS, 'description': ''},
    {'name': Tags.TAGS, 'description': ''},
    {'name': Tags.ASSETS, 'description': ''},
    {'name': Tags.BUILDS, 'description': ''},
    {'name': Tags.PLATFORMS, 'description': ''},
    {'name': Tags.SYSTEM_REQUIREMENTS, 'description': ''},
    {'name': Tags.GAME_LANGUAGES, 'description': ''},
    {'name': Tags.LANGUAGES, 'description': ''},
    {'name': Tags.REVIEWS, 'description': ''},
    {'name': Tags.ADMIN, 'description': ''},
]


# Types


class RoleType(Enum):
    ADMIN = "admin"
    USER = "user"


class AgeType(Enum):
    PEGI_3 = 'PEGI 3'
    PEGI_7 = 'PEGI 7'
    PEGI_12 = 'PEGI 12'
    PEGI_16 = 'PEGI 16'
    PEGI_18 = 'PEGI 18'


# From https://docs.python.org/3/library/sys.html
class PlatformType(Enum):
    LINUX = 'linux'
    WINDOWS = 'win32'


DEFAULT_AVATAR_FILENAME = 'default.webp'

DEFAULT_TAGS = [
    'Indie',
    'Strategy',
    'Cyberpunk',
    'Shooter',
    '2D',
    '3D',
    'First person',
    'Third party',
    'Action',
    'Complex',
    'Bagel',
    'Great soundtrack',
    'Simulator',
    'Pixel graphic',
    'Anime',
    'Role-playing',
    'Adventure',
    'Atmosphere',
    'For two',
    'Cooperative',
    'Multiplayer',
    'Battle royal',
    'Tactics',
    'Puzzle',
]

DEFAULT_LANGUAGES = [
    'Chinese',
    'Spanish',
    'English',
    'Hindi',
    'Arab',
    'Bengal',
    'Portuguese',
    'Russian',
    'Japanese',
    'Javanese',
]
