from enum import Enum
from pathlib import Path

from dotenv import dotenv_values

DEBUG = False

BASE_DIR = Path(__file__).resolve().parent.parent
ENVS_DIR = BASE_DIR / 'envs'

if DEBUG:
    ENVS_DIR = ENVS_DIR / 'dev'
else:
    ENVS_DIR = ENVS_DIR / 'prod'

# Databases

admin_config = dotenv_values(ENVS_DIR / ".admin")
redis_config = dotenv_values(ENVS_DIR / ".redis")
database_config = dotenv_values(ENVS_DIR / ".db")

if DEBUG:
    CONNECTION_STRING = f"sqlite:///{BASE_DIR / database_config['NAME']}"
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

# Tags


class Tags(str, Enum):
    AUTH = 'Auth'
    GAMES = 'Games'
    COMPANIES = 'Companies'


tags_metadata = [
    {'name': Tags.AUTH, 'description': 'Describes an authentication API'},
    {'name': Tags.GAMES, 'description': 'Describes an API to manage games'},
    {'name': Tags.COMPANIES, 'description': 'Describes an  API to manage companies'},
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
