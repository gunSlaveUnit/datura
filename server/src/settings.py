# Versions
from enum import Enum

API_VERSION = '0.1.0'

# Strings
GAMES_ROUTER_PREFIX = '/games'
COMPANIES_ROUTER_PREFIX = '/companies'
ASSETS_ROUTER_PREFIX = '/{game_id}/assets'

# Tags


class Tags(str, Enum):
    GAMES = 'Games'
    COMPANIES = 'Companies'
    ASSETS = 'Assets'


tags_metadata = [
    {'name': Tags.GAMES, 'description': 'Describes an API to manage games'},
    {'name': Tags.COMPANIES, 'description': 'Describes an  API to manage companies'},
    {'name': Tags.ASSETS, 'description': 'Describes an API for managing game resources'},
]
