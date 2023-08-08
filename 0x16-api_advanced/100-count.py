#!/usr/bin/python3
"""A recursive function to count words in all hot posts of a given Reddit subreddit."""
import requests

def count_words(subreddit, word_list, after="",
                uniq_word_list=[], word_count={}):
    """
    Prints counts of given words found in hot posts of a given subreddit
    """

    """ Generate list of keywords from word_list """
    if len(uniq_word_list) == 0:
        for word in word_list:
            word = word.lower()
            uniq_word_list.append(word)

    """ Request """
    url = "https://www.reddit.com/r/{}/hot.json?after={}".\
        format(subreddit, after)
    resp = requests.get(url, headers={'User-agent': '100-count.py'},
                        allow_redirects=False)

    if resp.status_code != 200:
        return

    data = resp.json()

    """ Base """
    if "after" not in data["data"]:
        if not word_count:
            return

        keys = []
        values = sorted(list(word_count.values()), reverse=True)

        for value in values:
            for key in word_count.keys():
                if word_count[key] == value and key not in keys:
                    keys.append(key)

        for key in keys:
            print("{}: {}".format(key, word_count[key]))
        return

    posts = data["data"]["children"]

    """keywords in titles """
    for post in posts:
        title_words = post["data"]["title"].split(" ")
        title_words_small = [i.lower() for i in title_words]
        for word in uniq_word_list:
            if word in title_words_small:
                if word in word_count:
                    word_count[word] += title_words_small.count(word)
                else:
                    word_count[word] = title_words_small.count(word)
            else:
                continue

    return count_words(subreddit, word_list,
                       after=data["data"]["after"],
                       uniq_word_list=uniq_word_list,
                       word_count=word_count)
