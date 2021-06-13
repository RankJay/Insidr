from requests_oauthlib import OAuth1Session
import os
import json
import requests

class DeveloperKeyConfigurations():
    # To set your enviornment variables in your terminal run the following line:

    # export 'CONSUMER_KEY'='<your_consumer_key>'
    # export 'CONSUMER_SECRET'='<your_consumer_secret>'
    # export 'BEARERTOKEN'='<your_bearer_token>'

    consumer_key = 'ohMa5HYN1pXT7x3X2H67499B1'
    consumer_secret = 'xqSfnEmZHn3YNnqo3Yk6ruzhOs9LpiOqtFjNKw7gJiC9mRT4Q0'
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAF5GNAEAAAAALUoy1SaTDchx11r3GZ8Z0Qz9GQY%3DQFrQhXz14idxvfzZcuF8NBagW9sLy6b3mk9u6PIcjbUUC8Qzf2'
    access_token = '1086485080728428545-IWLwqXMSDpzSjm7jpyti1NqbLgMbZq'
    access_secret = 'uG7vhvOIUtZBEPkCnVavqOistTXljX4nIPblyxbdmvZHa'
    
    def __init__(self):
        pass

    def developerKeyConfigurations(self):
        # Write your extra pre-set variable tokens here 
        pass


# Declaring Decisive content sessions
keyAccessSession = DeveloperKeyConfigurations()
TweetMetricsJSON = '{}'
UserMetricsJSON = '{}'
UserFollowsJSON = '{}'
UserFollowingJSON = '{}'


def OAuthentication_v1A():
    global keyAccessSession
    # To set up Oauth v1.A request in order to fetch desired requests
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(keyAccessSession.consumer_key, client_secret=keyAccessSession.consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
        print(fetch_response)
    except ValueError:
        print("There may have been an issue with the consumer_key or consumer_secret you entered.")

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(keyAccessSession.consumer_key, client_secret=keyAccessSession.consumer_secret, resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret, verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)


    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(keyAccessSession.consumer_key, client_secret=keyAccessSession.consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)

    return oauth




def tweetMetrics(tweetID):
    global TweetMetricsJSON
    # You can adjust ids to include a single Tweets
    # Or you can add to up to 100 comma-separated IDs
    params = {"ids": tweetID, "tweet.fields": "id,author_id,created_at,text,attachments,lang,source,withheld,conversation_id,context_annotations,entities,geo,possibly_sensitive,public_metrics,organic_metrics,non_public_metrics", "expansions": "attachments.media_keys", "media.fields": "duration_ms,public_metrics"} # Add tweet.fields for non_public_metrics, organic_metrics, promoted_metrics
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    # Make the request
    oauth = OAuthentication_v1A()
    response = oauth.get("https://api.twitter.com/2/tweets", params=params)

    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    print("Response code: {}".format(response.status_code))
    TweetMetricsJSON = response.json()
    # json_response = response.json()
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    return TweetMetricsJSON

# NEED TWEET.ID OF USER
def userMetrics(userID):
    global UserMetricsJSON
    # You can adjust ids to include a single Tweets
    # Or you can add to up to 100 comma-separated IDs
    params = {"ids": userID, "user.fields": "id,created_at,name,username,verified,description,entities,location,pinned_tweet_id,profile_image_url,protected,url,withheld"} # Add tweet.fields for promoted_metrics

    # User fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    # Make the request
    oauth = OAuthentication_v1A()

    response = oauth.get("https://api.twitter.com/2/users", params=params)

    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    print("Response code: {}".format(response.status_code))
    UserMetricsJSON = response.json()
    # json_response = response.json()
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    return UserMetricsJSON

def userFollows(userID):
    global keyAccessSession
    global UserFollowsJSON
    # You can adjust ids to include a single Tweets
    # Or you can add to up to 100 comma-separated IDs

    params = {"user.fields": "created_at"} # Add tweet.fields for promoted_metrics
    headers = {"Authorization": "Bearer {}".format(keyAccessSession.bearer_token)}

    # User fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    response = requests.request("GET", "https://api.twitter.com/2/users/{}/followers".format(userID), headers=headers, params=params)

    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    print("Response code: {}".format(response.status_code))
    UserFollowsJSON = response.json()
    # json_response = response.json()
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    return UserFollowsJSON

def userFollowing(userID):
    global keyAccessSession
    global UserFollowingJSON
    # You can adjust ids to include a single Tweets
    # Or you can add to up to 100 comma-separated IDs

    params = {"user.fields": "created_at"} # Add tweet.fields for promoted_metrics
    headers = {"Authorization": "Bearer {}".format(keyAccessSession.bearer_token)}

    # User fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    response = requests.request("GET", "https://api.twitter.com/2/users/{}/following".format(userID), headers=headers, params=params)

    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    print("Response code: {}".format(response.status_code))
    UserFollowingJSON = response.json()
    # json_response = response.json()
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    return UserFollowingJSON




# tweetMetrics('1398540647003422726')
# print(json.dumps(TweetMetricsJSON, indent=4, sort_keys=True))
# print(TweetMetricsJSON['data'][0]['source'])
# userMetrics(1234812920791388160)
# print(json.dumps(UserMetricsJSON, indent=4, sort_keys=True))
# userFollows('2244994945')
# userFollowing('2244994945')
