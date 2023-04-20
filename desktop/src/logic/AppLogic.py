import datetime
import os

import requests
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl

from desktop.src.settings import GAMES_URL


class AppLogic(QObject):
    BASE_YEAR = 1958

    title_changed = Signal()
    developer_changed = Signal()
    publisher_changed = Signal()
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
    header_changed = Signal()
    capsule_changed = Signal()
    trailers_changed = Signal()
    project_files_changed = Signal()

    drafted = Signal()

    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self.id = -1
        self.is_approved = None

        self._title = 'Unnamed'
        self._developer = ''
        self._publisher = ''
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
        self.developer = ''
        self.publisher = ''
        self.short_description = ''
        self.long_description = ''
        self.price = "0"

    def reset_files(self):
        self.screenshots = []
        self.header = ''
        self.capsule = ''
        self.trailers = []
        self.project_files = []

    @Slot(int)
    def map(self, game_id: int):
        reply = requests.get(GAMES_URL + f'{str(game_id)}/',
                             headers={"Authorization": self._auth_service.session_id})

        if reply.status_code == requests.codes.ok:
            data = reply.json()

            self.id = data['id']

            self.title = data['title']
            self.developer = data['developer']
            self.publisher = data['publisher']
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
            self.developer_changed.emit()
            self.publisher_changed.emit()
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
            "developer": self._developer,
            "publisher": self._publisher,
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

        reply = requests.put(
            GAMES_URL + f'{str(self.id)}/',
            json=data,
            headers={"Authorization": self._auth_service.session_id}
        )

        if self._header != '':
            filename = QUrl(self._header).toLocalFile()
            with open(filename, 'rb') as header_file:
                files = [('file', (os.path.basename(filename), header_file))]
                url = GAMES_URL + f"{reply.json()['id']}" + '/assets/header/'
                requests.post(url, files=files, headers={"Authorization": self._auth_service.session_id})

        if self._capsule != '':
            filename = QUrl(self._capsule).toLocalFile()
            with open(filename, 'rb') as capsule_file:
                files = [('file', (os.path.basename(filename), capsule_file))]
                url = GAMES_URL + f"{reply.json()['id']}" + '/assets/capsule/'
                requests.post(url, files=files, headers={"Authorization": self._auth_service.session_id})

        if self._screenshots:
            files = []
            for screenshot in self._screenshots:
                filename = QUrl(screenshot).toLocalFile()
                files.append(
                    (
                        'files', (os.path.basename(filename), open(filename, 'rb'))
                    )
                )
            url = GAMES_URL + f"{reply.json()['id']}" + '/assets/screenshots/'
            requests.post(url, files=files, headers={"Authorization": self._auth_service.session_id})

        if self._trailers:
            files = []
            for trailer in self._trailers:
                filename = QUrl(trailer).toLocalFile()
                files.append(
                    (
                        'files', (os.path.basename(filename), open(filename, 'rb'))
                    )
                )
            url = GAMES_URL + f"{reply.json()['id']}" + '/assets/trailers/'
            requests.post(url, files=files, headers={"Authorization": self._auth_service.session_id})

        if self._project_files:
            files = []
            for build_file in self._project_files:
                filename = QUrl(build_file).toLocalFile()
                files.append(
                    (
                        'files', (os.path.basename(filename), open(filename, 'rb'))
                    )
                )
            url = GAMES_URL + f"{reply.json()['id']}" + '/assets/build/'
            requests.post(url, files=files, headers={"Authorization": self._auth_service.session_id})

        if reply.status_code == requests.codes.ok:
            self.reset_files()

    @Slot()
    def draft_new(self):
        self.reset_form()

        # TODO: need to get available age categories
        data = {
            "title": self._title,
            "developer": self._developer,
            "publisher": self._publisher,
            "short_description": self._short_description,
            "long_description": self._long_description,
            "price": float(self._price),
            "release_date": None,
            "age_category_id": 1
        }

        reply = requests.post(
            GAMES_URL,
            json=data,
            headers={"Authorization": self._auth_service.session_id}
        )
        if reply.status_code == requests.codes.ok:
            self.id = reply.json()["id"]
            self.drafted.emit()

    @Slot()
    def send_for_verification(self):
        reply = requests.post(
            GAMES_URL + f'{str(self.id)}/verify/',
            headers={"Authorization": self._auth_service.session_id}
        )

    @Slot()
    def publish(self):
        reply = requests.post(
            GAMES_URL + f'{str(self.id)}/publish/',
            json={"is_published": self.is_published},
            headers={"Authorization": self._auth_service.session_id}
        )

    def get_possible_years(self):
        base = AppLogic.BASE_YEAR
        current_year = datetime.datetime.now().year
        years_into_future = 10
        years = [i + base for i in range(current_year - base + years_into_future)]
        return years

    title = Property(str,
                     lambda self: self._title,
                     lambda self, value: setattr(self, '_title', value),
                     notify=title_changed)
    developer = Property(str,
                         lambda self: self._developer,
                         lambda self, value: setattr(self, '_developer', value),
                         notify=developer_changed)
    publisher = Property(str,
                         lambda self: self._publisher,
                         lambda self, value: setattr(self, '_publisher', value),
                         notify=publisher_changed)
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

    screenshots = Property(list,
                           lambda self: self._screenshots,
                           lambda self, value: setattr(self, '_screenshots', value),
                           notify=screenshots_changed)
    header = Property(str,
                      lambda self: self._header,
                      lambda self, value: setattr(self, '_header', value),
                      notify=header_changed)
    capsule = Property(str,
                       lambda self: self._capsule,
                       lambda self, value: setattr(self, '_capsule', value),
                       notify=capsule_changed)
    trailers = Property(list,
                        lambda self: self._trailers,
                        lambda self, value: setattr(self, '_trailers', value),
                        notify=trailers_changed)
    project_files = Property(list,
                             lambda self: self._project_files,
                             lambda self, value: setattr(self, '_project_files', value),
                             notify=project_files_changed)
