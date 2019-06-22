# imas_hack-20190414

このリポジトリは、  
2019/04/14に開催された「技術書典6」で頒布した「週刊IM@Study 2019年4月号」に掲載した記事  
『何つながりなのかな？を探る自然言語処理 ～765PRO LIVE THEATERに通りがかる小日向美穂～』の  
関連ソースコードを格納しています。

※参照しているデータに差があるため、書籍掲載の内容と結果に差異があります。

技術書典6  
2019.04.14 @ 池袋サンシャインシティ2F 展示ホールD  
https://techbookfest.org/event/tbf06

IM@Study | 技術書典6「か48」  
https://techbookfest.org/event/tbf06/circle/54670006

「何つながりなのかな？」を探る自然言語処理  
 ～765PRO LIVE THEATERに通りがかる小日向美穂～  
https://takemikami.com/2019/02/21/765PRO-LIVE-THEATER.html


## セットアップ

venvで仮想環境を作成し、切り替えます。

```
$ python3 -m venv venv
$ . venv/bin/activate
```

必要となるライブラリをインストールします。

```
(venv) $ pip install -r requirements.txt
```

Word2Vecの学習済みモデルを、data/word2vec配下に配置します。  
以下から``Japanese(w)``をダウンロードします。

Pre-trained word vectors  
https://github.com/Kyubyong/wordvectors


## 実行方法

```
(venv) $ jupyter notebook
```

jupyter notebookから、以下を実行します。

- tfidf.pynb
- logistic_regression.ipynb

注: 初回実行時はデータ取り込むので、かなり処理時間がかかります。


## ファイルの説明

- tfidf.pynb ... TF-IDF計算のNotebook
- logistic_regression.ipynb ... ロジスティック回帰のNotebook
- data
   - master ... マスターデータ（アイドル順データ）
   - word2vec ... Word2Vecの学習済みモデルの格納先
- utils
   - datasource.py ... im@sparql, ニコニコ大百科からデータを取り込む関数群
   - helper.py ... その他の補助関数群
