import copy

import jieba
import math

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

# 对str/unicode
normalize = lambda s: ''.join(filter(lambda x: x not in punct, s))


def cumulative(tokens, frequency):
    _frequency = copy.deepcopy(frequency)
    for t in tokens:
        _frequency[t] += 1
    return _frequency


def cosine_similarity(source, target):
    source = normalize(source)
    target = normalize(target)
    source_tokens = list(jieba.cut(source))
    target_tokens = list(jieba.cut(target))
    _frequency = {t: 0 for t in (set(source_tokens + target_tokens))}
    source_frequency = cumulative(source_tokens, _frequency)
    target_frequency = cumulative(target_tokens, _frequency)
    Si_Ti = 0
    Si_square = 0
    Ti_square = 0
    for k in source_frequency:
        Si_Ti += source_frequency[k] * target_frequency[k]
        Si_square += source_frequency[k] * source_frequency[k]
        Ti_square += target_frequency[k] * target_frequency[k]

    cosine = Si_Ti / (math.sqrt(Si_square) * math.sqrt(Ti_square))
    return cosine

if __name__ == '__main__':
    source = """
    我去上海交大看长者
    """

    target = """
    我去清华听演讲
    """

    print(cosine_similarity(source, target))
