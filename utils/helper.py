import os
import pandas as pd
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import lil_matrix

_base_path = "{}/..".format(os.path.dirname(os.path.abspath(__file__)))


# 形態素解析の実行
def _default_filterfunc(t):
    if t.part_of_speech.split(',')[0] in ['助動詞', '助詞', '記号']:
        return False
    if t.part_of_speech.split(',')[1] in ['非自立', '接尾', '数']:
        return False
    if t.base_form in ['○', 'P', 'する', 'いる', 'アップ', 'アイドル', 'マスター']:
        return False
    return True


def tokenize_func(tokenizer, filter=_default_filterfunc):
    def tokenize(txt):
        tokenized = tokenizer.tokenize(txt)
        return [t.base_form for t in tokenized if filter(t)]

    return tokenize


# TF-IDFの計算
def tfidf(tokenized_list, top_n=20):
    def list2ssv(v):
        return ' '.join(v)

    df_ssv = tokenized_list.apply(list2ssv)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df_ssv)
    words = vectorizer.get_feature_names()

    lst = []
    for e in X:
        word_scores = [(words[v[0]], v[1]) for v in zip(e.indices, e.data)]
        lst.append(sorted(word_scores, key=lambda x: x[1] * -1)[0:top_n])
    return pd.Series(lst)


# TF-IDFの計算(単語リスト指定)
def tfidf_wordlist(tokenized_list: pd.Series, word_list):
    def list2ssv(v):
        return ' '.join(v)

    df_ssv = tokenized_list.apply(list2ssv)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df_ssv)
    words = vectorizer.get_feature_names()

    word_index = dict([(w, i) for i, w in enumerate(word_list)])

    def word_list_vector(e):
        word_scores = dict(
            [[word_index[words[v[0]]], v[1]] for v in zip(e.indices, e.data) if words[v[0]] in word_index])
        lvec = lil_matrix((1, len(word_index)))
        lvec[0, list(word_scores.keys())] = list(word_scores.values())
        return lvec.tocsr()

    return pd.Series([word_list_vector(e) for e in X])


def wordlist_top_n(tfidf_list, word_list, top_n=20):
    lst = [
        sorted([(word_list[v[0]], v[1]) for v in zip(e.indices, e.data)], key=lambda x: x[1] * -1)[0:top_n]
        for e in tfidf_list
    ]
    return pd.Series(lst)


# 学習済みWord2Vecモデルの取得
def w2v_pretrained_model():
    return gensim.models.Word2Vec.load('{}/data/word2vec/ja/ja.bin'.format(_base_path))
