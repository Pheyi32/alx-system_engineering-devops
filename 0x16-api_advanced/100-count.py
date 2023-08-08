#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    if not subreddit or not word_list:
        return

    base_url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "100-count.py"}  # Add a user agent to avoid 429 error

    if after:
        params = {"after": after}
    else:
        params = {}

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data.get("data", {}).get("children", [])

        for post in posts:
            title = post["data"]["title"].lower()

            for keyword in word_list:
                keyword_lower = keyword.lower()
                if keyword_lower in title:
                    word_count[keyword_lower] = word_count.get(keyword_lower, 0) + title.count(keyword_lower)

        after = data.get("data", {}).get("after")
        if after:
            count_words(subreddit, word_list, after, word_count)
        else:
            sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
            for keyword, count in sorted_word_count:
                print(f"{keyword}: {count}")
    else:
        print("")
	
# Example usage
subreddit = "programming"
word_list = ["python", "java", "javascript"]
count_words(subreddit, word_list)
