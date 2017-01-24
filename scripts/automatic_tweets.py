# -*- coding: utf-8 -*-
import os
import sys

heads, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))
site_root, project_dir_name = os.path.split(heads)
sys.path.append(heads)

os.environ['PROJECT_DIR_NAME'] = project_dir_name
os.environ['DJANGO_SETTINGS_MODULE'] = project_dir_name + '.settings'
os.environ['OVERLOAD_SITE'] = 'adimsayar'
os.environ['SITE_ROOT'] = os.path.dirname(__file__)

from django.core.management import setup_environ

import settings

setup_environ(settings)
DEBUG = False

#keep this for render_to_string unicode errors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.contrib.auth.models import User
from content.models import Tweet
import urllib, urllib2
import simplejson as json
import random
import string
import time
import hmac
import hashlib
import datetime


#if expired get new one using this url: 
# first https://developers.facebook.com/tools/access_token/
# then https://graph.facebook.com/oauth/access_token?client_id=APP_ID&client_secret=APP_SECRET&grant_type=fb_exchange_token&fb_exchange_token=EXISTING_ACCESS_TOKEN 
# app secret is 6c5ca248f1e45c226b8778b5f651ffe3 which is adimsayar app app secret
# invalidates every 60 days


FBX_APP_ID = "210050799065722"
FBX_ACCESS_TOKEN = "CAACZCCkNDWnoBAJp8T4paAH9lznqoyWPZAyP9Urzrm16irekd3NqvIUis7cVZAonXHSiC9ZBNJslRS4EBeKZAO9mg6rEk3QguPauwRuFliexOVMfGCEmz1LdI2406V3kg7greHDhb1yVZAiBzKlWpWkfY3XBv0EIwZCQafPgJYMzwZDZD"
#FBX_ACCESS_TOKEN = "AAACZCCkNDWnoBAFOluGZCk0spnhiElCHDnyTL3dQgoj1krMOe8TrtlUvM7O7906FcI6bVoDmQSsZCjFWOWsNvf90wh7aoVRuHkAexQM7QZDZD"

def fb_post_feed(message):
	fb_id = FBX_APP_ID
	access_token = FBX_ACCESS_TOKEN
	tmp = urllib.urlopen("https://graph.facebook.com/"+ fb_id +"/feed?",
		urllib.urlencode(dict(access_token=access_token,
			message=message)))
	profile = json.load(tmp)
	print profile
	if "id" in profile:
	  return True
	elif "error" in profile:
	  return False

#posted = fb_post_feed(FBX_APP_ID, FBX_ACCESS_TOKEN,"3yet another test")
TWITTER_OAUTH_CONSUMER_KEY = "8gChi9d6s5WAvmL5NQ8Eg"
TWITTER_OAUTH_CONSUMER_SECRET = "qXjyRNBOZsLlmub7J9c47dpgDKQyfDRmeEUbqbcbc"
TWITTER_OAUTH_TOKEN = "420633696-AVKZwrzaXQc383YMBSfuMwmj8IjwXajSCxjNrYgf"
TWITTER_OAUTH_SECRET = "YCgwYiKiptl5Gh9q9Gm4MtiyRtkgR1PqAlAj7I6cMzU"


#            "oauth_nonce": "".join(random.choice(string.digits + string.letters) for i in xrange(32)),
#            "oauth_timestamp": str(int(time.time())),

def post_tweet(message):
    params = {
            "oauth_consumer_key": TWITTER_OAUTH_CONSUMER_KEY,
            "oauth_nonce": "".join(random.choice(string.digits + string.letters) for i in xrange(32)),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_token": TWITTER_OAUTH_TOKEN,
            "oauth_version": "1.0",
			"trim_user": "true",
			"include_entities": "true"
            }
    #status = {"status": u"Always look on the bright side of life".encode("UTF-8")}
    #stat = message.encode("UTF-8")
    #stat_encoded = urllib.quote(stat)
    status = {"status":message.encode("UTF-8")}
    #print status
    params.update(status)
    url = "https://api.twitter.com/1/statuses/update.json"
    key = "&".join([TWITTER_OAUTH_CONSUMER_SECRET, TWITTER_OAUTH_SECRET])
    msg = "&".join(["POST", urllib.quote(url,""),
                urllib.quote("&".join([k+"="+urllib.quote(params[k], "-._~") for k in sorted(params)]), "-._~")])

    print msg
    signature = hmac.new(key, msg, hashlib.sha1).digest().encode("base64").strip()
    params["oauth_signature"] = signature
    req = urllib2.Request(url,
          headers={"Authorization":"OAuth", "Content-type":"application/x-www-form-urlencoded"})
    req.add_data("&".join([k+"="+urllib.quote(params[k], "-._~") for k in params]))
    print req.get_data()
    res = urllib2.urlopen(req).read()
    print res


#import pdb; pdb.set_trace()
#post_tweet("asasdasd şşişiöşi #hicbirkisi")
now = datetime.datetime.now()
weekday = now.weekday()
tweet = Tweet.objects.filter(when=weekday+11).order_by('?')[0]
#tweet = Tweet.objects.order_by('?')[0]
print tweet.message
post_tweet(tweet.message)
#fb_post_feed(tweet.message)



