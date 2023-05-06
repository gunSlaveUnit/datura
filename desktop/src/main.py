import sys
import ctypes

from PySide6.QtGui import QGuiApplication, QColor, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from desktop.src.logic.AppLogic import AppLogic
from desktop.src.logic.AuthLogic import AuthLogic
from desktop.src.logic.BuildLogic import BuildLogic
from desktop.src.logic.CartLogic import CartLogic
from desktop.src.logic.CompanyLogic import CompanyLogic
from desktop.src.logic.CurrentUserLogic import CurrentUserLogic
from desktop.src.logic.LibraryDetaledLogic import LibraryDetailedLogic
from desktop.src.logic.StoreDetailedLogic import StoreDetailedLogic
from desktop.src.logic.WalletLogic import WalletLogic
from desktop.src.models.build import BuildList
from desktop.src.models.game import GameList
from desktop.src.services.AuthService import AuthService
from desktop.src.services.CartService import CartService
from desktop.src.services.CompanyService import CompanyService
from desktop.src.services.GameService import GameService
from desktop.src.services.LibraryService import LibraryService
from desktop.src.services.WalletService import WalletService
from desktop.src.settings import ICONS_DIR, LAYOUTS_DIR, APP_ID

if __name__ == '__main__':
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

    app = QGuiApplication(sys.argv)
    app.setPalette(QColor("black"))

    icon_file_path = ICONS_DIR / "icon.png"
    app.setWindowIcon(QIcon(str(icon_file_path)))

    engine = QQmlApplicationEngine()

    auth_service = AuthService()

    wallet_service = WalletService(auth_service)
    game_service = GameService(auth_service)
    library_service = LibraryService(auth_service)
    cart_service = CartService(auth_service)

    auth_logic = AuthLogic(auth_service)
    engine.rootContext().setContextProperty("auth_logic", auth_logic)

    current_user_logic = CurrentUserLogic(auth_service)
    engine.rootContext().setContextProperty("current_user_logic", current_user_logic)

    wallet_logic = WalletLogic(wallet_service)
    engine.rootContext().setContextProperty("wallet_logic", wallet_logic)

    cart_logic = CartLogic(cart_service)
    engine.rootContext().setContextProperty("cart_logic", cart_logic)

    store_detailed_logic = StoreDetailedLogic(game_service, library_service, cart_service)
    engine.rootContext().setContextProperty("store_detailed_logic", store_detailed_logic)

    library_detailed_logic = LibraryDetailedLogic(auth_service)
    engine.rootContext().setContextProperty("library_detailed_logic", library_detailed_logic)

    company_service = CompanyService(auth_service)
    company_logic = CompanyLogic(company_service)
    engine.rootContext().setContextProperty("company_logic", company_logic)

    app_logic = AppLogic(auth_service)
    engine.rootContext().setContextProperty("app_logic", app_logic)

    build_logic = BuildLogic(auth_service)
    engine.rootContext().setContextProperty("build_logic", build_logic)

    game_list_model = GameList(auth_service, company_service)
    engine.rootContext().setContextProperty("game_list_model", game_list_model)

    build_list_model = BuildList(auth_service)
    engine.rootContext().setContextProperty("build_list_model", build_list_model)

    start_file_location = LAYOUTS_DIR / "main.qml"
    engine.load(start_file_location)

    app.exec()
