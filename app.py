from event_producer import generate_events
from event_consumer import process_events
from analytics import print_top_n, print_top_n_24h, print_stats_for_hashtag
from export_csv import export_hashtags_to_csv
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def show_menu():
    print("\n------------------------------------")
    print(" REDIS SOCIAL MEDIA ANALYTICS SYSTEM")
    print("------------------------------------")

    print("\n--- DATA GENERATION ---")
    print("1 - Generate N random events")
    print("2 - Generate N events for specific hashtag")
    print("3 - Add single event manually")

    print("\n--- PROCESSING ---")
    print("4 - Process new events")

    print("\n--- ANALYTICS ---")
    print("5 - Show TOP N (global)")
    print("6 - Show TOP N (24h)")
    print("7 - Show hashtag statistics")
    print("8 - List all tracked hashtags")

    print("\n--- SYSTEM ---")
    print("9  - Reset 24h ranking")
    print("10 - Flush ALL data (DANGEROUS)")
    print("11 - Show system info")

    print("\n--- EXPORT ---")
    print("12 - Export hashtags to CSV")

    print("\n0 - Exit")


def main():
    while True:
        show_menu()
        choice = input("Select option: ")

        if choice == "1":
            try:
                n = int(input("How many random events to generate? "))
                if n <= 0:
                    print("Please enter a positive number.")
                else:
                    generate_events(n)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            from event_producer import add_event
            import random
            
            hashtag = input("Enter hashtag (e.g. #redis): ").strip()
            n = int(input("How many events? "))
            
            for _ in range(n):
                event_type = random.choice(["like", "comment"])
                user_id = random.randint(1, 20)
                add_event(event_type, hashtag, user_id)
            
            print(f"{n} events generated for {hashtag}.")

        elif choice == "3":
            event_type = input("Type (like/comment): ").strip()
            hashtag = input("Hashtag (e.g. #redis): ").strip()
            user_id = input("User ID: ").strip()
    
            from event_producer import add_event
            add_event(event_type, hashtag, user_id)
            print("Event added.")

        elif choice == "4":
            process_events()

        elif choice == "5":
            from analytics import print_top_n
            total = r.zcard("ranking:hashtags") # ZCARD ranking:hashtags - sprawdza ile elementów jest w ZSET "ranking:hashtags"

            if total == 0:
                print("No hashtags available.")
                continue

            print(f"There are currently {total} tracked hashtags.")

            while True:
                try:
                    n = int(input("How many top results? "))
                    if n > total:
                        print(f"Only {total} hashtags exist. Try again.")
                    elif n <= 0:
                        print("Please enter a positive number.")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")

            print_top_n(n)

        elif choice == "6":
            from analytics import print_top_n_24h

            total = r.zcard("ranking:hashtags:24h")

            if total == 0:
                print("No hashtags available(24h ranking expired or no events).")
                continue

            print(f"There are currently {total} tracked hashtags in 24h ranking.")

            while True:
                try:
                    n = int(input("How many top results? "))
                    if n > total:
                        print(f"Only {total} hashtags exist. Try again.")
                    elif n <= 0:
                        print("Please enter a positive number.")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")

            print_top_n_24h(n)

        elif choice == "7":
            hashtag = input("Enter hashtag (e.g. #redis): ").strip()
            print_stats_for_hashtag(hashtag)

        elif choice == "8":
            hashtags = r.zrevrange("ranking:hashtags", 0, -1)
            
            if not hashtags:
                print("No hashtags tracked yet.")
            else:
                print("\nTracked hashtags:")
                for tag in hashtags:
                    print("-", tag)
        elif choice == "9":
            confirm = input("Are you sure you want to reset 24h ranking? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                r.delete("ranking:hashtags:24h")
                print("24h ranking reset.")
            else:
                print("Operation cancelled.")

        elif choice == "10":
            print("\nDANGEROUS: This will delete ALL data from Redis!")
            confirm = input("Type 'DELETE' to confirm: ").strip()

            if confirm == "DELETE":
                r.flushall()
                print("All Redis data has been deleted.")
            else:
                print("Operation cancelled.")

        elif choice == "11":
            print("\n--- SYSTEM INFO ---")

            stream_length = r.xlen("stream:events") # XLEN stream:events - sprawdza ile eventów jest w streamie "stream:events"
            total_hashtags = r.zcard("ranking:hashtags") # ZCARD ranking:hashtags - sprawdza ile elementów jest w ZSET "ranking:hashtags"
            total_24h = r.zcard("ranking:hashtags:24h") # ZCARD ranking:hashtags:24h - sprawdza ile elementów jest w ZSET "ranking:hashtags:24h"
            ttl_24h = r.ttl("ranking:hashtags:24h") # TTL ranking:hashtags:24h - sprawdza czas życia klucza "ranking:hashtags:24h"
            last_processed = r.get("consumer:last_id") # GET consumer:last_id - pobiera ostatni przetworzony ID
            print(f"Total events in stream: {stream_length}")
            print(f"Tracked hashtags (global ranking): {total_hashtags}")
            print(f"Tracked hashtags (24h ranking): {total_24h}")
            print(f"24h ranking TTL: {ttl_24h} seconds")
            print(f"Last processed event ID: {last_processed}")

        elif choice == "12":

            filename = input("Enter file name (default: trending_export.csv): ").strip()
            if not filename:
                filename = "trending_export.csv"

            if not filename.endswith(".csv"):
                filename += ".csv"

            export_hashtags_to_csv(filename)

        elif choice == "0":
            print("Exiting application.")
            break

        else:
            print("Invalid option. Try again.")

        

        


if __name__ == "__main__":
    main()
