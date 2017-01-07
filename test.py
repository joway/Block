import feedparser

resp = feedparser.parse('https://imququ.com/rss.html')
for entry in resp['entries']:
    title = entry['title_detail']['value']
    created_at = entry['updated']
    print(created_at)
    link = entry['link']
    content = entry['summary_detail']['value']



