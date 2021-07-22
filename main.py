import os
import requests
import time
import yaml
from datetime import datetime
from bs4 import BeautifulSoup

with open("config.yaml", 'r') as stream:
  try:
    config = yaml.safe_load(stream)
    delay = config['DELAY_IN_SECONDS']
    urls = config['SEARCH_RESULT_URLS']
  except yaml.YAMLError as exc:
    print(exc)

title_class = 'css-1f4mp12'
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


old_maps = [{} for _ in range(len(urls))]
iteration = 1
while True:
  print('Iteration', iteration, '-', current_time())

  for i in range(len(urls)):
    url = urls[i]
    old_map = old_maps[i]

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
      if iteration == 1:
        continue
      notify(title=price, message=title,  url=url)
      time.sleep(2)

    old_map = new_map

  iteration += 1
  time.sleep(delay)
