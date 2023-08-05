"""
Author: James Londal
Copyright: Copyright 2019, Hearts & Science
License: GNU AFFERO GENERAL PUBLIC LICENSE
Version: 1.0.0
Maintainer: James Londal
"""

__version__ = "1.5"

import pickle
import pandas as pd

#Twitter Collector
from .twitter_listener import *
from textblob import TextBlob


class Listener:

    keywords = None
    Usernames = None

    Profiles   = pd.DataFrame()
    Tweets     = pd.DataFrame()
    Hashtags   = pd.DataFrame()
    Related_Words = pd.DataFrame()

    def __init__(self,keywords=None,usernames=None,sample_size='Medium'):

        """
        You can start with set of keywords and/or twitter handles 

        keywords = {
            'Topic 1': 'gates foundation OR stiftung',
            'Topic 2' : 'internationale entwicklung'
            }
        usernames = ['username_1','username_2']
        
        sample_size = Large, Medium, Small or Test
        
        """
        self.keywords = keywords
        self.Usernames = usernames

        if sample_size == 'Large': 
            self.sample_size = 10000
        elif sample_size == 'Medium': 
            self.sample_size = 5000
        elif sample_size == 'Small': 
            self.sample_size = 1000
        elif sample_size == 'Test': 
            self.sample_size = 10
        else:
            self.sample_size = 5000

    def run(self):
        """
        runs the collector, if data already exists in the object will appened 
        """

        nest_asyncio.apply()

        if self.keywords:
            self.Tweets = pd.concat([self.Tweets,twitter_listener.Search_Twitter(self.keywords,size=self.sample_size)],sort=True) 
            self.Profiles = pd.concat([self.Profiles,twitter_listener.get_Users(self.Tweets.query("nlikes >= 5").username)],sort=True) 
            self.Tweets = pd.concat([self.Tweets,twitter_listener.get_timelines(self.Profiles.username)],sort=True) 

        if self.Usernames:
            self.Profiles = pd.concat([self.Profiles,twitter_listener.get_followers(self.Usernames,size=self.sample_size)],sort=True) 
            self.Tweets = pd.concat([self.Tweets,twitter_listener.get_timelines(self.Usernames)],sort=True) 


        self.Tweets['clean_tweet'] = twitter_listener.clean_tweet_txt(self.Tweets, 'tweet')

        df2 = pd.DataFrame()
        df2['tweets'] = self.Tweets.groupby('username')['clean_tweet'].agg(lambda col: ' '.join(col))
        df2['lang_tags'] = df2['tweets'].apply( lambda x : twitter_listener.lang_tags(x))

        self.Profiles = self.Profiles.join(df2, on='username')

        (self.Hashtags, self.Related_Words) = twitter_listener.Hashtags(self.Tweets)

    @classmethod
    def load(self,filename):
        """
        loads an objects
        """
        f = open(filename,'rb')
        self.Profiles = pickle.load(f)
        self.Tweets = pickle.load(f)
        self.Hashtags = pickle.load(f)

        self.keywords = pickle.load(f)
        self.Usernames = pickle.load(f)

        f.close()

    def save(self,filename):
        """
        saves an object
        """
        f = open(filename,'wb')
        pickle.dump(self.Profiles, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.Tweets, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.Hashtags, f, protocol=pickle.HIGHEST_PROTOCOL)

        pickle.dump(self.keywords, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.Usernames, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

