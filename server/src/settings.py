from enum import Enum
from pathlib import Path

from dotenv import dotenv_values

DEBUG = False

BASE_PATH = Path(__file__).resolve().parent.parent
ENVS_PATH = BASE_PATH / 'envs'
MEDIA_PATH = BASE_PATH.parent / 'media'
GAMES_ASSETS_PATH = MEDIA_PATH / 'assets'
GAMES_ASSETS_CAPSULE_DIR = 'capsule'
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

API_VERSION = '0.1.0'
SESSION_TTL = 3 * 24 * 60 * 60

# Strings
GAMES_ROUTER_PREFIX = '/games'
COMPANIES_ROUTER_PREFIX = '/companies'
ASSETS_ROUTER_PREFIX = '/{game_id}/assets'
BUILDS_ROUTER_PREFIX = '/builds'
LIBRARY_ROUTER_PREFIX = '/library'

# Tags


class Tags(str, Enum):
    AUTH = 'Auth'
    GAMES = 'Games'
    COMPANIES = 'Companies'
    LIBRARY = 'Library'


tags_metadata = [
    {'name': Tags.AUTH, 'description': 'Describes an authentication API'},
    {'name': Tags.GAMES, 'description': 'Describes an API to manage games'},
    {'name': Tags.COMPANIES, 'description': 'Describes an API to manage companies'},
    {'name': Tags.LIBRARY, 'description': 'Describes an API to manage library records'},
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


PLATFORMS = ["windows", "linux"]
