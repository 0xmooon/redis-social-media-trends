import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def print_top_n(n=5):
    print(f"\n----TOP {n} HASHTAGS. GLOBAL RANKING----")

    top = r.zrevrange("ranking:hashtags", 0, n-1, withscores=True) #ZREVRANGE ranking:hashtags 0 4 WITHSCORES

    if not top:
        print("No data available.")
        return

    for i, (hashtag, score) in enumerate(top, start=1):
        print(f"{i}. {hashtag} — {int(score)} points") 

    print("-----------------\n")

def print_top_n_24h(n=5):
    print(f"\n----TOP {n} HASHTAGS. 24H RANKING----")

    top = r.zrevrange("ranking:hashtags:24h", 0, n-1, withscores=True) #ZREVRANGE ranking:hashtags:24h 0 4 WITHSCORES

    if not top:
        print("No data available(24h ranking expired or no events).")
        return

    for i, (hashtag, score) in enumerate(top, start=1):
        print(f"{i}. {hashtag} — {int(score)} points") 

    print("-----------------\n")

def print_stats_for_hashtag(hashtag):
    print(f"\n---- STATISTICS FOR {hashtag} ----")

    likes = r.hget(f"hashtag:{hashtag}", "likes") or 0
    comments = r.hget(f"hashtag:{hashtag}", "comments") or 0
    count = r.hget(f"hashtag:{hashtag}", "count") or 0

    global_score = r.zscore("ranking:hashtags", hashtag) or 0
    score_24h = r.zscore("ranking:hashtags:24h", hashtag) or 0

    print(f"Likes: {int(likes)}")
    print(f"Comments: {int(comments)}")
    print(f"Total events: {int(count)}")
    print(f"Global score (weighted): {int(global_score)}")
    print(f"24h score (weighted): {int(score_24h)}")

    print("-----------------\n")


if __name__ == "__main__":
    print_top_5()
    print_top_5_24h()
    print_stats_for_hashtag("#redis")
