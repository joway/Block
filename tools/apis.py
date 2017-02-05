import re

import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from tools.serializers import DoubanExportSerializer


class ToolsViewSet(viewsets.ViewSet):
    @list_route(methods=['GET'])
    def douban(self, request, *args, **kwargs):
        serializer = DoubanExportSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        douban_id = serializer.validated_data['douban_id']

        _cache = cache.get('douban#%s' % douban_id)
        if _cache:
            return Response(data=_cache, status=status.HTTP_200_OK)

        movie_url = 'https://movie.douban.com/people/%s/collect' % douban_id
        movie_data = {
            'start': 0,
            'sort': 'time',
            'rating': 'all',
            'filter': 'all',
            'mode': 'grid',
        }
        movie_html = requests.post(movie_url, movie_data).text
        movie_soup = BeautifulSoup(movie_html, 'lxml')
        movies = []
        pages = int(movie_soup.find(class_='thispage')['data-total-page'])

        for i in range(pages):
            movie_data['start'] += i * 15
            movie_html = requests.post(movie_url, movie_data).text
            movie_soup = BeautifulSoup(movie_html, 'lxml')

            movie_list = movie_soup.find(class_='grid-view').contents
            movie_list = list(filter(('\n').__ne__, movie_list))

            for item in movie_list:
                cover_small_url = item.find('img')['src']
                cover_big_url = cover_small_url.replace('ipst', 'lpst')
                intro = item.find(class_='intro').string

                movies.append({
                    'title': item.find('em').string,
                    'cover_small_url': cover_small_url,
                    'cover_big_url': cover_big_url,
                    'intro': intro,
                    'link': item.find(class_='pic').a['href']
                })

        cache.set('douban#%s' % douban_id, movies, 3600)
        return Response(data=movies, status=status.HTTP_200_OK)
