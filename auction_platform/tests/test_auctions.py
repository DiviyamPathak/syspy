
import datetime
import unittest

from auction_platform.auctions.english_auction import EnglishAuction
from auction_platform.auctions.first_price_sealed_bid import \
    FirstPriceSealedBidAuction
from auction_platform.auctions.second_price_sealed_bid import \
    SecondPriceSealedBidAuction
from auction_platform.models.bid import Bid
from auction_platform.models.item import Item
from auction_platform.models.user import User


class TestAuctions(unittest.TestCase):
    def setUp(self):
        self.item = Item("Test Item", "A description")
        self.user1 = User("Alice")
        self.user2 = User("Bob")
        self.user3 = User("Charlie")
        self.now = datetime.datetime.now()
        self.end_time = self.now + datetime.timedelta(days=1)

    def test_first_price_sealed_bid_auction(self):
        auction = FirstPriceSealedBidAuction(
            self.item, self.now, self.end_time, reserve_price=50
        )
        auction.place_bid(Bid(self.user1, 100))
        auction.place_bid(Bid(self.user2, 120))
        auction.close()
        self.assertEqual(auction.winner, self.user2)
        self.assertEqual(auction.winning_price, 120)

    def test_first_price_sealed_bid_auction_no_winner(self):
        auction = FirstPriceSealedBidAuction(
            self.item, self.now, self.end_time, reserve_price=150
        )
        auction.place_bid(Bid(self.user1, 100))
        auction.place_bid(Bid(self.user2, 120))
        auction.close()
        self.assertIsNone(auction.winner)

    def test_second_price_sealed_bid_auction(self):
        auction = SecondPriceSealedBidAuction(
            self.item, self.now, self.end_time, reserve_price=50
        )
        auction.place_bid(Bid(self.user1, 100))
        auction.place_bid(Bid(self.user2, 120))
        auction.close()
        self.assertEqual(auction.winner, self.user2)
        self.assertEqual(auction.winning_price, 100)

    def test_english_auction(self):
        auction = EnglishAuction(self.item, self.now, self.end_time, reserve_price=50)
        auction.place_bid(Bid(self.user1, 100))
        auction.place_bid(Bid(self.user2, 120))
        with self.assertRaises(ValueError):
            auction.place_bid(Bid(self.user3, 110))
        auction.close()
        self.assertEqual(auction.winner, self.user2)
        self.assertEqual(auction.winning_price, 120)


if __name__ == "__main__":
    unittest.main()
