import re

import requests
from bs4 import BeautifulSoup

movie_url = 'https://movie.douban.com/people/54019708/collect'
movie_data = {
    'start': 0,
    'sort': 'time',
    'rating': 'all',
    'filter': 'all',
    'mode': 'grid',
}
movie_html = requests.post(movie_url, movie_data).text
movie_soup = BeautifulSoup(movie_html, 'lxml')
movie_list = movie_soup.find(class_='grid-view').contents
movie_list = list(filter(('\n').__ne__, movie_list))
for item in movie_list:
    title = item.find('em').string
    cover_small_url = item.find('img')['src']
    cover_big_url = cover_small_url.replace('ipst', 'lpst')
    intro = item.find(class_='intro').string

    rate_re = re.compile(r"rating[0-5]-t")
    rate = re.findall(r'[0-5]+', item.find(class_=rate_re)['class'][0])[0]

    data = {
        'title': title,
        'cover_small_url': cover_small_url,
        'cover_big_url': cover_big_url,
        'intro': intro,
        'rate': rate,
    }
    print(item.find(class_='pic').a['href'])
