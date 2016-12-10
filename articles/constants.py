class ArticleCatalogs(object):
    PROGRAMING = 'programing'
    SOFTWARE = 'software'
    THINKING = 'thinking'


ARTICLE_CATALOG_CHOICES = (
    (ArticleCatalogs.PROGRAMING, '编程'),
    (ArticleCatalogs.SOFTWARE, '软件'),
    (ArticleCatalogs.THINKING, '随想'),
)
