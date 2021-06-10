import os
import requests
import json
import tweepy
import TwitterAPI
from datetime import timezone
from time import time

APISession = TwitterAPI.DeveloperKeyConfigurations()
PARENT_TWEET_DETAILS = '{}'
PARENT_USER_DETAILS = '{}'
RETWEETERS_DETAILS = '{}'

def InsidrAlgorithm():
    pass




def Collectibles(retweetersID):
    global RETWEETERS_DETAILS

    TweetMetricValue, UserMetricValue = { retweetID[0]: tweetMetricComponent(retweetID[0]) for retweetID in retweetersID }, { retweeterID[1]: userMetricComponent(retweeterID[1]) for retweeterID in retweetersID }
    # UserMetricValue = { retweeter['user']['id']: [{"created_at": retweeter['user']['created_at']}, {"screen_name": retweeter['user']['screen_name']}, {"favourites_count": retweeter['user']['favourites_count']}, {"followers_count": retweeter['user']['followers_count']}, {"location": retweeter['user']['location']}, {"statuses_count": retweeter['user']['statuses_count']}] for retweeter in RETWEETERS_DETAILS }
    # print(TweetMetricValue, UserMetricValue)

    return TweetMetricValue, UserMetricValue

def userMetricComponent(userID):
    global RETWEETERS_DETAILS
    global PARENT_USER_DETAILS
    
    PARENT_USER_DETAILS["favourites_count"] = RETWEETERS_DETAILS[0]['retweeted_status']['user']['favourites_count']
    PARENT_USER_DETAILS["followers_count"] = RETWEETERS_DETAILS[0]['retweeted_status']['user']['followers_count']
    PARENT_USER_DETAILS["friends_count"] = RETWEETERS_DETAILS[0]['retweeted_status']['user']['friends_count']
    PARENT_USER_DETAILS["listed_count"] = RETWEETERS_DETAILS[0]['retweeted_status']['user']['listed_count']
    PARENT_USER_DETAILS["statuses_count"] = RETWEETERS_DETAILS[0]['retweeted_status']['user']['statuses_count']

    scrappedValues = '{}'
    unscrappedInfo = TwitterAPI.userMetrics(userID)
    scrappedValues = [{"created_at": unscrappedInfo['data'][0]['created_at']}, {"name": unscrappedInfo['data'][0]['name']}, {"username": unscrappedInfo['data'][0]['username']}, {"public_metrics": [{"favourites_count": retweeter['user']['favourites_count']}, {"followers_count": retweeter['user']['followers_count']}, {"friends_count": retweeter['user']['friends_count']}, {"listed_count": retweeter['user']['listed_count']}, {"statuses_count": retweeter['user']['statuses_count']}] for retweeter in RETWEETERS_DETAILS }]
    
    return scrappedValues

def tweetMetricComponent(tweetID):
    global RETWEETERS_DETAILS

    unscrappedInfo = TwitterAPI.tweetMetrics(tweetID)
    scrappedValues = [{"author_id": unscrappedInfo['data'][0]['author_id']}, {"created_at": unscrappedInfo['data'][0]['created_at']}, {"public_metrics": unscrappedInfo['data'][0]['public_metrics']}, {"source": unscrappedInfo['data'][0]['source']}]

    return scrappedValues




class Utility():

    def __init__(self, PARENT_TWEET_ID):
        self.PARENT_TWEET_ID = PARENT_TWEET_ID

    
    def retweetersScraping(self):
        global RETWEETERS_DETAILS

        tweet_id = self.PARENT_TWEET_ID
        key = APISession.consumer_key
        secret = APISession.consumer_secret

        authenticationURL = "https://api.twitter.com/oauth2/token"
        data = {'grant_type': 'client_credentials'}
        authenticationResponse = requests.post(authenticationURL, auth=(key, secret), data=data)
        bearerToken = authenticationResponse.json()['access_token']


        url = 'https://api.twitter.com/1.1/statuses/retweets/%s.json?count=1' % tweet_id
        headers = {'Authorization': 'Bearer %s' % bearerToken}
        retweetsResponse = requests.get(url, headers=headers)


        retweets = retweetsResponse.json()
        RETWEETERS_DETAILS = retweets
        # print(json.dumps(retweets, indent=4, sort_keys=True))
        retweeters = [[r['id'], r['user']['id'], r['user']['screen_name']] for r in retweets]

        # with open('retweeters-ids-%s.txt' % (tweet_id), 'w') as fileWriter:
        #     for r, i in retweeters:
        #         fileWriter.write('%s,%s\n' % (r, i))

        return retweeters
    

    def parentDetailsFromTwitterAPI(self):
        global PARENT_USER_DETAILS
        global PARENT_TWEET_DETAILS

        PARENT_TWEET_DETAILS = TwitterAPI.tweetMetrics(self.PARENT_TWEET_ID)
        PARENT_USER_DETAILS = TwitterAPI.userMetrics(PARENT_TWEET_DETAILS['data'][0]['author_id'])
        # print(json.dumps(PARENT_TWEET_DETAILS, indent=4, sort_keys=True))
        # print(json.dumps(PARENT_TWEET_DETAILS, indent=4, sort_keys=True))




def createInstance(PARENT_TWEET_ID):
    utilityInstance = Utility(PARENT_TWEET_ID)
    utilityInstance.parentDetailsFromTwitterAPI()
    scrappedTweetMetrics, scrappedUsertMetrics = Collectibles(utilityInstance.retweetersScraping())

    # print(json.dumps(PARENT_USER_DETAILS, indent=4, sort_keys=True))
    # print(json.dumps(PARENT_TWEET_DETAILS, indent=4, sort_keys=True))

# createInstance(1397207890075832320)
