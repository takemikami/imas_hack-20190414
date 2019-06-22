import os
import json
import hashlib
import requests
import time
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from bs4 import BeautifulSoup

_base_path = "{}/..".format(os.path.dirname(os.path.abspath(__file__)))
_cache_path = "{}/.cache".format(_base_path)


# キャッシュ機能
def clear_cache(group=None):
    import shutil
    if group is None:
        shutil.rmtree(_cache_path)
    else:
        shutil.rmtree("{}/{}".format(_cache_path, group))


def _digest_params(params):
    return hashlib.sha224('\t'.join(params).encode()).hexdigest()


def _get_from_cache(group, params):
    file_name = "{}/{}/{}".format(_cache_path, group, _digest_params(params))
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as f:
            return f.read()
    return None


def _put_to_cache(group, params, contents):
    os.makedirs("{}/{}".format(_cache_path, group), exist_ok=True)
    file_name = "{}/{}/{}".format(_cache_path, group, _digest_params(params))
    with open(file_name, mode='w') as f:
        f.write(contents)


# アイドル順データの取得
def idol_id():
    df = pd.read_csv("{}/data/master/idol_id.txt".format(_base_path), names=['label'])
    df['id'] = df.index
    return df


# im@sparqlからのデータ取得
def imasparql(query, endpoint='https://sparql.crssnky.xyz/spql/imas/query', cache=True):
    raw_json = _get_from_cache("imasparql", [query, endpoint])
    if raw_json is None:
        sparql = SPARQLWrapper(endpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        results = sparql.query().convert()
        _put_to_cache("imasparql", [query, endpoint], json.dumps(results))
    else:
        results = json.loads(raw_json)

    lst = []
    keys = results['head']['vars']
    for x in results['results']['bindings']:
        lst.append(dict([(k, x[k]['value']) if k in x else (k, "") for k in keys]))
    df = pd.read_json(json.dumps(lst), orient='records')
    return df


# ニコニコ大百科からのデータ取得
def niconico_dic(entries, cache=True):
    def get_entry_text(entry):
        raw_text = _get_from_cache("niconico_dic", [entry])
        if raw_text is None:
            url = "https://dic.nicovideo.jp/a/" + entry
            headers = {"User-Agent": "python requests"}
            time.sleep(3)
            resp = requests.get(url, timeout=10, headers=headers)
            raw_text = resp.text
            _put_to_cache("niconico_dic", [entry], resp.text)

        soup = BeautifulSoup(raw_text, "html5lib")

        txt_list = []
        p_list = soup.find_all("p")
        for ptxt in p_list:
            for txt in ptxt.text.split("\n"):
                if len(txt) > 0:
                    if not txt.startswith('※') and not txt.startswith('【'):
                        txt_list.append(txt)

        return '\n'.join(txt_list)

    text_list = []
    replace_map = {
        'エミリー': 'エミリー スチュアート',
        'ロコ': 'ロコ(アイドルマスター)',
        'ジュリア': 'ジュリア(アイドルマスター)',
    }
    for entry in entries:
        if entry in replace_map.keys():
            entry = replace_map[entry]
        text = get_entry_text(entry)
        text_list.append(text)
    return pd.DataFrame({'entry': entries, 'text': text_list})
