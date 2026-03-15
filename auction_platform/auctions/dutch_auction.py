from ..auctions.base_auction import BaseAuction
from ..models.bid import Bid
from ..models.item import Item
from ..models.user import User


class DutchAuction(BaseAuction):
    current_price: float

    def __init__(self, item: Item, start_time: int, end_time: int, start_price: float, reserve_price: float):
        super().__init__(item, start_time, end_time, start_price, reserve_price)
        self.current_price: float = start_price

    def place_bid(self, bid: Bid):
        if not self.is_open:
            raise ValueError("Auction is closed.")

        if bid.amount >= self.current_price:
            self.winner = bid.bidder
            self.winning_price = self.current_price
            self.is_open = False
        else:
            # In a real scenario, the price would be lowered over time.
            # For this simulation, we can just lower it with each bid.
            self.current_price -= (self.current_price - self.reserve_price) / 10.0

    def determine_winner(self):
        # The winner is determined as soon as a bid is accepted.
        pass
