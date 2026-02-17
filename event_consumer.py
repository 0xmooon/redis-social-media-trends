import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "stream:events"
LAST_ID_KEY = "consumer:last_id"


def process_events():
    print("\nStarting event processing...")
    
    # events = r.xrange("stream:events", "-", "+") # Odczyt wszystkich eventów ze streamu

    # Pobierz ostatnio przetworzone ID
    last_id = r.get(LAST_ID_KEY)

    if last_id is None:
        print("No previous state found. Starting from beginning.")
        last_id = "0-0"
    else:
        print(f"Last processed ID: {last_id}")

    # Pobierz tylko nowe eventy
    events = r.xrange(STREAM_NAME, min=last_id, max="+")
    processed_count = 0

    for event_id, fields in events:
        # Pomiń event, jeśli to dokładnie ostatnie ID
        if event_id == last_id:
            continue
        print("Processing event:", event_id, fields)

        hashtag = fields["hashtag"] # Pobieramy hashtag z eventu

        # Zwiększamy licznik hashtagu (HASH)
        r.hincrby(f"hashtag:{hashtag}", "count", 1)

        if fields["type"] == "like":
            r.hincrby(f"hashtag:{hashtag}", "likes", 1)
            # Aktualizujemy ranking (Sorted Set) globalny
            r.zincrby("ranking:hashtags", 1, hashtag) # tworzy ZSET o nazwie "ranking:hashtags" i zwiększa o 1 wartość dla hashtagu
            r.zincrby("ranking:hashtags:24h", 1, hashtag) # Ranking trendów 24h

        elif fields["type"] == "comment":
            r.hincrby(f"hashtag:{hashtag}", "comments", 1)
            r.zincrby("ranking:hashtags", 2, hashtag) # komentarze są ważniejsze niż lajki, więc zwiększamy o 2
            r.zincrby("ranking:hashtags:24h", 2, hashtag) # Ranking trendów 24h


        # Ustaw TTL tylko jeśli klucz(czyli ZSET "ranking:hashtags:24h") jeszcze nie ma ustawionego czasu życia
        if r.ttl("ranking:hashtags:24h") == -1: # -1 klucz jest ale nie ma TTL, -2 klucz nie istnieje
            r.expire("ranking:hashtags:24h", 240)  # na test ustawimy 60 sekund


        # Zapisz ID jako ostatnio przetworzone
        r.set(LAST_ID_KEY, event_id)
        processed_count += 1

    if processed_count == 0:
        print("No new events to process.")
    else:
        print(f"Processed {processed_count} new events.")

    print("Processing finished!\n")

if __name__ == "__main__":
    process_events()