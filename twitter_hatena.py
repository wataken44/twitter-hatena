#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" twitter-hatena.py


"""

import calendar
import codecs
import datetime
import json
import mechanize
import rfc822
import sys
import time
import urllib2

from pit import Pit

class Hatena(object):
    def __init__(self, username, password, domain):
        self.__username = username
        self.__password = password
        self.__domain = domain


    def Post(self, title, text):
        # login
        br = mechanize.Browser()
        br.open("https://www.hatena.ne.jp/login")
        br.select_form(nr=0)
        br["name"] = self.__username
        br["password"] = self.__password
        br.submit()

        # post
        br.open("http://blog.hatena.ne.jp/%s/%s/edit?editinplace=1"%(self.__username, self.__domain))
        br.select_form(nr=0)
        br["title"] = title.encode('utf-8')
        br["body"] = text.encode('utf-8')
        br.submit()


def GetTimeline(screen_name):
    url = "https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=" + screen_name + "&count=200"

    try:
        req = urllib2.Request(url=url)
        fp = urllib2.urlopen(req)
        
        js = json.loads(fp.read(), "UTF-8")
    except:
        return None

    return js


def CreateLink(href, text, klass=None):
    if klass:
        return "<a href=\"%s\" class=\"%s\" rel=\"nofollow\">%s</a>" % (href, klass, text)
    else:
        return "<a href=\"%s\" rel=\"nofollow\">%s</a>" % (href, text)

def BuildPost(timeline):
    if not isinstance(timeline, list):
        return None

    yesterday = datetime.date.today() - datetime.timedelta(1)
    
    tweets = []

    for elem in timeline:
        # determine elem is tweet or not
        if 'user' not in elem or 'created_at' not in elem or 'text' not in elem:
            continue
        # maybe tweet

        created_at_str = calendar.timegm(rfc822.parsedate(elem['created_at']))
        created_at = datetime.datetime.fromtimestamp(created_at_str)

        # filter tweet at yesterday
        if yesterday.year != created_at.year or yesterday.month != created_at.month or yesterday.day != created_at.day:
            continue

        text = BuildText(elem)
        tweets.append(text)

    post = "<!--\\n-->  ".join(reversed(tweets))
    post = "<ul class=\"twitter-log\">\n  " + post + "\n</ul>";

    return post

def BuildText(tweet):
    text = tweet['text']

    if 'entities' in tweet:
        for info in tweet['entities']['urls']:
            text = text.replace(
                info['url'],
                CreateLink(info['url'],info['expanded_url']))
        for info in tweet['entities']['hashtags']:
            text = text.replace(
                '#' + info['text'],
                CreateLink("//twitter.com/serch/%23"+info['text'],'#'+info['text']))
        for info in tweet['entities']['user_mentions']:
            name = info['screen_name']
            text = text.replace(
                '@' + name,
                CreateLink("//twitter.com/"+name,'@'+name))

    text = '<li class="twitter-tweet"><span class="twitter-text">' + text + "</span>"

    created_at_str = calendar.timegm(rfc822.parsedate(tweet['created_at']))
    created_at = datetime.datetime.fromtimestamp(created_at_str)

    screen_name = tweet['user']['screen_name']
    id_str = tweet['id_str']
    
    text += " " + CreateLink("//twitter.com/%s/status/%s"%(screen_name, id_str), created_at.strftime("%H:%M:%S"), "twitter-permalink") + "</li>"

    return text
    

def main():
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    credential = Pit.get('twitter-hatena',
                         {'require' : 
                          { 'hatena_username': '', 'hatena_password': '', 'hatena_domain': 'hatenablog.com', 'twitter_screenname': '' }})

    hatena = Hatena(credential['hatena_username'], credential['hatena_password'], credential['hatena_domain'])
    
    for i in range(9):
        timeline = GetTimeline(credential['twitter_screenname'])

        text = None
        if timeline is not None:
            text = BuildPost(timeline)
            yesterday = datetime.date.today() - datetime.timedelta(1)
            title = yesterday.strftime("%Y/%b/%d") + u"のtweet"

        if text is not None and text != "":
            #print text
            hatena.Post(title, text)
            return 

        time.sleep(3600 / 7 + 1)

if __name__ == "__main__":
    main()
