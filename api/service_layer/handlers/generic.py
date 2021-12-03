from typing import Union

from domain.commands.generic import AbstractCommand
from domain.events.generic import AbstractEvent

AbstractMessage = Union[AbstractCommand, AbstractEvent]
