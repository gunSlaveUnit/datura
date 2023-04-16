import sys

from PySide6.QtGui import QGuiApplication, QColor
from PySide6.QtQml import QQmlApplicationEngine

from desktop.src.logic.LibraryDetaledLogic import LibraryDetailedLogic
from desktop.src.logic.StoreDetaledLogic import StoreDetailedLogic
from desktop.src.models.game import GameList
from desktop.src.settings import LAYOUTS_DIR
from desktop.src.logic.AuthLogic import AuthLogic
from services.AuthService import AuthService

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    app.setPalette(QColor("black"))

    engine = QQmlApplicationEngine()

    auth_service = AuthService()

    auth_logic = AuthLogic(auth_service)
    engine.rootContext().setContextProperty("auth_logic", auth_logic)

    library_detailed_logic = LibraryDetailedLogic(auth_service)
    engine.rootContext().setContextProperty("library_detailed_logic", library_detailed_logic)

    store_detailed_logic = StoreDetailedLogic(auth_service)
    engine.rootContext().setContextProperty("store_detailed_logic", store_detailed_logic)

    game_list_model = GameList(auth_service)
    engine.rootContext().setContextProperty("game_list_model", game_list_model)

    start_file_location = LAYOUTS_DIR / "main.qml"
    engine.load(start_file_location)

    app.exec()
