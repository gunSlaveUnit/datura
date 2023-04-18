import requests
from desktop.src.settings import COMPANIES_URL


class CompanyService():
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service
        self.company = None

    def create(self, data):
        headers = {"Authorization": self._auth_service.session_id}
        return requests.post(COMPANIES_URL, headers=headers, json=data)

    def load_personal(self):
        headers = {"Authorization": self._auth_service.session_id}
        params = {"owner_id": self._auth_service.current_user["id"]}
        reply = requests.get(COMPANIES_URL, headers=headers, params=params)
        if reply.status_code == requests.codes.ok:
            self.company = reply.json()[0]
