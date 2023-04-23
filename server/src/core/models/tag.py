from sqlalchemy import Column, String, Text, Integer, ForeignKey

from server.src.core.models.entity import Entity


class GameTagAssociation(Entity):
    __tablename__ = 'games_tags'

    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


class Tag(Entity):
    __tablename__ = "tags"

    title = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
