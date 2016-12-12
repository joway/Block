class ArticleCatalogs(object):
    PROGRAMING = 'programing'
    SOFTWARE = 'software'
    THINKING = 'thinking'
    ENVIRONMENT = 'enviroment'
    LITERATURE = 'literature'


ARTICLE_CATALOG_CHOICES = (
    (ArticleCatalogs.PROGRAMING, '编程'),
    (ArticleCatalogs.SOFTWARE, '软件'),
    (ArticleCatalogs.THINKING, '随想'),
    (ArticleCatalogs.ENVIRONMENT, '环境'),
    (ArticleCatalogs.LITERATURE, '文艺'),
)
