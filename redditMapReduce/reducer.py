#!/usr/bin/env python
import sys

# Get input from stdin
for line in sys.stdin:
    # remove possible whitespaces
    line = line.strip()
    # split the line into words
    words = line.split(",")
    # print pairs of related subreddits
    # starts on 1 to ignore the root subreddit. Stops on len(words)-1 to ignore "1" in the last position.
    for word in words[1:len(words)-1]:
        print(words[0] + "," + word)