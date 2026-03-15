from ..auctions.base_auction import BaseAuction
from ..models.item import Item


class FirstPriceSealedBidAuction(BaseAuction):
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

        highest_bid = self.bids[0]
        for bid in self.bids:
            if bid.amount > highest_bid.amount:
                highest_bid = bid
                
        if highest_bid.amount >= self.reserve_price:
            self.winner = highest_bid.bidder
            self.winning_price = highest_bid.amount
