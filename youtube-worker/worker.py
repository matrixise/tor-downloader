#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# youtube_dl worker
#

import logging
import os
import redis
import time
import youtube_dl


def download(url):

    def hook(info):

        now = int(time.time())
        status = info['status']

        if status == 'downloading':
            rdb.zadd('running', {now: 1, url: 2})
        elif status == 'error':
            rdb.zrem('running', url)
            rdb.zadd('error', {now: 1, url: 2})
        elif status == 'finished':
            rdb.zrem('running', url)
            rdb.zadd('finished', {now: 1, url: 2})

    if rdb.zrank('finished', url) != None:
        logging.warning('This video already exists.')
        return False

    try:
        opts = {
            'format': os.getenv('FORMAT', 'best'),
            # 'outtmpl': unicode(os.getenv('OUTTMPL', '%(title)s-%(id)s.%(ext)s'), 'utf-8'),
            'progress_hooks': [hook],
            # 'writeinfojson': True,
            'proxy': 'socks5://tor:9150'
        }
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as ex:
        logging.error('error: %s', ex)
        rdb.zrem('running', url)
        rdb.zadd('error', {int(time.time()): 1, url: 2})
        return False

    return True


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%FT%T', level='INFO')
    logging.info('connect redis')
    rdb = redis.StrictRedis(host='redis', db=os.getenv('DATABASE', 0),  password=os.getenv('PASSWORD'))
    rdb.ping()

    while True:
        try:
            _, url = rdb.brpop('pending')
            logging.info('process: %s', url)
            ok = download(url.decode('utf-8'))
            logging.info('success: %s', ok)
        except Exception as ex:
            logging.error('error: %s', ex)

