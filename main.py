# Requirement:
# pip install beautifulsoup4
# brew install terminal-notifier ||OR|| sudo gem install terminal-notifier
import os
import requests
import time
import sys
from datetime import datetime
from bs4 import BeautifulSoup

title_class = 'css-18c4yhp'
price_class = 'css-rhd610'


def get_page_html(url):
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
  page = requests.get(url, headers=headers)
  return page.content


def get_products(url):
  page_html = get_page_html(url)
  soup = BeautifulSoup(page_html, 'html.parser')
  title_divs = soup.findAll("div", {"class": title_class})
  price_divs = soup.findAll("div", {"class": price_class})
  return [title_div.text for title_div in title_divs], [price_div.text for price_div in price_divs]


def notify(title, message, url):
  t = '-title {!r}'.format(title)
  m = '-message {!r}'.format(message)
  u = '-open {!r}'.format(url)
  os.system('terminal-notifier {}'.format(' '.join([m, t, u])))


def current_time():
  return datetime.now().strftime("%H:%M")


# How to use: py main.py DELAY_IN_SECONDS URL
# e.g.:
# py main.py 3 https://www.tokopedia.com/search?goldmerchant=true&ob=9&pmax=4000000&pmin=2500000&shop_tier=3&st=product&q=rx%20580
# py main.py 950 https://www.tokopedia.com/search?goldmerchant=true&ob=9&pmax=390000&pmin=285000&shop_tier=3&st=product&q=final%20fantasy%20remake%20ps4
# py main.py 1250 https://www.tokopedia.com/search?ob=9&pmax=530000&pmin=390000&st=product&q=miles%20morales%20ps4
delay = int(sys.argv[1])
url = str(sys.argv[2])
old_map = {}
first_time = True
while True:
  print(current_time())
  titles, prices = get_products(url)

  new_map = {}
  for i in range(len(titles)):
    new_map[titles[i]] = prices[i]

  diff_map = new_map.copy()
  for old_title, old_price in old_map.items():
    if old_title in diff_map and diff_map[old_title] == old_price:
      diff_map.pop(old_title, None)

  for title, price in diff_map.items():
    print(current_time(), price, title)
    if first_time:
      continue
    notify(title=price, message=title,  url=url)
    time.sleep(2)

  first_time = False
  old_map = new_map
  time.sleep(delay)
