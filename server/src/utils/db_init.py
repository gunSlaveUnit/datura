from server.src.models.age_category import AgeCategory
from server.src.models.game_status import GameStatus
from server.src.models.platform import Platform
from server.src.models.role import Role
from server.src.models.user import User
from server.src.settings import admin_config, RoleType, GameStatusType, AgeType, PLATFORMS
from server.src.utils.crypt import get_password_hash
from server.src.utils.db import get_db


def init_db():
    db = next(get_db())

    if len(db.query(Role).all()) == 0:
        _add_roles(db)

    if len(db.query(User).all()) == 0:
        _add_admin(db)

    if len(db.query(GameStatus).all()) == 0:
        _add_game_statuses(db)

    if len(db.query(AgeCategory).all()) == 0:
        _add_ages(db)

    if len(db.query(Platform).all()) == 0:
        _add_platforms(db)


def _add_admin(session):
    admin_role = session.query(Role).filter(Role.title == RoleType.ADMIN).one()

    user = User(
        email=admin_config["EMAIL"],
        account_name=admin_config["ACCOUNT_NAME"],
        displayed_name=admin_config["DISPLAYED_NAME"],
        password=get_password_hash(admin_config["PASSWORD"]),
        is_staff=True,
        is_superuser=True,
        role_id=admin_role.id
    )

    session.add(user)
    session.commit()


def _add_roles(session):
    for role_type in RoleType:
        role = Role(title=role_type)
        session.add(role)
    session.commit()


def _add_game_statuses(session):
    for game_status_type in GameStatusType:
        game_status = GameStatus(title=game_status_type)
        session.add(game_status)
    session.commit()


def _add_ages(session):
    pegi_3 = AgeCategory(title=AgeType.PEGI_3,
                         description="Suitable for all age categories. The game must not contain sounds "
                                     "or images that may frighten young children. Profanity must not be"
                                     " used.")
    pegi_7 = AgeCategory(title=AgeType.PEGI_7, description="Suitable for people over 7 years old. The game may contain "
                                                           "moderate violence and some scenes may scare children.")
    pegi_12 = AgeCategory(title=AgeType.PEGI_12,
                          description="Suitable for people over 12 years old. The game may contain "
                                      "more realistic and naturalistic scenes of violence.")
    pegi_16 = AgeCategory(title=AgeType.PEGI_16,
                          description="Suitable for people over 16 years old. This rating is used when "
                                      "the violence becomes realistic and lifelike. Profanity, "
                                      "use of tobacco, alcohol, or illegal drugs may also be present.")
    pegi_18 = AgeCategory(title=AgeType.PEGI_18, description='Suitable for persons over 18 years of age. The "adult" '
                                                             'classification is used when an extreme level of violence and '
                                                             'unmotivated murder is present in the game. Romanticization of '
                                                             'drugs, gambling, and sexual activity may also be present.')

    session.add(pegi_3)
    session.add(pegi_7)
    session.add(pegi_12)
    session.add(pegi_16)
    session.add(pegi_18)

    session.commit()


def _add_platforms(session):
    for platform_title in PLATFORMS:
        platform = Platform(title=platform_title)

        session.add(platform)

    session.commit()
