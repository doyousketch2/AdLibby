#! /usr/bin/env python3

##  pip install tweepy
##  pip3 install tweepy

import time
import tweepy
import logging
import configparser

##  vars  ========================================================================================##

with open( 'config.ini' ) as conf:
    config  = conf .read()

botname  = config ['bot']['name']

consumer_key  = config ['consumer']['key']
consumer_secret  = config ['consumer']['secret']

access_token  = config ['access']['token']
access_token_secret  = config ['access']['token_secret']

hours_between_tweets  = config ['time']['hours']
minutes_between_tweets  = hours_between_tweets *60 +config ['time']['minutes']
seconds_between_tweets  = minutes_between_tweets *60 +config ['time']['seconds']

##  logging setup  ===============================================================================##
##  https://realpython.com/python-logging

log_level  = logging .DEBUG  ##  DEBUG,  INFO,  WARNING,  ERROR,  CRITICAL

log_name  = config ['bot']['name'] +'.log'

mode  = 'a'  ##  'a' append, 'w' overwrite

line  = '%(asctime)s.%(msecs)03d  %(levelname)s - %(message)s'

date_time  = '%d %b\'%y  %H:%M:%S'  ##  strftime.org

logging .basicConfig( level = log_level,  filename = log_name,  filemode = mode,  format = line,  datefmt = date_time   )

##  functions  ===================================================================================##

def login():
    auth  = tweepy .OAuthHandler( consumer_key, consumer_secret )
    auth .set_access_token( access_token,  access_token_secret )

    ##  Construct API instance
    api  = tweepy .API( auth,  wait_on_rate_limit = True,
                               wait_on_rate_limit_notify = True )

    try:
        api .verify_credentials()

    except Exception as exc:
        logging .error( "Error during authentication", exc_info = True )
        raise exc

    logging .info( "Authentication OK" )
    return api


def update_info():
    if config ['bot']['update']:
        logger.info( 'updating info' )

        api .update_profile(
            url = config ['bot']['url'],
            location = config ['bot']['location'],
            description = config ['bot']['description']  )
        config ['bot']['update']  = False


    if config ['colors']['update']:
        logger.info( 'updating colors' )

        api .update_profile_colors(
            profile_background_color  = config ['colors']['background_color'],
            profile_text_color  = config ['colors']['text_color'],
            profile_link_color  = config ['colors']['link_color'],
            profile_sidebar_fill_color  = config ['colors']['sidebar_fill_color'],
            profile_sidebar_border_color  = config ['colors']['sidebar_border_color']  )
        config ['colors']['update']  = False


    if config ['profile']['update']:

        logger.info( 'updating icon' )
        api .update_profile_image(  config ['profile']['image']  )

        logger.info( 'updating background image' )
        api .update_background_image(  config ['profile']['background_image']  )
        config ['profile']['update']  = False

##  main loop ====================================================================================##

def main():

    login()
    update_info()

    while True:
        ## tweet text
        status  = "This is a tweet."

        ##  path to upload - 2:20 video
        filename  = "twitter.mp4"

        ##  posting the tweet
        api .update_with_media( filename,  status )

        logger.info( 'Waiting', seconds_between_tweets, 'seconds' )
        time .sleep( seconds_between_tweets )

##  dunder  ======================================================================================##

if __name__ == "__main__":
    main()

##  eof  =========================================================================================##

