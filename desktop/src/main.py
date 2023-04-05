import sys

from PySide6.QtGui import QGuiApplication, QColor
from PySide6.QtQml import QQmlApplicationEngine

from desktop.src.settings import LAYOUTS_DIR
from desktop.src.logic.AuthLogic import AuthLogic

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    app.setPalette(QColor("black"))

    engine = QQmlApplicationEngine()

    auth_logic = AuthLogic()
    engine.rootContext().setContextProperty("auth_logic", auth_logic)

    start_file_location = LAYOUTS_DIR / "main.qml"
    engine.load(start_file_location)

    app.exec()
