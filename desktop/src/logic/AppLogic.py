import datetime
import os
from pathlib import Path

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl

from desktop.src.settings import GAMES_URL


class AppLogic(QObject):
    BASE_YEAR = 1958

    id_changed = Signal()

    title_changed = Signal()
    price_changed = Signal()
    short_description_changed = Signal()
    long_description_changed = Signal()

    day_index_changed = Signal()
    month_index_changed = Signal()
    year_index_changed = Signal()
    coming_soon_changed = Signal()

    possible_days_changed = Signal()
    possible_months_changed = Signal()
    possible_years_changed = Signal()

    screenshots_changed = Signal()
    displayed_screenshots_changed = Signal()
    header_changed = Signal()
    displayed_header_changed = Signal()
    capsule_changed = Signal()
    displayed_capsule_changed = Signal()
    trailers_changed = Signal()
    displayed_trailers_changed = Signal()
    project_files_changed = Signal()
    displayed_project_files_changed = Signal()

    drafted = Signal()

    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self.is_approved = None

        self._title = 'Unnamed'
        self._price = "0.00"
        self._short_description = ''
        self._long_description = ''

        self._day_index = datetime.datetime.now().day - 1
        self._month_index = datetime.datetime.now().month - 1
        self._year_index = datetime.datetime.now().year - AppLogic.BASE_YEAR
        self._coming_soon = True

        self._screenshots = []
        self._header = ''
        self._capsule = ''
        self._trailers = []
        self._project_files = []

    def reset_form(self):
        self.id = -1

        self.title = 'Unnamed'
        self.day_index = datetime.datetime.now().day - 1
        self.month_index = datetime.datetime.now().month - 1
        self.year_index = datetime.datetime.now().year - AppLogic.BASE_YEAR
        self.coming_soon = True
        self.short_description = ''
        self.long_description = ''
        self.price = "0"

    def reset_files(self):
        self.header = ''
        self.screenshots = []
        self.capsule = ''
        self.trailers = []
        self.project_files = []

    @Slot(int)
    def map(self, game_id: int):
        reply = self._auth_service.authorized_session.get(GAMES_URL + f'{str(game_id)}/')

        if reply.status_code == requests.codes.ok:
            data = reply.json()

            self.id = data['id']

            self.title = data['title']
            self.short_description = data['short_description']
            self.long_description = data['long_description']
            self.price = str(data['price'])

            if data['release_date'] is None:
                self.coming_soon = True
            else:
                self.coming_soon = False
                date = datetime.datetime.fromtimestamp(data['release_date'])
                self.day_index = date.day
                self.month_index = date.month
                self.year_index = date.year - self.BASE_YEAR

            self.title_changed.emit()
            self.price_changed.emit()
            self.short_description_changed.emit()
            self.long_description_changed.emit()
            self.day_index_changed.emit()
            self.month_index_changed.emit()
            self.year_index_changed.emit()
            self.coming_soon_changed.emit()

    @Slot()
    def update(self):
        data = {
            "title": self._title,
            "short_description": self._short_description,
            "long_description": self._long_description,
            "price": float(self._price),
            "age_category_id": 1
        }

        if not self._coming_soon:
            release_date = datetime.datetime(
                day=self._day_index,
                month=self._month_index,
                year=self._year_index + self.BASE_YEAR).timestamp()
            data["release_date"] = release_date
        else:
            data["release_date"] = None

        reply = self._auth_service.authorized_session.put(
            GAMES_URL + f'{str(self.id)}/',
            json=data
        )

        if self._header != '':
            filename = QUrl(self._header).toLocalFile()
            with open(filename, 'rb') as header_file:
                files = [('file', (os.path.basename(filename), header_file))]
                url = GAMES_URL + f"{reply.json()['id']}" + '/header/'
                self._auth_service.authorized_session.post(url, files=files)

        if self._capsule != '':
            filename = QUrl(self._capsule).toLocalFile()
            with open(filename, 'rb') as capsule_file:
                files = [('file', (os.path.basename(filename), capsule_file))]
                url = GAMES_URL + f"{reply.json()['id']}" + '/capsule/'
                self._auth_service.authorized_session.post(url, files=files)

        if self._screenshots:
            files = []
            for screenshot in self._screenshots:
                filename = QUrl(screenshot).toLocalFile()
                files.append(
                    (
                        'files', (os.path.basename(filename), open(filename, 'rb'))
                    )
                )
            url = GAMES_URL + f"{reply.json()['id']}" + '/screenshots/'
            self._auth_service.authorized_session.post(url, files=files)

        if self._trailers:
            files = []
            for trailer in self._trailers:
                filename = QUrl(trailer).toLocalFile()
                files.append(
                    (
                        'files', (os.path.basename(filename), open(filename, 'rb'))
                    )
                )
            url = GAMES_URL + f"{reply.json()['id']}" + '/trailers/'
            self._auth_service.authorized_session.post(url, files=files)

        if self._project_files:
            files = []
            for build_file in self._project_files:
                filename = QUrl(build_file).toLocalFile()
                files.append(
                    (
                        'files', (os.path.basename(filename), open(filename, 'rb'))
                    )
                )
            url = GAMES_URL + f"{reply.json()['id']}" + '/builds/'
            self._auth_service.authorized_session.post(url, files=files)

        if reply.status_code == requests.codes.ok:
            self.reset_files()

    @Slot()
    def draft_new(self):
        self.reset_form()

        # TODO: need to get available age categories
        data = {
            "title": self._title,
            "short_description": self._short_description,
            "long_description": self._long_description,
            "price": float(self._price),
            "release_date": None,
            "age_category_id": 1
        }

        reply = self._auth_service.authorized_session.post(
            GAMES_URL,
            json=data
        )
        if reply.status_code == requests.codes.ok:
            self.id = reply.json()["id"]
            self.drafted.emit()

    def get_possible_years(self):
        base = AppLogic.BASE_YEAR
        current_year = datetime.datetime.now().year
        years_into_future = 10
        years = [i + base for i in range(current_year - base + years_into_future)]
        return years

    id = Property(int,
                  lambda self: self._id,
                  lambda self, value: setattr(self, '_id', value),
                  notify=id_changed)

    title = Property(str,
                     lambda self: self._title,
                     lambda self, value: setattr(self, '_title', value),
                     notify=title_changed)
    price = Property(str,
                     lambda self: self._price,
                     lambda self, value: setattr(self, '_price', value),
                     notify=price_changed)
    short_description = Property(str,
                                 lambda self: self._short_description,
                                 lambda self, value: setattr(self, '_short_description', value),
                                 notify=short_description_changed)
    long_description = Property(str,
                                lambda self: self._long_description,
                                lambda self, value: setattr(self, '_long_description', value),
                                notify=long_description_changed)

    day_index = Property(int,
                         lambda self: self._day_index,
                         lambda self, value: setattr(self, '_day_index', value),
                         notify=day_index_changed)
    month_index = Property(int,
                           lambda self: self._month_index,
                           lambda self, value: setattr(self, '_month_index', value),
                           notify=month_index_changed)
    year_index = Property(int,
                          lambda self: self._year_index,
                          lambda self, value: setattr(self, '_year_index', value),
                          notify=year_index_changed)
    coming_soon = Property(int,
                           lambda self: self._coming_soon,
                           lambda self, value: setattr(self, '_coming_soon', value),
                           notify=coming_soon_changed)

    possible_days = Property(list, lambda self: [_ for _ in range(1, 32)], constant=True)
    possible_months = Property(list, lambda self: [_ for _ in range(1, 13)], constant=True)
    possible_years = Property(list, lambda self: self.get_possible_years(), constant=True)

    @Property(str, notify=displayed_header_changed)
    def displayed_header(self):
        return Path(QUrl(self._header).toLocalFile()).name

    @Property(str, notify=header_changed)
    def header(self):
        return self._header

    @header.setter
    def header(self, new_value: str):
        if self._header != new_value:
            self._header = new_value
            self.header_changed.emit()
            self.displayed_header_changed.emit()

    @Property(str, notify=displayed_capsule_changed)
    def displayed_capsule(self):
        return Path(QUrl(self._capsule).toLocalFile()).name

    @Property(str, notify=capsule_changed)
    def capsule(self):
        return self._capsule

    @capsule.setter
    def capsule(self, new_value: str):
        if self._capsule != new_value:
            self._capsule = new_value
            self.capsule_changed.emit()
            self.displayed_capsule_changed.emit()

    @Property(str, notify=displayed_screenshots_changed)
    def displayed_screenshots(self):
        if self._screenshots:
            first_file = Path(QUrl(self._screenshots[0]).toLocalFile()).name
            amount = len(self._screenshots) - 1

            if amount:
                return f'{first_file} and {amount} more'
            else:
                return f'{first_file}'

    @Property(list, notify=screenshots_changed)
    def screenshots(self):
        return self._screenshots

    @screenshots.setter
    def screenshots(self, new_value: list):
        if self._screenshots != new_value:
            self._screenshots = new_value
            self.screenshots_changed.emit()
            self.displayed_screenshots_changed.emit()

    @Property(str, notify=displayed_trailers_changed)
    def displayed_trailers(self):
        if self._trailers:
            first_file = Path(QUrl(self._trailers[0]).toLocalFile()).name
            amount = len(self._trailers) - 1

            if amount:
                return f'{first_file} and {amount} more'
            else:
                return f'{first_file}'

    @Property(list, notify=trailers_changed)
    def trailers(self):
        return self._trailers

    @trailers.setter
    def trailers(self, new_value: list):
        if self._trailers != new_value:
            self._trailers = new_value
            self.trailers_changed.emit()
            self.displayed_trailers_changed.emit()

    project_files = Property(list,
                             lambda self: self._project_files,
                             lambda self, value: setattr(self, '_project_files', value),
                             notify=project_files_changed)
