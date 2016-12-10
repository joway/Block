import jieba.analyse


def topk(content, k):
    return jieba.analyse.extract_tags(content, topK=k, withWeight=False, allowPOS=())
