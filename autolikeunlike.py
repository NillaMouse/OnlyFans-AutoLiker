import os
import sys
import json
import argparse
import logging
import time
import random
import math
from threading import Thread

import requests
import datetime

from _constants import (
    PROFILE_URL,
    POSTS_URL,
    POSTS_100_URL,
    FAVORITE_URL,
    HEADERS
)


class Logger:
    FORMAT = '%(levelname)s: %(message)s'

    def __init__(self):
        self.log = logging.getLogger(name=__name__)
        self.log.setLevel(level=logging.DEBUG)
        if not self.log.handlers:
            _formatter = logging.Formatter(fmt=self.FORMAT)
            _sh = logging.StreamHandler()
            _sh.setLevel(logging.INFO)
            _sh.setFormatter(fmt=_formatter)
            self.log.addHandler(hdlr=_sh)

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def error(self, message):
        self.log.error(message)


class OnlyFans(Logger):
    def __init__(self, args):
        super().__init__()
        with open(os.path.join(sys.path[0], 'auth.json')) as f:
            _a = json.load(f)['auth']
        if not _a['auth_uniq_']:
            _a.pop('auth_uniq_')
        else:
            _a[f"auth_uniq_{_a['auth_id']}"] = _a.pop('auth_uniq_')
        _cookies = [f'{k}={v}' for k, v in _a.items() if k !=
                    'user_agent' and k != 'app_token']
        self.headers = {"user-agent": _a['user_agent'], 'cookie': "; ".join(_cookies)}
        for k, v in HEADERS.items():
            self.headers[k] = v
        self.app_token = _a['app_token']
        self.username = args.username
        self.action = args.whattodo 
        self.id = None
        self.has_pinned_posts = None
        self.posts_count = None
        self.ids = None
        self.stop = False
        

    def scrape_user(self):
        with requests.Session() as s:
            r = s.get(PROFILE_URL.format(self.username, self.app_token), headers=self.headers)
        self.log.debug(r.status_code)
        if r.ok:
            user = r.json()
            self.id = user['id']
            self.has_pinned_posts = user['hasPinnedPosts']
            self.posts_count = user['postsCount']
            print(f'User {self.username} scraped with {self.posts_count} posts.', end='\n')
            write_log(f'User {self.username} scraped with {self.posts_count} posts.')
        else:
            self.stop = True
            self.log.error(f"Unable to scrape user profile -- Received {r.status_code} STATUS CODE")
            write_log(f'Unable to scrape user profile -- Received {r.status_code} STATUS CODE')

    def scrape_posts(self, pinned=0, array=[], count=0, cycles=0, time=0):
        if not array:
            if self.has_pinned_posts:
                with requests.Session() as s:
                    r = s.get(
                        POSTS_URL.format(self.id, self.posts_count, 1, self.app_token), headers=self.headers)
                if r.ok:
                    array = r.json()
                else:
                    self.stop = True
                    self.log.error(f'Unable to scrape pinned posts -- Received {r.status_code} STATUS CODE')
                    write_log(f'Unable to scrape pinned posts -- Received {r.status_code} STATUS CODE')
            if self.posts_count > 100:
                cycles = math.floor(self.posts_count / 100)
        url = POSTS_URL if not time else POSTS_100_URL
        slot = pinned if not time else time
        with requests.Session() as s:
            r = s.get(url.format(self.id, self.posts_count, slot, self.app_token),headers=self.headers)
        self.log.debug(r.status_code)
        if r.ok:
            posts = r.json()
            if cycles:
                if count < cycles:
                    count += 1
                    list_posts = array + posts
                    posted_at_precise = posts[-1]['postedAtPrecise']
                    posts = self.scrape_posts(
                        array=list_posts, count=count, cycles=cycles, time=posted_at_precise)
                    if time:
                        return posts
                else:
                    return array + posts
            else:
                posts += array

            write_log(f'Parsing {self.username} to determine posts to {self.action}')
            if self.action == 'like':
                favorited_posts = [post for post in posts if not post['isFavorite']]
                self.ids = [post['id'] for post in favorited_posts if post['canViewMedia']]
                print(f'Posts scraped with {len(self.ids)} posts to be liked.\n', end='\r')
                write_log(f'Posts scraped with {len(self.ids)} posts to be liked.')
            elif self.action == 'unlike':
                favorited_posts = [post for post in posts if post['isFavorite']]
                self.ids = [post['id'] for post in favorited_posts if post['canViewMedia']]
                print(f'Posts scraped with {len(self.ids)} posts to be unliked.\n', end='\r')
                write_log(f'Posts scraped with {len(self.ids)} posts to be unliked.')
            write_log(f'Parsing {self.username} completed - {len(self.ids)} to be actioned.')
            if len(self.ids):
                write_log(f'IDs : {self.ids}')
            
        else:
            self.stop = True
            self.log.error(f'Unable to scrape posts -- Received {r.status_code} STATUS CODE')
            write_log(f'Unable to scrape posts -- Received {r.status_code} STATUS CODE')

    def action_posts(self):
        self.stop = True
        length = len(self.ids)
        if length:
            enum = enumerate(self.ids, 1)
            for c, post_id in enum:
                time.sleep(random.uniform(1, 1.1))
                with requests.Session() as s:
                    r = s.post(FAVORITE_URL.format(post_id, self.id, self.app_token), headers=self.headers)
                if r.ok:
                    print(f'Post {c} of {length} : Successfully {self.action}d', end='\r')
                    write_log(f'Post {c} of {length}  - URL : http://onlyfans.com/{post_id}/{self.username}/ - Action taken : {self.action}d')
                else:
                    self.log.error(f'Unable to action post {post_id} -- Received {r.status_code} STATUS CODE')
                    write_log(f'Unable to action post {post_id} of {self.username} due to error {r.status_code} - URL : http://onlyfans.com/{post_id}/{self.username}')

    def spinner(self):
        icons = [
            '(.    )',
            '(.o   )',
            '(.oO  )',
            '(.oOo )',
            '(.oOo.)',
            '(.oOo )',
            '(.oO  )',
            '(.o   )',
        ]
        while True:
            for icon in icons:
                print(icon, end='\r')
                if self.stop:
                    return None
                time.sleep(0.1)

def write_log(logmessage):
        curr_time = datetime.datetime.now()
        df = open("OF.log","a")
        df.write(f'{curr_time} - {logmessage}\n')
        df.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, help='Username of OnlyFans content creator')
    parser.add_argument('-w', '--whattodo', type=str, default = "like" , help='Action [like/unlike] to take on all wall posts of specified username')
    args = parser.parse_args()
    
    write_log("==================")    
    write_log("Start of Actioning")    

    onlyfans = OnlyFans(args)
    t1 = Thread(target=onlyfans.spinner)
    t1.start()
    onlyfans.scrape_user()
    onlyfans.scrape_posts()
    onlyfans.action_posts()

    write_log("End of Actioning")    
    write_log("================")    
    
if __name__ == '__main__':
    main()
