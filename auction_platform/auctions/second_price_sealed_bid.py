
from auction_platform.auctions.base_auction import BaseAuction


class SecondPriceSealedBidAuction(BaseAuction):
    def determine_winner(self) -> None:
        if not self.bids:
            return

        if len(self.bids) == 1:
            highest_bid = self.bids[0]
            if highest_bid.amount >= self.reserve_price:
                self.winner = highest_bid.bidder
                self.winning_price = self.reserve_price
            return

        sorted_bids = sorted(self.bids, key=lambda bid: bid.amount, reverse=True)
        highest_bid = sorted_bids[0]
        second_highest_bid = sorted_bids[1]

        if highest_bid.amount >= self.reserve_price:
            self.winner = highest_bid.bidder
            self.winning_price = second_highest_bid.amount
