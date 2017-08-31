#!/usr/bin/env python
import sys

# Get input from stdin
for line in sys.stdin:
    # remove possible whitespaces
    line = line.strip()
    # split the line into words
    words = line.split(",")
    # print root_subreddit,related_subreddit1,related_subreddit2,related_subreddot3...
    print(words[0] + "," + ",".join(words[2:]), 1)