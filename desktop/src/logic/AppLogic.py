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
    developer_changed = Signal()
    publisher_changed = Signal()
    price_changed = Signal()
    short_description_changed = Signal()
    long_description_changed = Signal()

    day_index_changed = Signal()
    month_index_changed = Signal()
    year_index_changed = Signal()
    coming_soon_changed = Signal()

    is_approved_changed = Signal()
    is_published_changed = Signal()

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

    drafted = Signal()

    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._is_approved = None

        self._title = 'Unnamed'
        self._developer = ""
        self._publisher = ""
        self._price = "0.00"
        self._short_description = ''
        self._long_description = ''

        self._day_index = datetime.datetime.now().day - 1
        self._month_index = datetime.datetime.now().month - 1
        self._year_index = datetime.datetime.now().year - AppLogic.BASE_YEAR
        self._coming_soon = True
        self._is_published = False

        self._screenshots = []
        self._header = ''
        self._capsule = ''
        self._trailers = []

        self._server_screenshots = ''
        self._server_header = ''
        self._server_capsule = ''
        self._server_trailers = ''

    # region Id

    @Property(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value: int):
        if self._id != new_value:
            self._id = new_value
            self.id_changed.emit()

    # endregion

    # region Title

    @Property(str, notify=title_changed)
    def title(self):
        return self._title

    @title.setter
    def title(self, new_value: str):
        if self._title != new_value:
            self._title = new_value
            self.title_changed.emit()

    @Property(str, notify=developer_changed)
    def developer(self):
        return self._developer

    @developer.setter
    def developer(self, new_value: str):
        if self._developer != new_value:
            self._developer = new_value
            self.developer_changed.emit()

    @Property(str, notify=publisher_changed)
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, new_value: str):
        if self._publisher != new_value:
            self._publisher = new_value
            self.publisher_changed.emit()

    # endregion

    # region Price

    @Property(str, notify=price_changed)
    def price(self):
        return self._price

    @price.setter
    def price(self, new_value: str):
        if self._price != new_value:
            self._price = new_value
            self.price_changed.emit()

    # endregion

    # region Short description

    @Property(str, notify=short_description_changed)
    def short_description(self):
        return self._short_description

    @short_description.setter
    def short_description(self, new_value: str):
        if self._short_description != new_value:
            self._short_description = new_value
            self.short_description_changed.emit()

    # endregion

    # region Long description

    @Property(str, notify=long_description_changed)
    def long_description(self):
        return self._long_description

    @long_description.setter
    def long_description(self, new_value: str):
        if self._long_description != new_value:
            self._long_description = new_value
            self.long_description_changed.emit()

    # endregion

    # region Day index

    @Property(int, notify=day_index_changed)
    def day_index(self):
        return self._day_index

    @day_index.setter
    def day_index(self, new_value: int):
        if self._day_index != new_value:
            self._day_index = new_value
            self.day_index_changed.emit()

    # endregion

    # region Month index

    @Property(int, notify=month_index_changed)
    def month_index(self):
        return self._month_index

    @month_index.setter
    def month_index(self, new_value: int):
        if self._month_index != new_value:
            self._month_index = new_value
            self.month_index_changed.emit()

    # endregion

    # region Year index

    @Property(int, notify=year_index_changed)
    def year_index(self):
        return self._year_index

    @year_index.setter
    def year_index(self, new_value: int):
        if self._year_index != new_value:
            self._year_index = new_value
            self.year_index_changed.emit()

    # endregion

    # region Coming soon

    @Property(bool, notify=coming_soon_changed)
    def coming_soon(self):
        return self._coming_soon

    @coming_soon.setter
    def coming_soon(self, new_value: bool):
        if self._coming_soon != new_value:
            self._coming_soon = new_value
            self.coming_soon_changed.emit()

    # endregion

    # region Is approved

    @Property(bool, notify=is_approved_changed)
    def is_approved(self):
        return self._is_approved

    @is_approved.setter
    def is_approved(self, new_value: bool):
        if self._is_approved != new_value:
            self._is_approved = new_value
            self.is_approved_changed.emit()

    # endregion

    # region Is published

    @Property(bool, notify=is_published_changed)
    def is_published(self):
        return self._is_published

    @is_published.setter
    def is_published(self, new_value: bool):
        if self._is_published != new_value:
            self._is_published = new_value
            self.is_published_changed.emit()

    # endregion

    def reset_form(self):
        self.id = -1
        self.is_approved = None

        self.title = 'Unnamed'
        self.developer = ''
        self.publisher = ''
        self.day_index = datetime.datetime.now().day - 1
        self.month_index = datetime.datetime.now().month - 1
        self.year_index = datetime.datetime.now().year - AppLogic.BASE_YEAR
        self.coming_soon = True
        self.is_published = False
        self.short_description = ''
        self.long_description = ''
        self.price = "0"

    def reset_files(self):
        self.header = ''
        self.screenshots = []
        self.capsule = ''
        self.trailers = []

    @Slot(int)
    def map(self, game_id: int):
        self.server_header = ''
        self.server_capsule = ''
        self.server_screenshots = ''
        self.server_trailers = ''

        response = self._auth_service.authorized_session.get(GAMES_URL + f'{str(game_id)}/')

        if response.ok:
            data = response.json()

            self.id = data['id']
            self.is_approved = data['is_approved']
            self.is_published = data['is_published']

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
                self.day_index = date.day - 1
                self.month_index = date.month - 1
                self.year_index = date.year - self.BASE_YEAR

            response = self._auth_service.authorized_session.get(GAMES_URL + f'{str(game_id)}/header/')
            if response.ok:
                content_disposition = response.headers['content-disposition']
                filename = content_disposition.split('=')[1]
                self.server_header = filename

            response = self._auth_service.authorized_session.get(GAMES_URL + f'{str(game_id)}/capsule/')
            if response.ok:
                content_disposition = response.headers['content-disposition']
                filename = content_disposition.split('=')[1]
                self.server_capsule = filename

            response = self._auth_service.authorized_session.get(GAMES_URL + f'{str(game_id)}/screenshots/')
            if response.ok:
                filenames = response.json()['filenames']
                if filenames:
                    first_file = filenames[0]
                    amount = len(filenames) - 1

                    if amount != 0:
                        self.server_screenshots = f'{first_file} and {amount} more'
                    else:
                        self.server_screenshots = f'{first_file}'

            response = self._auth_service.authorized_session.get(GAMES_URL + f'{str(game_id)}/trailers/')
            if response.ok:
                filenames = response.json()['filenames']
                if filenames:
                    first_file = filenames[0]
                    amount = len(filenames) - 1

                    if amount != 0:
                        self.server_trailers = f'{first_file} and {amount} more'
                    else:
                        self.server_trailers = f'{first_file}'

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
            # TODO: something wrong with indices
            release_date = datetime.datetime(
                day=self._day_index + 1,
                month=self._month_index + 1,
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

        if reply.status_code == requests.codes.ok:
            self.reset_files()
            self.map(self.id)

    @Slot()
    def send_for_verification(self):
        reply = self._auth_service.authorized_session.patch(
            GAMES_URL + f'{str(self.id)}/verify/',
            json={"is_send_for_verification": True}
        )

    @Slot()
    def publish(self):
        self._auth_service.authorized_session.patch(
            GAMES_URL + f'{str(self.id)}/publish/',
            json={"is_published": self.is_published}
        )

    @Slot()
    def draft_new(self):
        self.reset_form()
        self.reset_files()

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

    possible_days = Property(list, lambda self: [_ for _ in range(1, 32)], constant=True)
    possible_months = Property(list, lambda self: [_ for _ in range(1, 13)], constant=True)
    possible_years = Property(list, lambda self: self.get_possible_years(), constant=True)

    server_header_changed = Signal()

    @Property(str, notify=server_header_changed)
    def server_header(self):
        return self._server_header

    @server_header.setter
    def server_header(self, new_value: str):
        if self._server_header != new_value:
            self._server_header = new_value
            self.server_header_changed.emit()

    server_capsule_changed = Signal()

    @Property(str, notify=server_capsule_changed)
    def server_capsule(self):
        return self._server_capsule

    @server_capsule.setter
    def server_capsule(self, new_value: str):
        if self._server_capsule != new_value:
            self._server_capsule = new_value
            self.server_capsule_changed.emit()

    server_screenshots_changed = Signal()

    @Property(str, notify=server_screenshots_changed)
    def server_screenshots(self):
        return self._server_screenshots

    @server_screenshots.setter
    def server_screenshots(self, new_value: str):
        if self._server_screenshots != new_value:
            self._server_screenshots = new_value
            self.server_screenshots_changed.emit()

    server_trailers_changed = Signal()

    @Property(str, notify=server_trailers_changed)
    def server_trailers(self):
        return self._server_trailers

    @server_trailers.setter
    def server_trailers(self, new_value: str):
        if self._server_trailers != new_value:
            self._server_trailers = new_value
            self.server_trailers_changed.emit()

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
