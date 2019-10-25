#!/usr/bin/env python3
import os
import sys
import time
import wikipedia

from lib.constants import BACKOFF, MAX_ATTEMPTS, MAX_STATUS_LEN, TIMEOUT_BACKOFF
from lib import images
from lib import twitter
from lib import words


def main():
    title = searchForLick(MAX_ATTEMPTS, BACKOFF)
    #logo = images.getLogo(title)
    status_text = "\n".join((title, words.getWikiUrl(title)))

    if len(status_text) > MAX_STATUS_LEN:
        status_text = title

    #_ = twitter.sendTweet(status_text, logo)


def searchForLick(attempts=MAX_ATTEMPTS, backoff=BACKOFF):
    """Loop MAX_ATTEMPT times, searching for a Lick meter wikipedia title.

    Args:
        Integer: attempts, retries remaining.
        Integer: backoff, seconds to wait between each loop.
    Returns:
        String or False: String of wikipedia title in Lick meter, or False if
                         none found.
    """
    for attempt in range(attempts):
        print(f"\r{str(attempt * 10)} articles fetched...", end="")
        sys.stdout.flush()
        title = checkTenPagesForLick()

        if type(title) == str and len(title) > 1:
            print(f"\nMatched: {title}")
            return title

        time.sleep(backoff)

    print(f"\nNo matches found.")
    sys.exit(1)


def checkTenPagesForLick():
    """Get 10 random wiki titles, check if any of them isLick().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in Lick meter, return the title. Otherwise, return False.

    Args:
        None
    Returns:
        String or False: The Lick compliant title, or False if none found.
    """
    wikipedia.set_rate_limiting(True)
    try:
        titles = wikipedia.random(10)
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"Wikipedia timout exception: {e}")
        time.sleep(TIMEOUT_BACKOFF)
        main()
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Wikipedia exception: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception while fetching wiki titles: {e}")
        sys.exit(1)

    for title in titles:
        if words.isLick(title):
            return title
    return False


if __name__ == "__main__":
    main()
