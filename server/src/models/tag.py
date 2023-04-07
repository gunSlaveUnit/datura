from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from server.src.models.entity import Entity


class GameTagAssociation(Entity):
    __tablename__ = 'games_tags'

    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    game = relationship("Game", backref="tags")
    tag = relationship("Tag", backref="games")


class Tag(Entity):
    # TODO: or use categories with genres?

    __tablename__ = "tags"

    title = Column(String, unique=True, nullable=False)
    description =  Column(Text, nullable=False)
