import time
from typing import List, Optional

from auction_platform.auctions.base_auction import BaseAuction
from auction_platform.auctions.english_auction import EnglishAuction
from auction_platform.auctions.first_price_sealed_bid import FirstPriceSealedBidAuction
from auction_platform.auctions.second_price_sealed_bid import SecondPriceSealedBidAuction
from auction_platform.models.bid import Bid
from auction_platform.models.item import Item
from auction_platform.models.user import User

auctions: List[BaseAuction] = []
users: List[User] = []


def find_user(name: str) -> Optional[User]:
    for u in users:
        if u.name == name:
            return u
    return None


def create_auction():
    print("Creating a new auction...")

    item_name = input("Enter item name: ")
    item_description = input("Enter item description: ")

    item = Item(item_name, item_description)

    start_price = float(input("Enter start price: "))
    reserve_price = float(input("Enter reserve price: "))

    print("Select auction type:")
    print("1. First-Price Sealed-Bid")
    print("2. Second-Price Sealed-Bid")
    print("3. English Auction")

    auction_type = input("Enter your choice: ")

    now = int(time.time())
    end_time = now + 86400

    if auction_type == "1":
        auction1 = FirstPriceSealedBidAuction(
            item, now, end_time, start_price, reserve_price
        )
        auctions.append(auction1)

    elif auction_type == "2":
        auction2 = SecondPriceSealedBidAuction(
            item, now, end_time, start_price, reserve_price
        )
        auctions.append(auction2)

    elif auction_type == "3":
        auction3 = EnglishAuction(
            item, now, end_time, start_price, reserve_price
        )
        auctions.append(auction3)

    else:
        print("Invalid auction type.")
        return

    print("Auction created successfully!")


def list_auctions():

    print("Available auctions:")

    i = 0
    for auction in auctions:
        print(str(i + 1) + ". " + str(auction))
        i += 1


def place_bid():

    list_auctions()

    auction_choice = int(input("Select an auction to bid on: "))
    auction = auctions[auction_choice - 1]

    user_name = input("Enter your name: ")

    user = find_user(user_name)

    if user is None:
        user = User(user_name)
        users.append(user)

    amount = float(input("Enter your bid amount: "))

    bid = Bid(user, amount)

    try:
        auction.place_bid(bid)
        print("Bid placed successfully!")
    except ValueError as e:
        print("Error: " + str(e))


def close_auction():

    list_auctions()

    auction_choice = int(input("Select an auction to close: "))
    auction = auctions[auction_choice - 1]

    auction.close()

    if auction.winner is not None:
        print(
            "Auction closed! Winner is "
            + str(auction.winner)
            + " with a price of "
            + str(auction.winning_price)
        )
    else:
        print("Auction closed! No winner.")


def main():

    while True:

        print("")
        print("Welcome to the Auction Platform!")
        print("1. Create Auction")
        print("2. List Auctions")
        print("3. Place Bid")
        print("4. Close Auction")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_auction()

        elif choice == "2":
            list_auctions()

        elif choice == "3":
            place_bid()

        elif choice == "4":
            close_auction()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()