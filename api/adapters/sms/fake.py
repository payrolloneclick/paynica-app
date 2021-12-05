from .generic import AbstractSmsAdapter


class FakeSmsAdapter(AbstractSmsAdapter):
    def __init__(self):
        self._sms = []

    async def clean(self) -> None:
        self._sms = []

    async def send(self, phone, sms):
        self._sms.append(
            {
                "phone": phone,
                "sms": sms,
            }
        )
