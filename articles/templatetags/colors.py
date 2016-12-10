import random

from . import register


@register.filter(is_safe=True)  # 注册template filter
def random_color(option):
    BASE_COLORS = ['light-blue', 'cyan', 'green', 'light-green', 'lime', 'orange',
                   'amber', 'yellow', 'deep-orange', 'blue', ]
    LIGHTENS = ['lighten-1', 'lighten-2', 'lighten-3', 'lighten-4', 'lighten-5']
    DARKENS = ['darken-1', 'darken-2', 'darken-3', 'darken-4', 'darken-5']
    if option == 'darken':
        return random.choice(BASE_COLORS) + ' ' + random.choice(DARKENS)
    elif option == 'lighten':
        return random.choice(BASE_COLORS) + ' ' + random.choice(LIGHTENS)
    else:
        return random.choice(BASE_COLORS)

