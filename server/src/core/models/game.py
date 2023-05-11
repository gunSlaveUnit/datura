from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey, Boolean

from server.src.core.models.entity import Entity


class Game(Entity):
    __tablename__ = "games"

    title = Column(String, index=True, nullable=False)
    developer = Column(String, index=True, nullable=False)
    publisher = Column(String, index=True, nullable=False)
    release_date = Column(Integer, index=True)
    short_description = Column(Text, nullable=False)
    long_description = Column(Text, nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    directory = Column(String, nullable=False)

    is_approved = Column(Boolean, nullable=False, default=False)
    is_send_for_verification = Column(Boolean, nullable=False, default=False)
    is_published = Column(Boolean, nullable=False, default=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    age_category_id = Column(Integer, ForeignKey("age_categories.id", ondelete="RESTRICT"), index=True, nullable=False)
