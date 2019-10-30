import re

# Constants for use throughout the application.
# Someday maybe I'll use configs or CLI args. For now this is easier.
MAX_ATTEMPTS = 1000
MAX_STATUS_LEN = 280
BACKOFF = 0.5
TIMEOUT_BACKOFF = 240
KEY_PATH = ""
# Licc image information
Y_POSITION = 220
X_POSITIONS = [172, 267, 362, 457, 552, 697, 792]
# Article titles the contain strings in BANNED_WORDS are skipped.
# Banned words are things that are very inappropriate, or things
# that are oversaturating the timeline, i.e. historic districts
BANNED_WORDS = ("rape", "nazi", "victim")
BANNED_PHRASES = ("rugby union", "historic district", "murder of")
PRONUNCIATION_OVERRIDES = (("HD", "10"), ("U.S.", "10"), ("Laos", "1"))
LICK_STRESSES = re.compile(r"^1[012]1[012]1[012][012]$")
CHARS_ONLY = re.compile("[^a-zA-Z]")
