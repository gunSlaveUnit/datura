from common.api.v1.schemas.payments import PaymentCreateSchema
from desktop.src.services.AuthService import AuthService
from desktop.src.settings import PAYMENTS_URL, USERS_URL


class WalletService:
    def __init__(self, auth_service: AuthService):
        super().__init__()

        self._auth_service: AuthService = auth_service
        self.balance: float = 0.00

    def load(self):
        current_user_id = self._auth_service.current_user.id
        response = self._auth_service.authorized_session.get(USERS_URL + f'{current_user_id}/balance/')

        if response.ok:
            data = response.json()
            self.balance = data["balance"]

    def top_up(self, data: PaymentCreateSchema):
        response = self._auth_service.authorized_session.post(PAYMENTS_URL, json=data)
        self.load()
        return response
