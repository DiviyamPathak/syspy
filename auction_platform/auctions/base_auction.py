
import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from auction_platform.models.bid import Bid
from auction_platform.models.item import Item
from auction_platform.models.user import User


class BaseAuction(ABC):
    def __init__(
        self,
        item: Item,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        start_price: float = 0.0,
        reserve_price: float = 0.0,
    ):
        self.item = item
        self.start_time = start_time
        self.end_time = end_time
        self.start_price = start_price
        self.reserve_price = reserve_price
        self.bids: List[Bid] = []
        self.is_open = True
        self.winner: Optional[User] = None
        self.winning_price: float = 0.0

    def place_bid(self, bid: Bid):
        if not self.is_open:
            raise ValueError("Auction is closed.")
        self.bids.append(bid)

    def close(self):
        if not self.bids:
            self.is_open = False
            return

        self.is_open = False
        self.determine_winner()

    @abstractmethod
    def determine_winner(self) -> None:
        raise NotImplementedError

    def __str__(self):
        return f"Auction for {self.item.name}"
