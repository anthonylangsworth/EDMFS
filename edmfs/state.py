from typing import Dict

class StarSystemState:
    def __init__(self, name:str, address:int, minor_factions:tuple):
        self._name = name
        self._address = address
        self._minor_factions = minor_factions

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address

    @property
    def minor_factions(self) -> str:
        return self._minor_factions

class Station:
    def __init__(self, name:str, system_address:int, controlling_minor_faction:str):
        self._name:str = name
        self._system_address:int = system_address
        self._controlling_minor_faction:str = controlling_minor_faction

    @property
    def name(self) -> str:
        return self._name

    @property
    def system_address(self) -> int:
        return self._system_address

    @property
    def controlling_minor_faction(self) -> str:
        return self._controlling_minor_faction

    def __eq__ (self, other) -> bool:
        if not isinstance(other, Station):
            return NotImplemented

        return self._name == other._name \
            and self._controlling_minor_faction == other._controlling_minor_faction

class GalaxyState:
    def __init__(self):
        self._systems:Dict[int, StarSystemState] = {}

    @property
    def systems(self) -> list:
        return self._systems

class PilotState:
    def __init__(self):
        self._last_docked_station:Station = None
        self._missions:list = []

    @property
    def last_docked_station(self) -> Station:
        return self._last_docked_station

    @last_docked_station.setter
    def last_docked_station(self, value:Station) -> None:
        self._last_docked_station = value

    @property
    def missions(self) -> list:
        return self._missions

