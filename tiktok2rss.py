#!/usr/bin/env python
# -*- coding: utf-8 -*-

def close_browser(sig, frame):
    browser.close()
#    browser.exit()

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import PyRSS2Gen, datetime
import sys, os, signal
import argparse

try:
  url = "https://www.tiktok.com/@" + sys.argv[1]
except IndexError:
  print(sys.argv[0] + " TikTok_Username [destination_folder]")
  sys.exit(1)


signal.signal(signal.SIGINT, close_browser)
signal.signal(signal.SIGTERM, close_browser)

try:
  browser = webdriver.Firefox()
  wait = WebDriverWait(browser, 10)
  browser.get(url)
  state_data = browser.execute_script("return window['SIGI_STATE']")
except Exception as e:
  close_browser(None, None)
  print(e)
  sys.exit(1)
close_browser(None, None)

items = list()

for video in state_data['ItemModule']:
  video_title=state_data['ItemModule'][video]['desc']
  video_url="https://www.tiktok.com/@" + state_data['ItemModule'][video]['author'] + "/video/" + state_data['ItemModule'][video]['id']
  video_time=state_data['ItemModule'][video]['createTime']
  video_contents="<img src='" + state_data['ItemModule'][video]['video']['cover'] + "'>"

  items.append(PyRSS2Gen.RSSItem(title = video_title,
                                 link = video_url,
                                 description = video_contents,
                                 guid = PyRSS2Gen.Guid(video_url),
                                 pubDate = datetime.datetime.fromtimestamp(int(video_time))))

rss = PyRSS2Gen.RSS2(
  title = "Latest TikTok videos from @" + sys.argv[1],
  link = url,
  description = state_data['UserModule']['users'][sys.argv[1]]['signature'],
  lastBuildDate = datetime.datetime.now(),
  items = items
)

try:
  rss.write_xml(open(os.path.join(sys.argv[2], sys.argv[1]+".xml"), "w"), encoding="utf-8")
except IndexError:
  rss.write_xml(open(sys.argv[1]+".xml", "w"), encoding="utf-8")
