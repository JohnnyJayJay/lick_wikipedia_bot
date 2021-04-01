## The Lick Wikipedia Bot

Every 60 minutes this Python script posts to @thelickbot
The majority of the original functionality implemented by @catleball for TMNT Wikipedia bot @wiki_tmnt - I've just changed the meter searching and the image macroing.

### Why

For fun! Inspired by https://twitter.com/insanerainmusic/status/1186288069986734080, and original setup (TMNT Wikipedia bot) inspired by https://xkcd.com/1412/

### How

When it runs, it:

- Pulls 10 random Wikipedia article titles
- Checks if they are in a suitable prosody/meter to match The Lick (or a variant of it)
  - If not, pull 10 more articles ad infinitum until a match is found
- Create an image containing The Lick phrase and the found lyrics underneath
- Post the title and generated music to @thelickbot

### Environment

This script requires the following:

- Python >= 3.7
  - Earlier may work, only tested on 3.7
- Chrome >= 57
- Via PyPi:
  - pronouncing
  - num2words
  - PIL (pillow)
  - pyphen
  - syllables
  - tweepy
  - wikipedia

For @thelickbot it runs on a cron job on my local machine.

### Configuration

I haven't defined a config file format yet, it's in the TODO list below. Common config knobs are currently mostly in `lib/constants.py`.

### How to run it

The preferred way to run the app is [docker](https://docker.com). 

1. Clone this repository
   
   ```
   git clone https://github.com/JohnnyJayJay/lick_wikipedia_bot
   ```
2. Place a file called `auth.txt` in `lick_wikipedia_bot`. See [auth.txt.template](./auth.txt.template) to see what to put where. 
3. Run with docker
   
   ```
   docker-compose up
   ```
   
   

### Caveats

I'm not developing this for anyone but myself, so you may see some anti-patterns like hardcoded paths specific to my environment, and general lack of configurability outside editing the source.

Given this runs once per hour, I'm not very concerned about performance. I often choose slow, but readable and easy-to-implement solutions.

### TODO
