from .generic import AbstractEmailAdapter


class FakeEmailAdapter(AbstractEmailAdapter):
    def __init__(self):
        self._emails = []

    async def send(self, email, subject, body):
        self._emails.append({"email": email, "subject": subject, "body": body})
