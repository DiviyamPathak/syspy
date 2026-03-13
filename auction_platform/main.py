
import datetime

from auction_platform.auctions.english_auction import EnglishAuction
from auction_platform.auctions.first_price_sealed_bid import \
    FirstPriceSealedBidAuction
from auction_platform.auctions.second_price_sealed_bid import \
    SecondPriceSealedBidAuction
from auction_platform.models.bid import Bid
from auction_platform.models.item import Item
from auction_platform.models.user import User

auctions = []
users = []


def create_auction():
    print("Creating a new auction...")
    item_name = input("Enter item name: ")
    item_description = input("Enter item description: ")
    item = Item(item_name, item_description)

    start_price = float(input("Enter start price: "))
    reserve_price = float(input("Enter reserve price: "))

    print("Select auction type:")
    print("1. First-Price Sealed-Bid")
    print("2. Second-Price Sealed-Bid (Vickrey)")
    print("3. English Auction")
    auction_type = input("Enter your choice: ")

    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(days=1)

    if auction_type == "1":
        auction = FirstPriceSealedBidAuction(
            item, now, end_time, start_price, reserve_price
        )
    elif auction_type == "2":
        auction = SecondPriceSealedBidAuction(
            item, now, end_time, start_price, reserve_price
        )
    elif auction_type == "3":
        auction = EnglishAuction(item, now, end_time, start_price, reserve_price)
    else:
        print("Invalid auction type.")
        return

    auctions.append(auction)
    print("Auction created successfully!")


def list_auctions():
    print("Available auctions:")
    for i, auction in enumerate(auctions):
        print(f"{i + 1}. {auction}")


def place_bid():
    list_auctions()
    auction_choice = int(input("Select an auction to bid on: "))
    auction = auctions[auction_choice - 1]

    user_name = input("Enter your name: ")
    user = next((u for u in users if u.name == user_name), None)
    if not user:
        user = User(user_name)
        users.append(user)

    amount = float(input("Enter your bid amount: "))
    bid = Bid(user, amount)

    try:
        auction.place_bid(bid)
        print("Bid placed successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def close_auction():
    list_auctions()
    auction_choice = int(input("Select an auction to close: "))
    auction = auctions[auction_choice - 1]

    auction.close()
    if auction.winner:
        print(
            f"Auction closed! Winner is {auction.winner} with a price of {auction.winning_price}"
        )
    else:
        print("Auction closed! No winner.")


def main():
    while True:
        print("\nWelcome to the Auction Platform!")
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

def run_demonstration():
    print("--- Running Auction Demonstration ---")

    # 1. Create users
    user1 = User("Alice")
    user2 = User("Bob")
    user3 = User("Charlie")
    users.extend([user1, user2, user3])
    print(f"Users: {[user.name for user in users]}")

    # 2. Create a First-Price Sealed-Bid auction
    item = Item("Vintage Painting", "A beautiful painting from the 19th century.")
    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(minutes=5)
    auction = FirstPriceSealedBidAuction(item, now, end_time, reserve_price=100)
    auctions.append(auction)
    print(f"\nCreated Auction: {auction}")

    # 3. Place bids
    print("\nPlacing bids...")
    bid1 = Bid(user1, 110)
    bid2 = Bid(user2, 150)
    bid3 = Bid(user3, 130)
    auction.place_bid(bid1)
    print(f"- {bid1}")
    auction.place_bid(bid2)
    print(f"- {bid2}")
    auction.place_bid(bid3)
    print(f"- {bid3}")

    # 4. Close the auction and determine the winner
    print("\nClosing auction...")
    auction.close()

    # 5. Print the results
    if auction.winner:
        print(
            f"\nAuction for '{auction.item.name}' has ended."
            f"\nWinner: {auction.winner.name}"
            f"\nWinning Price: ${auction.winning_price:.2f}"
        )
    else:
        print(f"\nAuction for '{auction.item.name}' has ended with no winner (reserve price not met).")

    print("\n--- Demonstration Finished ---")


if __name__ == "__main__":
    main() # Keep the interactive main function for future use
    # run_demonstration()
