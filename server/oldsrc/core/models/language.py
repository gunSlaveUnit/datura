from sqlalchemy import Column, String, Integer, ForeignKey, Boolean

from server.oldsrc.core.models.entity import Entity


class Language(Entity):
    __tablename__ = "languages"

    title = Column(String, index=True, nullable=False)


class GameLanguage(Entity):
    __tablename__ = "game_languages"

    interface = Column(Boolean)
    subtitles = Column(Boolean)
    voice_acting = Column(Boolean)

    language_id = Column(Integer, ForeignKey("languages.id", ondelete="RESTRICT"), index=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), index=True, nullable=False)
