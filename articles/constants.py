class ArticleCategories(object):
    PROGRAMING = 'programing'
    SOFTWARE = 'software'
    THINKING = 'thinking'
    ENVIRONMENT = 'enviroment'
    LITERATURE = 'literature'


ARTICLE_CATEGORY_CHOICES = (
    (ArticleCategories.PROGRAMING, '编程'),
    (ArticleCategories.SOFTWARE, '软件'),
    (ArticleCategories.THINKING, '随想'),
    (ArticleCategories.ENVIRONMENT, '环境'),
    (ArticleCategories.LITERATURE, '文艺'),
)
