import tweepy
import time
import ssl
import csv

# Authenticate to Twitter
auth = tweepy.OAuthHandler("H1W2BKZXkdaPqnSw3Dp9XayaV", "1WempwrnMoNwWgsNZKa3rojzNxayXn6oHBKvoK0nL65srA1Qjg")
auth.set_access_token("972006721316036608-rpevtyiHE6TDBooZZnWrs6cHxSvFaYj", "Vc3D3lDPU2Ph6gaHBivDdqo7TyF7HqApqekkgNLQXlNX6")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")

except:
    print("Error during authentication")

def update_status(status):
    api.update_status(status)


def get_user_info(user_name: str):
    user = api.get_user(screen_name=user_name)

    print("User details:")
    print(user.name)
    print(user.description)
    print(user.location)

    print("Last 20 Followers:")
    for follower in user.followers():
        print(follower.name)

    # user = api.create_friendship(screen_name=user_name)


def like_tweet(api):
    tweets = api.home_timeline(count=1)
    tweet = tweets[0]
    print(f"Liking tweet {tweet.id} of {tweet.author.name}")
    api.create_favorite(tweet.id)


ban_list = ['@Pickle_Bot_', 'Pickle_Bot_', 'score', 'penis', 'dick', 'cock', 'Score', 'sport', 'sports', 'in a pickle', 'game', 'Ukraine', "Ukraine's", 'Drone', 'Drones']
# followers_count = 0  # used to keep from going over max following per day (400)


def follow_based_on_public_tweets(api):
    for tweet in api.search(q="Pickle", lang="en", result_type="popular"):
        m = "Did someone say pickle?"  # pickle emoji unicode \U0001F952
        # if tweet.user.screen_name != "Pickle_Bot_":
        if "pickle" in tweet.user.screen_name or "Pickle" in tweet.user.screen_name:
            continue
        else:
            counter = 0
            for i in ban_list:
                if i in tweet.text:
                    counter += 1
            if counter == 0:
                try:
                    api.retweet(tweet.id)
                    print(f"retweeted: {tweet.user.screen_name}")
                    # api.create_friendship(screen_name=tweet.user.screen_name)
                    # print(f"followed: {tweet.user.screen_name}")
                    if tweet.id != int(api.verify_credentials().id_str):
                        print(f"responded to tweet: {tweet.user.screen_name}")
                        api.update_status(status = m, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)

                except:
                    continue
            else:
                continue


def follow_followers(api):
    for follower in tweepy.Cursor(api.get_followers).items():
        if not follower.following:
            print(f"Following {follower.name}")
        follower.follow()


def unfolllow_accounts_not_following_me(api):
    followers_list = []  # followers: users following specific account. friends: an account the user is following
    for follower in api.get_follower_ids(screen_name="Pickle_Bot_"):
        followers_list.append(follower)
    for friend in api.get_friend_ids(screen_name="Pickle_Bot_"):
        if friend not in followers_list:
            api.destroy_friendship(user_id=friend)


def reply_followers(api):
    for follower in api.home_timeline():
        print(follower)


while True:
    follow_based_on_public_tweets(api)
    time.sleep(15)

# unfolllow_accounts_not_following_me(api)




