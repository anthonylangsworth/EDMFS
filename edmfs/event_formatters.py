from abc import abstractmethod, ABC
from itertools import groupby, accumulate
from typing import Dict, List, Iterable
import operator

from .event_summaries import EventSummary

class EventFormatter(ABC):
    @abstractmethod
    def process(self, event_summaries: Iterable[EventSummary]) -> List[str]:
        pass


class RedeemVoucherEventFormatter(EventFormatter):
    def process(self, event_summaries: Iterable[EventSummary]) -> List[str]:
        result = []
        redeem_voucher_order = (
            "bounty",
            "CombatBond"
        )      
        voucher_type_lookup:Dict[str, str] = {
            #"scannable" : "Scan Data",
            "bounty" : "Bounty Vouchers",
            "CombatBond" : "Combat Bonds"
        }          
        for voucher_type, event_summaries_by_type in groupby(sorted(event_summaries, key=lambda x: redeem_voucher_order.index(x.voucher_type)), key=lambda x: x.voucher_type):
            result.append(f"{sum(map(lambda es: es.amount, event_summaries_by_type)):,} CR of {voucher_type_lookup.get(voucher_type, voucher_type)}")
        return result


class SellExplorationDataEventFormatter(EventFormatter):
    def process(self, event_summaries: Iterable[EventSummary]) -> List[str]:
        return [f"{sum(map(lambda es: es.amount, event_summaries)):,} CR of Cartography Data",]


class MarketSellEventFormatter(EventFormatter):
    def process(self, event_summaries: Iterable[EventSummary]) -> List[str]:
        total_sell_price = 0
        total_buy_price = 0
        total_count = 0
        for event_summary in event_summaries:
            total_sell_price += event_summary.sell_price_per_unit * event_summary.count
            total_buy_price += event_summary.average_buy_price_per_unit * event_summary.count
            total_count += event_summary.count
        return [f"{total_count:,} T trade at {(total_sell_price - total_buy_price) / total_count:,.0f} CR average profit per T",]


class MissionCompletedEventFormatter(EventFormatter):
    def process(self, event_summaries: Iterable[EventSummary]) -> List[str]:
        result = []
        for influence, mission_completed_events in groupby(sorted(event_summaries, key=lambda x: x.influence), key=lambda x: x.influence):
            result.append(f"{len(list(mission_completed_events))} INF{influence} mission(s)")
        return result


class MissionFailedEventFormatter(EventFormatter):
    def process(self, event_summaries:Iterable[EventSummary]) -> List[str]:
        return [f"{len(list(event_summaries))} failed mission(s)"]
    

class MurderEventFormatter(EventFormatter):
    def process(self, event_summaries:Iterable[EventSummary]) -> List[str]:
        return [f"{len(list(event_summaries))} clean ship kill(s)"]
    

_default_event_formatters:Dict[str, EventFormatter] = {
    "RedeemVoucherEventSummary" : RedeemVoucherEventFormatter(),
    "SellExplorationDataEventSummary" : SellExplorationDataEventFormatter(),
    "MarketSellEventSummary": MarketSellEventFormatter(),
    "MissionCompletedEventSummary": MissionCompletedEventFormatter(),
    "MissionFailedEventSummary": MissionFailedEventFormatter(),
    "MurderEventSummary": MurderEventFormatter()
}
