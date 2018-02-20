Lattice-encrypt (格子暗号)
============================
今話題の量子コンピュータ耐性を持つと言われる格子暗号を触ってみました。  
2次元またはN次元の格子暗号により暗号復号を行えます。

Work for Python3 (>=3.5)

詳細
----
* [koushi_angou.py](koushi_angou.py)  ２次元の格子暗号、外部ライブラリ必要無し
* [lattice_encrypt.py](lattice_encrypt.py)  N次元の格子暗号、Numpyが必要

実際にPythonで動かすことができますが、暗号学的に安全かわからないので実用にならないです。  
実際の所、鍵が大きすぎて使いづらい。

参考
----
* [量子コンピュータによる解読に耐えうる
『格子暗号』を巡る最新動向](http://www.imes.boj.or.jp/citecs/symp/16/ref3_seito.pdf)
* [格子と同種写像に関するアルゴリズムの
耐量子暗号への応用](http://coop-math.ism.ac.jp/files/231/1f220534ba6f84164f284c5134f6f4a2.pdf)

Author
-----
[@namuyan_mine](http://twitter.com/namuyan_mine/)

LICENCE
------
MIT
