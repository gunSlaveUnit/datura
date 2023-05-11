import asyncio
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PySide6.QtCore import QObject, Slot, Signal, Property, QUrl

from desktop.src.settings import GAMES_URL, BUILDS_URL, PLATFORMS_URL
from server.src.core.models.platform import Platform
from server.src.core.utils.io import read_compressed_chunks, read_uncompressed_chunks


class BuildLogic(QObject):
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service

        self._id = -1
        self._version = ''
        self._call = ''
        self._params = ''
        self._platform_id = -1

        self._platforms = []
        self._selected_platform_index = 1

        self._project_archive = ''
        self._displayed_status = ''
        self._build_size_bytes = 0

    id_changed = Signal()
    version_changed = Signal()
    call_changed = Signal()
    params_changed = Signal()
    platform_id_changed = Signal()
    selected_platform_index_changed = Signal()
    project_archive_changed = Signal()
    displayed_status_changed = Signal()

    @Property(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value: int):
        if self._id != new_value:
            self._id = new_value
            self.id_changed.emit()

    @Property(str, notify=version_changed)
    def version(self):
        return self._version

    @version.setter
    def version(self, new_value: str):
        if self._version != new_value:
            self._version = new_value
            self.version_changed.emit()

    @Property(str, notify=call_changed)
    def call(self):
        return self._call

    @call.setter
    def call(self, new_value: str):
        if self._call != new_value:
            self._call = new_value
            self.call_changed.emit()

    @Property(str, notify=params_changed)
    def params(self):
        return self._params

    @params.setter
    def params(self, new_value: str):
        if self._params != new_value:
            self._params = new_value
            self.params_changed.emit()

    @Property(int, notify=platform_id_changed)
    def platform_id(self):
        return self._platform_id

    @platform_id.setter
    def platform_id(self, new_value: int):
        if self._platform_id != new_value:
            self._platform_id = new_value
            self.platform_id_changed.emit()

    @Property(int, notify=selected_platform_index_changed)
    def selected_platform_index(self):
        return self._selected_platform_index

    @selected_platform_index.setter
    def selected_platform_index(self, new_value: int):
        if self._selected_platform_index != new_value:
            self._selected_platform_index = new_value
            self.selected_platform_index_changed.emit()

    @Property(str, notify=project_archive_changed)
    def project_archive(self):
        return self._project_archive

    @project_archive.setter
    def project_archive(self, new_value: str):
        if self._project_archive != new_value:
            self._project_archive = new_value
            self.project_archive_changed.emit()

    @Property(str, notify=displayed_status_changed)
    def displayed_status(self):
        return self._displayed_status

    @displayed_status.setter
    def displayed_status(self, new_value: str):
        if self._displayed_status != new_value:
            self._displayed_status = new_value
            self.displayed_status_changed.emit()

    def reset_form(self):
        self.id = -1
        self.version = '1.0.0'
        self.call = ''
        self.params = ''
        self.platform_id = 1

    def upload(self):
        uploading_bytes_progress = 0
        filename = QUrl(self._project_archive).toLocalFile()
        base_path = Path(filename)
        url = BUILDS_URL + f"{self.id}" + '/files/'
        for file_path in base_path.glob("**/*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(base_path)
                for chunk in read_uncompressed_chunks(file_path):
                    self._auth_service.authorized_session.post(url, headers={"Content-Disposition": str(relative_path)}, data=chunk)
                    uploading_bytes_progress += len(chunk)
                    self.displayed_status = f"Uploading ... {(uploading_bytes_progress / self._build_size_bytes * 100):.2f}%"

        self.reset_files()

    def done(self, task):
        self.displayed_status = "Uploading done"

    def get_file_info(self, filepath: Path, base_path: Path):
        return {
            "size_bytes": filepath.stat().st_size,
            'rel_path': filepath.relative_to(base_path)
        }

    def files_info(self):
        filename = QUrl(self._project_archive).toLocalFile()
        base_path = Path(filename)
        futures = []
        pool = ThreadPoolExecutor(8)
        for file_path in base_path.glob("**/*"):
            if file_path.is_file():
                futures.append(pool.submit(self.get_file_info, file_path, base_path))

        self._build_size_bytes = sum([future.result()['size_bytes'] for future in futures])

    def collecting_size_done_callback(self, task):
        self.displayed_status = str(self._build_size_bytes)

    @Slot(int)
    def update(self, game_id: int):
        data = {
            "version": self._version,
            "call": self._call,
            "params": self._params,
            "game_id": game_id,
            "platform_id": self._selected_platform_index + 1,
        }

        response = self._auth_service.authorized_session.put(
            BUILDS_URL + f'{str(self.id)}/',
            json=data
        )

        if self._project_archive != '':
            self.displayed_status = "Collecting information about build ..."
            executor = ThreadPoolExecutor(1)
            future = executor.submit(self.files_info)
            future.add_done_callback(self.collecting_size_done_callback)
            self.displayed_status = "Uploading ... 0%"
            future = executor.submit(self.upload)
            future.add_done_callback(self.done)

    drafted = Signal()

    @Slot()
    def load_platforms(self):
        response = self._auth_service.authorized_session.get(PLATFORMS_URL)
        if response.ok:
            platforms = response.json()
            self._platforms = [Platform(**platform) for platform in platforms]
            self.platforms_changed.emit()

    platforms_changed = Signal()

    @Property(list, notify=platforms_changed)
    def displayed_platforms(self):
        return [platform.title for platform in self._platforms]

    @Slot(int)
    def draft_new(self, game_id: int):
        self.reset_form()

        data = {
            "version": self._version,
            "call": self._call,
            "params": None,
            "platform_id": 1,
            "game_id": game_id
        }

        response = self._auth_service.authorized_session.post(
            BUILDS_URL,
            json=data
        )
        if response.ok:
            self.id = response.json()["id"]
            self.drafted.emit()

    @Slot(int)
    def map(self, build_id: int):
        response = self._auth_service.authorized_session.get(BUILDS_URL + f'{build_id}/')

        if response.ok:
            data = response.json()

            self.id = data['id']
            self.version = data['version']
            self.call = data['call']
            self.params = data['params']
            self.platform_id = data['platform_id']
            self.selected_platform_index = data['platform_id'] - 1

    def reset_files(self):
        self.project_archive = ''
