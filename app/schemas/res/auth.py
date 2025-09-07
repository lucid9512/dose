
from app.schemas.__base__ import VaModelRes


class RefreshResponse(VaModelRes):
    refresh_token: str