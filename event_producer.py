import redis
import time
import random

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

HASHTAGS = ["#redis", "#python", "#nosql", "#ai", "#bigdata"]
EVENT_TYPES = ["like", "comment"]

def add_event(event_type, hashtag, user_id):
    event = {
        "type": event_type,
        "hashtag": hashtag,
        "user_id": str(user_id),
        "timestamp": str(int(time.time()))
    }

    r.xadd("stream:events", event) # XADD robi append do strumienia, a Redis automatycznie nadaje unikalny ID

def generate_events(n):
    for _ in range(n):
        event_type = random.choice(EVENT_TYPES) # losowy typ eventu (like/comment)
        hashtag = random.choice(HASHTAGS) # losowy hashtag z listy
        user_id = random.randint(1, 20) # losowy identyfikator użytkownika

        add_event(event_type, hashtag, user_id)

    print(f"{n} events generated!")

if __name__ == "__main__":
    generate_events(100)
