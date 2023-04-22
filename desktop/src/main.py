import sys

from PySide6.QtGui import QGuiApplication, QColor
from PySide6.QtQml import QQmlApplicationEngine

from desktop.src.logic.AppLogic import AppLogic
from desktop.src.logic.CompanyLogic import CompanyLogic
from desktop.src.logic.LibraryDetaledLogic import LibraryDetailedLogic
from desktop.src.logic.NavigationLogic import NavigationLogic
from desktop.src.logic.StoreDetaledLogic import StoreDetailedLogic
from desktop.src.models.game import GameList
from desktop.src.services.CompanyService import CompanyService
from desktop.src.settings import LAYOUTS_DIR
from desktop.src.logic.AuthLogic import AuthLogic
from services.AuthService import AuthService

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    app.setPalette(QColor("black"))

    engine = QQmlApplicationEngine()

    auth_service = AuthService()
    engine.rootContext().setContextProperty("auth_service", auth_service)

    auth_logic = AuthLogic(auth_service)
    engine.rootContext().setContextProperty("auth_logic", auth_logic)

    company_service = CompanyService(auth_service)
    company_logic = CompanyLogic(company_service)
    engine.rootContext().setContextProperty("company_logic", company_logic)

    library_detailed_logic = LibraryDetailedLogic(auth_service)
    engine.rootContext().setContextProperty("library_detailed_logic", library_detailed_logic)

    store_detailed_logic = StoreDetailedLogic(auth_service)
    engine.rootContext().setContextProperty("store_detailed_logic", store_detailed_logic)

    app_logic = AppLogic(auth_service)
    engine.rootContext().setContextProperty("app_logic", app_logic)

    library_game_list_model = GameList(auth_service, company_service)
    engine.rootContext().setContextProperty("library_game_list_model", library_game_list_model)

    store_game_list_model = GameList(auth_service, company_service)
    engine.rootContext().setContextProperty("store_game_list_model", store_game_list_model)

    own_releases_game_list_model = GameList(auth_service, company_service)
    engine.rootContext().setContextProperty("own_releases_game_list_model", own_releases_game_list_model)

    navigation_logic = NavigationLogic()
    engine.rootContext().setContextProperty("navigation_logic", navigation_logic)

    start_file_location = LAYOUTS_DIR / "main.qml"
    engine.load(start_file_location)

    app.exec()
