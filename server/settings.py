# Versions
from enum import Enum

API_VERSION = '0.1.0'

# Strings
GAMES_ROUTER_PREFIX = '/games'

# Tags


class Tags(str, Enum):
    GAMES = 'Games'


tags_metadata = [
    {'name': Tags.GAMES, 'description': 'Describes API to manage games'},
]
