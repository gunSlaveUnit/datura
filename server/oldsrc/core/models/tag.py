from sqlalchemy import Column, String, Integer, ForeignKey

from server.oldsrc.core.models.entity import Entity


class GameTagAssociation(Entity):
    __tablename__ = 'games_tags'

    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


class Tag(Entity):
    __tablename__ = "tags"

    title = Column(String, unique=True, nullable=False)
