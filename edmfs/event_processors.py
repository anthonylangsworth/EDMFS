from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, StarSystem,PilotState, GalaxyState
from .event_summaries import RedeemVoucherEventSummary

class EventProcessor(ABC):
    @property
    @abstractmethod
    def eventName(self) -> str:
        #TODO: Make this a list, in case one event processor handles multiple event types
        pass

    @abstractmethod
    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        pass

# Also used for FSDJump. They have the same
class LocationEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "Location"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        if "Factions" in event.keys():
            galaxy_state.systems[event["SystemAddress"]] = StarSystem(event["StarSystem"], event["SystemAddress"], [faction["Name"] for faction in event["Factions"]])

        if "Docked" in event.keys() and event["Docked"]:
            pilot_state.last_docked_station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])

        return []

class DockedEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "Docked"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])
        pilot_state.last_docked_station = station
        return []

class RedeemVoucherEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "RedeemVoucher"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        result = []        
        try:
            star_system = galaxy_state.systems[pilot_state.last_docked_station.system_address]
            system_name = star_system.name
            system_minor_factions = star_system.minor_factions
        except:
            system_name = "unknown"
            system_minor_factions = []

        if event["Type"] == "bounty":
            for x in event["Factions"]:
                if x["Faction"] == minor_faction:
                    result.append(RedeemVoucherEventSummary(system_name, True, event["Type"], x["Amount"]))
                elif x["Faction"] in system_minor_factions:
                    result.append(RedeemVoucherEventSummary(system_name, False, event["Type"], x["Amount"]))
        elif event["Type"] == "CombatBond":
            if event["Faction"] == minor_faction:
                result.append(RedeemVoucherEventSummary(system_name, True, event["Type"], event["Amount"]))
            elif event["Faction"] in system_minor_factions:
                result.append(RedeemVoucherEventSummary(system_name, False, event["Type"], event["Amount"]))
        elif event["Type"] == "scannable":
            if pilot_state.last_docked_station.controlling_minor_faction == minor_faction:
                result.append(RedeemVoucherEventSummary(system_name, True, event["Type"], event["Amount"]))
            elif pilot_state.last_docked_station.controlling_minor_faction in system_minor_factions:
                result.append(RedeemVoucherEventSummary(system_name, False, event["Type"], event["Amount"]))
        return result
    
# Module non-public
# TODO: move this to an IoC setup
_default_event_processors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "FSDJump": LocationEventProcessor(),
    "Docked": DockedEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor()
}

#_this = sys.modules[__name__]

