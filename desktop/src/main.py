import sys

from PySide6.QtGui import QGuiApplication, QColor, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from desktop.src.settings import LAYOUTS_DIR


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    start_file_location = LAYOUTS_DIR / "main.qml"
    engine.load(start_file_location)

    app.exec()
