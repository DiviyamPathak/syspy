
from auction_platform.models.user import User


class Bid:
    def __init__(self, bidder: User, amount: float):
        self.bidder = bidder
        self.amount = amount

    def __str__(self):
        return f"{self.bidder} bids {self.amount}"
