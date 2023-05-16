from typing import Optional

from PySide6.QtCore import Slot

from common.api.v1.schemas.company import CompanyCreateSchema
from desktop.src.models.company import Company
from desktop.src.services.AuthService import AuthService
from desktop.src.settings import COMPANIES_URL


class CompanyService:
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service: AuthService = auth_service
        self.company: Optional[Company] = None

    def create(self, data: CompanyCreateSchema):
        return self._auth_service.authorized_session.post(COMPANIES_URL, json=data.dict())

    @Slot()
    def load_personal(self):
        params = {"owner_id": self._auth_service.current_user.id}
        response = self._auth_service.authorized_session.get(COMPANIES_URL, params=params)

        if response.ok:
            self.company = Company(**response.json()[0])
        else:
            self.company = None
