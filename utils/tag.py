import jieba.analyse


def topk(content, k):
    return jieba.analyse.textrank(content, topK=k, withWeight=False,
                                  allowPOS=('ns', 'nr', 'an', 'n', 'vn'))
