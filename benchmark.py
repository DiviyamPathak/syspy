import time
from typing import List

from auction_platform.auctions.base_auction import BaseAuction
from auction_platform.auctions.english_auction import EnglishAuction
from auction_platform.models.bid import Bid
from auction_platform.models.item import Item
from auction_platform.models.user import User

def run_benchmark(num_iterations: int):
    start_time = time.time()
    
    users: List[User] = []
    for i in range(100):
        users.append(User("User" + str(i)))

    auctions: List[BaseAuction] = []
    now = int(time.time())
    end_time = now + 86400

    # Create auctions
    for i in range(num_iterations):
        item = Item("Item" + str(i), "Description" + str(i))
        auction = EnglishAuction(item, now, end_time, 10.0, 50.0)
        auctions.append(auction)

    # Place bids
    for i in range(num_iterations):
        auction = auctions[i]
        for j in range(20):  # 20 bids per auction
            user = users[j % 100]
            bid = Bid(user, 15.0 + float(j * 5))
            auction.place_bid(bid)

    # Close auctions
    for i in range(num_iterations):
        auctions[i].close()
        
    end_time_exec = time.time()
    print("Processed " + str(num_iterations) + " auctions and " + str(num_iterations * 20) + " bids.")
    print("Completed in: " + str(end_time_exec - start_time) + " seconds")

if __name__ == "__main__":
    print("Starting benchmark...")
    run_benchmark(50000)