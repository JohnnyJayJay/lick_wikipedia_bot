import sys
import tweepy

from collections import namedtuple
from lib.constants import KEY_PATH

TwitterAuth = namedtuple(
    "TWITTER",
    ["consumer_key", "consumer_secret", "access_token", "access_token_secret"],
)


def createClient():
    TWITTER = getTwitterCredentials()
    auth = tweepy.OAuthHandler(TWITTER.consumer_key, TWITTER.consumer_secret)
    auth.set_access_token(TWITTER.access_token, TWITTER.access_token_secret)
    return tweepy.API(auth)


def getTwitterCredentials(keyfile=KEY_PATH):
    # TOODO: Use better config file format, better parsing logic
    try:
        with open(keyfile, "r") as f:
            keys = f.read()
    except Exception as e:
        sys.stderr.write(f"Exception fetching Twitter keys: {e}")
        sys.exit(1)

    keys = keys.split()
    keys = [key.strip() for key in keys]

    return TwitterAuth(
        consumer_key=keys[0],
        consumer_secret=keys[1],
        access_token=keys[2],
        access_token_secret=keys[3],
    )


def sendTweet(api, file):
    """Post an image to twitter.

    Args:
        image_path: String, path to image on disk to be posted to twitter
    Returns:
        tweepy.status object, contains response from twitter request
    """
    return api.update_with_media(filename=file.name, file=file)
