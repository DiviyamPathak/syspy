
from auction_platform.auctions.base_auction import BaseAuction
from auction_platform.models.bid import Bid
from auction_platform.models.user import User


class DutchAuction(BaseAuction):
    def __init__(self, item, start_time, end_time, start_price, reserve_price):
        super().__init__(item, start_time, end_time, start_price, reserve_price)
        self.current_price = start_price

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
            self.current_price -= (self.current_price - self.reserve_price) / 10

    def determine_winner(self) -> None:
        # The winner is determined as soon as a bid is accepted.
        pass
