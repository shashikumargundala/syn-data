#!/usr/bin/env python3

import csv
import time
import os
import sys

import tweepy

import kays

from utils import fopen, writelog, esc

def collect_tweets(task, tags):
  '''
  Collect tweets for tag, indefinitely and store in csv files
  '''
  print('Collecting tweets...')

  appKeys = kays.appKeys


  with fopen(task, newline='\n', encoding='utf-8') as f:
    # save task to log
    writelog(task, tags)
    keyIdx = 0
    tagIdx = 0

    # writer for csv
    writer = csv.writer(f)

    # collect tweets indefinitely by using all keys
    while True:
      # get the key
      key = appKeys[keyIdx]

      # create auth and api
      auth = tweepy.OAuthHandler(key['consumerAPIKey'], key['consumerAPISecretKey'])
      auth.set_access_token(key['accessToken'], key['accessTokenSecret'])
      api = tweepy.API(auth)

      # filter out retweets
      query = tags[tagIdx] + ' -filter:retweets'

      # collect tweets and save
      try:
        for tweet in tweepy.Cursor(api.search, q=query).items():
          user = tweet.user

          # escape text
          row = map(esc, [tweet.text, tweet.id, user.name, user.screen_name, user.location, user.description, user.followers_count, user.friends_count, user.listed_count, user.statuses_count, user.favourites_count, user.verified, user.default_profile_image, user.default_profile, user.protected, user.created_at])

          print(str(row))

          writer.writerow(row)
      except Exception as e:
        # Stop for 1min and then start using next key
        print(e)
        keyIdx = (keyIdx+1) % len(appKeys)
        tagIdx = (tagIdx+1) % len(tags)
        time.sleep(1 * 60)


def main():
  args = sys.argv[1:]

  task = ''
  tags = ''

  if len(args) == 0:
    # return
    task = 'all'
    tags = [
      '#LEFTIST_ARE_TERRORISTS',
      '#LeftAttacksJNU',
      '#ShutDownJNU'
      '#LeftKillingJNU',
      '#IndiaSupportsCAA',
      '#CAASupport',
      '#TukdeGangSpotted',
      '#JNUattack',
      '#ABVP_TERRORISTS',
      '#JNUTerrorAttack',
      '#IndiaAgainstCAA',
      '#CAA_NRC'
    ]
  else:
    task = args[0]
    tags = [args[1]]

  collect_tweets(task, tags)

if __name__ == "__main__":
  # execute only if run as a script
  main()