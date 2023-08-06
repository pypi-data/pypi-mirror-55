import enum
from typing import *

from typeguard import check_argument_types, typechecked

from pydatapack.mc.internal import MCCommand
from . import internal
from . import TargetType

__all__ = ['advancement', 'Bossbar', 'execute', 'msg', 'whisper', 'tell', 'say', 'summon', 'tp']


class advancement:
    class method(enum.Enum):
        only = enum.auto()
        until = enum.auto()
        from_ = enum.auto()
        through = enum.auto()
        everything = enum.auto()

    @staticmethod
    @typechecked
    def grant(target: Union[TargetType, str], method: method, advancement_name: Optional[str] = None,
              criterion: Optional[str] = None) -> MCCommand:
        return MCCommand(advancement, advancement.grant, target, method, advancement_name, criterion)

    @staticmethod
    @typechecked
    def revoke(target: Union[TargetType, str], method: method, advancement_name: Optional[str] = None,
               criterion: Optional[str] = None) -> MCCommand:
        return MCCommand(advancement, advancement.grant, target, method, advancement_name, criterion)


class Bossbar(MCCommand):
    def __init__(self, id: str):
        super().__init__()
        self.id = id

    @staticmethod
    @typechecked
    def list() -> MCCommand:
        return MCCommand(Bossbar, Bossbar.list)

    @typechecked
    def add(self, name: str) -> MCCommand:
        self._name = name
        self._color = "white"
        self._style = "progress"
        self._value = 0
        self._max = 100
        self._visible = True
        self._players = None

        return MCCommand(Bossbar, Bossbar.add, self.id, internal.json_parser(name))

    def _set(self, setting: str, value: Any) -> MCCommand:
        setattr(self, f"_{setting}", value)

        return MCCommand(Bossbar, Bossbar._set, self.id, setting, value)

    def _get(self, setting: str) -> Union[MCCommand, Any]:
        assert check_argument_types()
        value = getattr(self, f"_{setting}")
        if value:
            return value
        else:
            return MCCommand(Bossbar, Bossbar._get, self.id, setting)

    @typechecked
    def remove(self) -> MCCommand:
        return MCCommand(Bossbar, Bossbar.remove, self.id)

    @property
    @typechecked
    def name(self) -> str:
        try:
            return self._name
        except AttributeError:
            raise internal.InvalidCommandError("There is no 'bossbar get <id> name' command.")

    @name.setter
    @typechecked
    def name(self, name: str):
        self._set("name", name)

    @property
    @typechecked
    def color(self) -> str:
        try:
            return self._color
        except AttributeError:
            raise internal.InvalidCommandError("There is no 'bossbar get <id> color' command.")

    @color.setter
    @typechecked
    def color(self, color: str):
        self._set("color", color)

    @property
    @typechecked
    def style(self) -> str:
        try:
            return self._style
        except AttributeError:
            raise internal.InvalidCommandError("There is no 'bossbar get <id> style' command.")

    @style.setter
    @typechecked
    def style(self, style: str):
        self._set("style", style)

    @property
    @typechecked
    def value(self) -> int:
        return self._get("value")

    @value.setter
    @typechecked
    def value(self, value: int):
        self._set("value", value)

    @property
    def max(self) -> int:
        return self._get("max")

    @max.setter
    @typechecked
    def max(self, max: int):
        self._set("max", max)

    @property
    @typechecked
    def visible(self) -> bool:
        return self._get("visible")

    @visible.setter
    @typechecked
    def visible(self, visible: bool):
        self._set("visible", visible)

    @property
    @typechecked
    def players(self) -> str:
        return self._get("players")

    @players.setter
    @typechecked
    def players(self, players: str):
        self._set("players", players)


class execute:
    @staticmethod
    @internal.generic_command()
    def at(target: Union[TargetType, str]) -> MCCommand:
        assert check_argument_types()

    @staticmethod
    @internal.generic_command()
    def as_(target: Union[TargetType, str]) -> MCCommand:
        assert check_argument_types()


@internal.generic_command()
def msg(target: Union[TargetType, str], msg: str) -> MCCommand:
    assert check_argument_types()
whisper = msg
tell = msg


@internal.generic_command()
def say(msg: str) -> MCCommand:
    assert check_argument_types()


@internal.generic_command()
def summon(entity: str) -> MCCommand:
    assert check_argument_types()


@internal.generic_command()
def tp(*args) -> MCCommand:
    assert check_argument_types()
