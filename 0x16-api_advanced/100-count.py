import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    if not word_list:
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'limit': 100}
    if after:
        params['after'] = after

    response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
    data = response.json()

    if 'data' in data and 'children' in data['data']:
        children = data['data']['children']
        for child in children:
            title = child['data']['title'].lower()
            for word in word_list:
                if word.lower() in title:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

        if 'after' in data['data']:
            count_words(subreddit, word_list, after=data['data']['after'], word_count=word_count)
        else:
            sorted_words = sorted(word_count.keys(), key=lambda w: (-word_count[w], w))
            for word in sorted_words:
                print(f"{word}: {word_count[word]}")

if __name__ == "__main__":
    subreddit = input("Enter subreddit: ")
    word_list = input("Enter keywords (space-separated): ").split()
    count_words(subreddit, word_list)

