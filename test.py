# # from weibo import Client
# #
# # API_KEY = '3596718401'
# # API_SECRET = 'cf42fafc2baeafdba0902a8bef893a1f'
# # REDIRECT_URI = 'http://127.0.0.1:8000/test'
# # c = Client(API_KEY, API_SECRET, REDIRECT_URI)
# # print(c.authorize_url)
# # # c.set_code('647d0955d4baf7ab376bb6f67028e88a')
# # # {'uid': '1576273817', 'access_token':'2.00PpsfiBHl96vDec787ef82ehJzEYB','expires_at': 1491418799, 'remind_in': '2621205'}
# #
# # token = {'uid': '1576273817', 'access_token': '2.00PpsfiBHl96vDec787ef82ehJzEYB', 'expires_at': 1491418799,
# #          'remind_in': '2621205'}
# #
# # print(token)
# #
# # c2 = Client(API_KEY, API_SECRET, REDIRECT_URI, token)
# # info = c2.post('statuses/update', visible=0, status='今天天气真好')
# #
# # print(info)
# import twitter
#
# api = twitter.Api(consumer_key='6O89zaoGQIDfgQdYhKzQ8JTex',
#                   consumer_secret='ht35sAqhWI7a6P6uizTvxZoQNgKEmSCMGLq8tXg06hhRhlpb2N',
#                   access_token_key='526877310-RsFdH1ceQE1hoxUXQzkB8JT0aPlFHsCLNPW7VlE3',
#                   access_token_secret='nvdf5vNH0eUo4JaT4OhtFtsnpXJu5GLX0Ake0syWHdZFw')
#
# statuses = api.GetUserTimeline(screen_name='realdonaldtrump', count=1)
#
# print(statuses)
from monitor.tasks import monitor_trump

monitor_trump()
