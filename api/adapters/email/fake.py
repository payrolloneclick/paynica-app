from .generic import AbstractEmailAdapter


class FakeEmailAdapter(AbstractEmailAdapter):
    def __init__(self) -> None:
        self._emails = []

    async def clean(self) -> None:
        self._emails = []

    async def send(self, email: str, subject: str, body: str) -> None:
        self._emails.append({"email": email, "subject": subject, "body": body})
