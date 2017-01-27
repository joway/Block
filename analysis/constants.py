class ActivityType(object):
    COMMENT = '评论'
    POST = '发表'
    UPDATE = '更新'
    LOGIN = '登陆'


class ANALYSITICS_METRICS(object):
    PAGE_VIEW = 'ga:pageviews'
    SESSIONS = 'ga:sessions'
    USERS = 'ga:users'


ALL_METRICS = ','.join([ANALYSITICS_METRICS.__getattribute__(ANALYSITICS_METRICS, x) for x in ANALYSITICS_METRICS.__dict__ if x[:2] != '__'])
