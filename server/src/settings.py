# Versions
from enum import Enum

API_VERSION = '0.1.0'

# Strings
GAMES_ROUTER_PREFIX = '/games'
COMPANIES_ROUTER_PREFIX = '/companies'

# Tags


class Tags(str, Enum):
    GAMES = 'Games'
    COMPANIES = 'Companies'


tags_metadata = [
    {'name': Tags.GAMES, 'description': 'Describes API to manage games'},
    {'name': Tags.COMPANIES, 'description': 'Describes API to manage companies'},
]
