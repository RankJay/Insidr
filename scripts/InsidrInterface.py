import tweepy
import TwitterAPI

APISession = TwitterAPI.DeveloperKeyConfigurations()

tweepyAuth = tweepy.OAuthHandler(APISession.consumer_key, APISession.consumer_secret)
tweepyAuth.set_access_token(APISession.access_token, APISession.access_secret)
tweepyAPISession = tweepy.API(tweepyAuth)


# Change the Owner Name here in order to get admin access and privileges
OWNER_NAME = "triquet77786036"
FILE_NAME = './LastSeenId.txt'
# =====================================================================




def retrieveLastSeenId(file_name):
    f_read = open(file_name, 'r')
    lastSeenId = int(f_read.read().strip())
    f_read.close()
    return lastSeenId

def storeLastSeenId(lastSeenId, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(lastSeenId))
    f_write.close()
    return

def replyToTweets():
    print('Triquetra is up and running...', flush=True)

    lastSeenId = retrieveLastSeenId(FILE_NAME)

    mentions = tweepyAPISession.mentions_timeline(lastSeenId, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        lastSeenId = mention.id
        storeLastSeenId(lastSeenId, FILE_NAME)
        if 'publicize' in mention.full_text.lower():
            pass