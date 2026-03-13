
from auction_platform.auctions.base_auction import BaseAuction
from auction_platform.models.bid import Bid


class EnglishAuction(BaseAuction):
    def place_bid(self, bid: Bid):
        if self.bids:
            highest_bid = max(self.bids, key=lambda b: b.amount)
            if bid.amount <= highest_bid.amount:
                raise ValueError(
                    f"Bid must be higher than the current highest bid of {highest_bid.amount}"
                )
        super().place_bid(bid)

    def determine_winner(self) -> None:
        if not self.bids:
            return

        highest_bid = max(self.bids, key=lambda bid: bid.amount)
        if highest_bid.amount >= self.reserve_price:
            self.winner = highest_bid.bidder
            self.winning_price = highest_bid.amount
