import twitter
import urlparse # python 2.7
# import urllib # python 3.0
import logging
import time
from datetime import datetime
import PersistingIO_
import codecs
import sys

class TwitterAPI(object):
    """
    TwitterAPI class allows the Connection to Twitter via OAuth
    once you have registered with Twitter and receive the 
    necessary credentials 
    """
    def __init__(self): 
        consumer_key = 'VKtqIwFfDn2Ws1J9CMvLiLbpw'
        consumer_secret = 'kEX6w5FfTJFctLj9Jm91tm4TYQydqBewBBNqWkGbfnX4GtlQ0O'
        access_token = '311188727-h5eVHXmqtfKdfvlR8UsQ7jXMBiU08IUkupfqdBJB'
        access_secret = 'LEMeqTg6XjQ0TYWTyaE35hUI3uS2gExlTRAnr0FDhaVqw'
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.retries = 3
        self.auth = twitter.oauth.OAuth(access_token, access_secret, consumer_key, consumer_secret)
        self.api = twitter.Twitter(auth=self.auth)
        # logger initialisation
        appName = 'twt150530'
        self.logger = logging.getLogger(appName)
        #self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        logPath = '/home/henry/spark'
        fileName = appName
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler) 
        self.logger.setLevel(logging.DEBUG)
        
        # Save to JSON file initialisation
        jsonFpath = '/home/henry/spark'
        jsonFname = 'twitterjson'
        self.jsonSaver = IO_json(jsonFpath, jsonFname)
        csvFpath = '/home/henry/spark'
        csvFname = 'twittercsv'
        self.csvSaver = IO_csv(csvFpath, csvFname)       


    def searchTwitter(self, q, maxid, max_res=10000, **kwargs):
        print maxid    
        search_results = self.api.search.tweets(q=q,max_id=maxid,count=100 , **kwargs)
    
        statuses = search_results['statuses']
               
        max_results = min(10000, max_res) 
        for _ in range(1):
            try:
                next_results = search_results['search_metadata']['next_results']
                # self.logger.
                ('info in searchTwitter - next_results:%s'% next_results[1:])
            except KeyError as e:
            	#self.logger.error('error in searchTwitter: %s', %(e))
                break
            
            # next_results = urlparse.parse_qsl(next_results[1:]) # python 2.7
            next_results = urlparse.parse_qsl(next_results[1:])
            # self.logger.info('info in searchTwitter - next_results[max_id]:', next_results[0:])
            kwargs = dict(next_results)
            #self.logger.info('info in searchTwitter - next_results[max_id]:%s'% kwargs['max_id'])        
            search_results = self.api.search.tweets(**kwargs)
            statuses += search_results['statuses']
            if len(statuses) > max_results:
                self.logger.info('info in searchTwitter - got %i tweets - max: %i' %(len(statuses), max_results))
                break
        return statuses
          
    def saveTweets(self, statuses):
        # Saving to JSON File
        a =['id', 'created_at', 'tweet_text','retweet_count','user_id', 'user_name', 'user_created_at','user_location','user_screen_name','user_friends_count' , 'user_followers_count','user_favourites_count','user_total_tweets', 
             'user_listed_count','user_profile_sidebar_fill_color','user_profile_sidebar_border_color','user_profile_image_url','user_description','user_lang','user_time_zone', 
             'user_profile_link_color','user_profile_background_tile','user_id_str','user_default_profile','user_contributors_enabled',
             'user_utc_offset','user_profile_use_background_image','user_profile_text_color','user_profile_background_color','url']
        self.jsonSaver.save(statuses,a)      
        # Saving to MongoDB
        # for s in statuses:
        # self.mongoSaver.save(s)
    #def saveTweetss(self, statuses,NTname, fields):            
     #   self.csvSaver.save(statuses,"b","a")   
        
    def saveTweetscsv(self, statuses):

       fields01 = ['id', 'created_at', 'tweet_text','retweet_count','user_id', 'user_name', 'user_created_at','user_location','user_screen_name','user_friends_count' , 'user_followers_count','user_favourites_count','user_total_tweets', 
                   'user_listed_count','user_profile_sidebar_fill_color','user_profile_sidebar_border_color','user_profile_image_url','user_description','user_lang','user_time_zone', 
                   'user_profile_link_color','user_profile_background_tile','user_id_str','user_default_profile','user_contributors_enabled',
                   'user_utc_offset','user_profile_use_background_image','user_profile_text_color','user_profile_background_color','url']
       self.csvSaver.save(statuses,'nt', fields01)           

    def parseTweets(self, statuses):
        return [ (status['id'], 
                  status['created_at'],
                  status['text'],           
                  status['retweet_count'], 
                  status['user']['id'],
                  status['user']['name'], 
                  status['user']['created_at'], 
                  status['user']['location'], 
                  status['user']['screen_name'], 
                  status['user']['friends_count'], 
                  status['user']['followers_count'], 
                  status['user']['favourites_count'], 
                  status['user']['statuses_count'],
                  status['user']['listed_count'],
                  status['user']['profile_sidebar_fill_color'], 
                  status['user']['profile_sidebar_border_color'], 
                  status['user']['profile_image_url'],  
                  status['user']['description'],
                  status['user']['lang'],
                  status['user']['time_zone'],
                  status['user']['profile_link_color'],           
                  status['user']['profile_background_tile'],
                  status['user']['id_str'],
                  status['user']['default_profile'],
                  status['user']['contributors_enabled'],
                  status['user']['utc_offset'],
                  status['user']['profile_use_background_image'],
                  status['user']['profile_text_color'],
                  status['user']['profile_background_color'],
                  url['expanded_url']) 
                        for status in statuses 
                            for url in status['entities']['urls'] ]
                            
    def parseTweetscsv(self, statuses):
        return [ (status['id'], 
                  status['created_at'].encode('utf-8') ,
                  status['text'].encode('utf-8'),        
                  status['retweet_count'], 
                  status['user']['id'],
                  status['user']['name'].encode('utf-8'), 
                  status['user']['created_at'].encode('utf-8'), 
                  status['user']['location'].encode('utf-8'), 
                  status['user']['screen_name'].encode('utf-8'), 
                  status['user']['friends_count'], 
                  status['user']['followers_count'], 
                  status['user']['favourites_count'], 
                  status['user']['statuses_count'],
                  status['user']['listed_count'],
                  status['user']['profile_sidebar_fill_color'].encode('utf-8'), 
                  status['user']['profile_sidebar_border_color'].encode('utf-8'), 
                  status['user']['profile_image_url'].encode('utf-8'),               
                  status['user']['description'].encode('utf-8'),
                  status['user']['lang'].encode('utf-8'),
                  status['user']['time_zone'],
                  status['user']['profile_link_color'].encode('utf-8'),           
                  status['user']['profile_background_tile'],
                  status['user']['id_str'].encode('utf-8'),
                  status['user']['default_profile'],
                  status['user']['contributors_enabled'],
                  status['user']['utc_offset'],
                  status['user']['profile_use_background_image'],
                  status['user']['profile_text_color'].encode('utf-8'),
                  status['user']['profile_background_color'].encode('utf-8'),
                  url['expanded_url'].encode('utf-8')) 
                        for status in statuses 
                            for url in status['entities']['urls'] ]
                                
    def parseTweetsmax(self, statuses,maxid):
        for status in statuses :
            print status['created_at']
            if (status['id']< maxid):          
                maxid=status['id']      
        return maxid-1                          

    def getTweets(self, q , maxid, max_res=10000):
        """
        Make a Twitter API call whilst managing rate limit and errors.
        """
        timee=1
        def handleError(e, wait_period=2, sleep_when_rate_limited=True):
            
            if wait_period > 3600: # Seconds
                #self.logger.error('Too many retries in getTweets: %s', %(e))
                raise e
            if e.e.code == 401:
                #self.logger.error('error 401 * Not Authorised * in getTweets: %s', %(e))
                return None
            elif e.e.code == 404:
                #self.logger.error('error 404 * Not Found * in getTweets: %s', %(e))
                return None
            elif e.e.code == 429: 
                #self.logger.error('error 429 * API Rate Limit Exceeded * in getTweets: %s', %(e))
                if sleep_when_rate_limited:
                    #self.logger.error('error 429 * Retrying in 15 minutes * in getTweets: %s', %(e))
                    #sys.stderr.flush()
                    time.sleep(905)
                    #self.logger.info('error 429 * Retrying now * in getTweets: %s', %(e))
                    return 2
                else:
                    raise e # Caller must handle the rate limiting issue
            elif e.e.code in (500, 502, 503, 504):
                self.logger.info('Encountered %i Error. Retrying in %i seconds' % (e.e.code, wait_period))
                time.sleep(wait_period)
                wait_period *= 1.5
                return wait_period
            else:
                #self.logger.error('Exit - aborting - %s', %(e))
                raise e
        
        while True:
            try:
                timee=timee+1
                print "******************"
                print timee
                print maxid
                tsearch=self.searchTwitter(q, maxid, max_res=10000)              
                ttsearch = self.parseTweets(tsearch)
                self.saveTweets(ttsearch)
                tttsearch = self.parseTweetscsv(tsearch)
                self.saveTweetscsv(tttsearch)
                maxid= self.parseTweetsmax(tsearch,maxid)           
             
            except twitter.api.TwitterHTTPError as e:
                error_count = 0 
                wait_period=2
                wait_period = handleError(e, wait_period)
                if wait_period is None:
                    return

t=TwitterAPI()
q="fintech"
maxid=10000000000000000000
tsearch = t.getTweets(q,maxid)

