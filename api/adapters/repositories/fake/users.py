from typing import List, Optional

from api.domain.models.users import User

from .generic import AbstractFakeRepository


class UsersFakeRepository(AbstractFakeRepository):
    async def filter(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        phone_code: Optional[str] = None,
        email_code: Optional[str] = None,
        password_code: Optional[str] = None,
    ) -> List[User]:
        objs = filter(lambda o: o, self._objs)
        if email:
            objs = filter(lambda o: o.email == email, objs)
        if phone:
            objs = filter(lambda o: o.phone == phone, objs)
        if phone_code:
            objs = filter(lambda o: o.phone_code == phone_code, objs)
        if email_code:
            objs = filter(lambda o: o.phone_code == email_code, objs)
        if password_code:
            objs = filter(lambda o: o.password_code == password_code, objs)
        return [o for o in objs]
