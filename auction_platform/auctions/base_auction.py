from typing import List, Optional

from ..models.bid import Bid
from ..models.item import Item
from ..models.user import User


class BaseAuction:
    item: Item
    start_time: int
    end_time: int
    start_price: float
    reserve_price: float
    bids: List[Bid]
    is_open: bool
    winner: Optional[User]
    winning_price: float

    def __init__(
        self,
        item: Item,
        start_time: int,
        end_time: int,
        start_price: float = 0.0,
        reserve_price: float = 0.0,
    ):
        self.item: Item = item
        self.start_time: int = start_time
        self.end_time: int = end_time
        self.start_price: float = start_price
        self.reserve_price: float = reserve_price

        self.bids: List[Bid] = []
        self.is_open: bool = True
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

    def determine_winner(self):
        pass

    def __str__(self):
        return f"Auction for {self.item.name}"