import requests

from desktop.src.schemas.company import CompanyCreateSchema
from desktop.src.settings import COMPANIES_URL


class CompanyService:
    def __init__(self, auth_service):
        super().__init__()

        self._auth_service = auth_service
        self.company = None

    def new(self, data: CompanyCreateSchema):
        return self._auth_service.authorized_session.post(COMPANIES_URL, json=data.dict())

    def load_personal(self, current_user_id: int):
        params = {"owner_id": current_user_id}
        reply = self._auth_service.authorized_session.get(COMPANIES_URL, params=params)
        if reply.status_code == requests.codes.ok:
            self.company = reply.json()[0]
