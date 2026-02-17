import csv
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def export_hashtags_to_csv(filename="trending_export.csv"):
    hashtags = r.zrevrange("ranking:hashtags", 0, -1)

    if not hashtags:
        print("No data to export.")
        return

    rows = []

    for hashtag in hashtags:
        likes = int(r.hget(f"hashtag:{hashtag}", "likes") or 0)
        comments = int(r.hget(f"hashtag:{hashtag}", "comments") or 0)
        count = int(r.hget(f"hashtag:{hashtag}", "count") or 0)

        global_score = int(r.zscore("ranking:hashtags", hashtag) or 0)
        score_24h = int(r.zscore("ranking:hashtags:24h", hashtag) or 0)

        rows.append({
            "hashtag": hashtag,
            "likes": likes,
            "comments": comments,
            "count": count,
            "global_score": global_score,
            "score_24h": score_24h,
        })

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["hashtag", "likes", "comments", "count", "global_score", "score_24h"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} hashtags to {filename}")


if __name__ == "__main__":
    export_hashtags_to_csv()