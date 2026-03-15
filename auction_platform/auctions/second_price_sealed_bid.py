from ..auctions.base_auction import BaseAuction
from ..models.bid import Bid
from ..models.item import Item

class SecondPriceSealedBidAuction(BaseAuction):
    def __init__(
        self,
        item: Item,
        start_time: int,
        end_time: int,
        start_price: float = 0.0,
        reserve_price: float = 0.0,
    ):
        super().__init__(item, start_time, end_time, start_price, reserve_price)

    def determine_winner(self):
        if not self.bids:
            return

        if len(self.bids) == 1:
            highest_bid = self.bids[0]
            if highest_bid.amount >= self.reserve_price:
                self.winner = highest_bid.bidder
                self.winning_price = self.reserve_price
            return

        highest_bid = self.bids[0]
        second_highest_bid = self.bids[0]
        for i in range(1, len(self.bids)):
            bid = self.bids[i]
            if bid.amount > highest_bid.amount:
                second_highest_bid = highest_bid
                highest_bid = bid
            elif bid.amount > second_highest_bid.amount or highest_bid is second_highest_bid:
                second_highest_bid = bid

        if highest_bid.amount >= self.reserve_price:
            self.winner = highest_bid.bidder
            self.winning_price = second_highest_bid.amount
