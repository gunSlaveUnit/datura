from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean

from server.oldsrc.core.models.entity import Entity


class Review(Entity):
    __tablename__ = "reviews"

    content = Column(Text, nullable=False)
    is_game_recommended = Column(Boolean, index=True, nullable=False)

    language_id = Column(Integer, ForeignKey("languages.id", ondelete="RESTRICT"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), index=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
