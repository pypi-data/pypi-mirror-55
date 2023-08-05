"""
Author: James Londal
Copyright: Copyright 2019, Hearts & Science
License: GNU AFFERO GENERAL PUBLIC LICENSE
Version: 1.0.0
Maintainer: James Londal
"""

import twint 
import nest_asyncio
import pandas as pd
import numpy as np

def Search_Twitter(search_terms,size=10000,lang='en',locations=None,min_likes=5,min_replies=0,min_retweets=0,since=None,until=None):
    """
    Searches twitter using a collection of search terms 
    """
    df = pd.DataFrame()
    
    for key in search_terms.keys():
        c = twint.Config()
        c.Limit = size
        c.Get_replies = True
        c.Pandas = True
        c.Hide_output = True
        c.Tor_control_password
        c.Lang = lang
        c.Min_likes = min_likes
        c.Min_replies = min_replies
        c.Min_retweets = min_retweets
        
        if since: c.Since = since
        if until: c.Until = until
        
        c.Search = search_terms[key]
        
        if locations:
            for loc in locations:
                c.Near = locations
                twint.run.Search(c)

                Tweets_df = twint.storage.panda.Tweets_df
                Tweets_df['topic'] = key

                df = pd.concat([df,Tweets_df],sort=True) 
        else:
            twint.run.Search(c)

            Tweets_df = twint.storage.panda.Tweets_df
            Tweets_df['topic'] = key

            df = pd.concat([df,Tweets_df],sort=True) 
            
        df['hashtags'] = df['hashtags'].apply(lambda x: ' '.join(x))
        
    return df

def get_Hastags(df):
    """
    takes a dataframe of tweets and extracts the hashtags 
    """
    hastags = {}
    for tweet in df[df['hashtags'] != '']['hashtags'].values:
        for tag in tweet.split(' '):
            try:
                hastags[tag] += 1
            except:
                hastags[tag] = 1

    tag = []
    cnt = []
    users = []
    for (key) in hastags:
        tag.append(key)
        cnt.append(len(np.unique(df[df['hashtags'].str.contains(pat = key)].id)))    
        users.append(len(np.unique(df[df['hashtags'].str.contains(pat = key)].username)))
    
    hastags_cnt = pd.DataFrame()
    hastags_cnt['hashtag'] = tag
    hastags_cnt['tweets'] = cnt
    hastags_cnt['users'] = users
    
    return hastags_cnt

def Hashtags(df):
    """
    returns the conditional probablity given of a tweet containing a hashtag given another hashtag
    """    
    num_tweets  = len(df)
    num_users   = len(np.unique(df.username))
    
    hastags_cnt = get_Hastags(df)
    
    hastags_cnt.sort_values(by='tweets',ascending=False,inplace=True)

    hastags_cnt['Pr_tweet'] = hastags_cnt['tweets']/num_tweets
    hastags_cnt['Pr_user'] = hastags_cnt['users']/num_users

    hastag_con_pr = pd.DataFrame()

    for hashtag in hastags_cnt.query('tweets >= 1')['hashtag']:
        p1 = df[df['hashtags'].str.contains(pat = hashtag)]
        p2 = get_Hastags(p1)
        
        p2['hashtag_1'] = hashtag
        p2['hashtag_1_tweets'] = hastags_cnt[hastags_cnt['hashtag'] == hashtag]['tweets'].values[0]
        p2['hashtag_1_users'] = hastags_cnt[hastags_cnt['hashtag'] == hashtag]['users'].values[0]
        
        p2['Pr_tweet'] = p2['tweets']/p2['hashtag_1_tweets']
        p2['Pr_users'] = p2['users']/p2['hashtag_1_users']

        p2.sort_values(by='tweets',ascending=False,inplace=True)
        
        p2 = p2[p2['Pr_tweet'] < 1.00]
        p2 = p2[p2['tweets'] > 1]

        hastag_con_pr = pd.concat([hastag_con_pr,p2],sort=True) 
    
    hastag_con_pr.sort_values(by='Pr_users',ascending=False,inplace=True)

    return (hastags_cnt, hastag_con_pr)


def get_Users(usernames):
    """
    gets user profiles from a collection of tweets 
    """
    twint.run.output.panda.clean()

    for users in usernames:

        c = twint.Config()
        c.Username = users
        c.Get_replies = True
        c.Pandas = True
        c.Hide_output = True
        c.Tor_control_password

        twint.run.Lookup(c)

    users_df = twint.run.output.panda.User_df.copy()
    users_df.sort_values(by='followers',ascending=False,inplace=True)
    users_df.drop_duplicates(inplace=True)
    
    return users_df

def get_tweets(username,size=10,min_likes=5,min_replies=0,min_retweets=0):
    """
    Gets tweets from a specific user 
    """
    twint.run.output.panda.clean()
    c = twint.Config()
    c.Username = username 
    c.Pandas = True
    c.Hide_output = True
    c.Tor_control_password
    c.Limit = size
    c.Source = "Twitter Web Client"
    c.Min_likes = min_likes
    c.Min_replies = min_replies
    c.Min_retweets = min_retweets
        
    c.Replies = True
    
    twint.run.Search(c)
    
    return twint.run.output.panda.Tweets_df.copy()


def get_users_replied_to(df,dropna=True):
    """
    takes df of a users tweets and replies and then returns a list of all the users he has replied to
    """
    def _get_usernames(x):
        try:
            return x['username']
        except:
            return None

    repied_users = []
    for i in range(1,len(pd.DataFrame(df['reply_to'].tolist()).ix[:,1:].columns)+1):
        repied_users.append(list(pd.DataFrame(df['reply_to'].tolist()).ix[:,1:][i].apply(_get_usernames).values))

    if dropna:
        repied_users = [item for sublist in repied_users for item in sublist]
    repied_users = [i for i in repied_users if i] 
    return repied_users

def get_followers(usernames,size=100):
    df = pd.DataFrame()
    for username in usernames:
        print(username)
        c = twint.Config()
        twint.run.output.panda.clean()
        c.Username = username 
        c.User_full = True
        c.Pandas = True
        c.Hide_output = True
        c.Tor_control_password
        c.Limit = size

        twint.run.Followers(c)
        
        tmp_df = twint.run.output.panda.User_df.copy()
        tmp_df['seed_user'] = username
        
        df = pd.concat([df,tmp_df],sort=True) 
    
    return df

def get_timelines(users,size=100):
    timeline_df = pd.DataFrame()
    for user in users:
        timeline_df = pd.concat([timeline_df,get_tweets(user,size=size,min_likes=3)],sort=True) 
    
    timeline_df['hashtags'] = timeline_df['hashtags'].apply(lambda x: ' '.join(x))
    return timeline_df

def clean_tweet_txt(df, column):
    series = df[column].str.replace(r'http +','http')\
    .replace(r' com','com')\
    .replace(r"https?://[^\s]+", '',regex=True)\
    .replace(r'@\w+',' ', regex=True)\
    .replace(r"pic.twitter.com[^\s]+",'',regex=True)\
    .replace(r"twitter",'',regex=True)
    return series

def lang_tags(x):
    blob = TextBlob(x)
    nonus = []
    verbs = []
    adject = []
    for (word,tag) in blob.tags:
        if len(word) >= 3:
            if tag == 'NN' or tag == 'NNS' or tag == 'NNPS' : nonus.append(word)
            if 'VB' in tag  : verbs.append(word)
            if 'JJ' in tag : adject.append(word)
        
    return (' '.join(nonus),
            ' '.join(verbs),
            ' '.join(adject))