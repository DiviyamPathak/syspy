from .base_auction import BaseAuction
from ..models.bid import Bid
from ..models.item import Item

class EnglishAuction(BaseAuction):
    def __init__(
        self,
        item: Item,
        start_time: int,
        end_time: int,
        start_price: float = 0.0,
        reserve_price: float = 0.0,
    ):
        super().__init__(item, start_time, end_time, start_price, reserve_price)

    def place_bid(self, bid: Bid):
        if self.bids:
            highest_bid = self.bids[0]
            for b in self.bids:
                if b.amount > highest_bid.amount:
                    highest_bid = b
            
            if bid.amount <= highest_bid.amount:
                raise ValueError(
                    "Bid must be higher than the current highest bid of " + str(highest_bid.amount)
                )
        super().place_bid(bid)

    def determine_winner(self):
        if not self.bids:
            return

        highest_bid = self.bids[0]
        for bid in self.bids:
            if bid.amount > highest_bid.amount:
                highest_bid = bid
                
        if highest_bid.amount >= self.reserve_price:
            self.winner = highest_bid.bidder
            self.winning_price = highest_bid.amount
