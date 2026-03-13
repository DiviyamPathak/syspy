
from auction_platform.auctions.base_auction import BaseAuction


class FirstPriceSealedBidAuction(BaseAuction):
    def determine_winner(self) -> None:
        if not self.bids:
            return

        highest_bid = max(self.bids, key=lambda bid: bid.amount)
        if highest_bid.amount >= self.reserve_price:
            self.winner = highest_bid.bidder
            self.winning_price = highest_bid.amount
