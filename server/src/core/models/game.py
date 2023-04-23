from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey

from server.src.core.models.entity import Entity


class Game(Entity):
    __tablename__ = "games"

    title = Column(String, index=True, nullable=False)
    release_date = Column(Integer, index=True)
    short_description = Column(Text, nullable=False)
    long_description = Column(Text, nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    directory = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    status_id = Column(Integer, ForeignKey("game_statuses.id", ondelete="RESTRICT"), index=True, nullable=False)
    age_category_id = Column(Integer, ForeignKey("age_categories.id", ondelete="RESTRICT"), index=True, nullable=False)
