# view_log


## ターミナルやコマンドラインなどで以下のインストールが必要
~~~
$ pip install ttk 
$ pip install mecab
$ pip install wordcloud
$ pip install pandas
$ pip install matplotlib
~~~

## meca辞書のインストールが必要

### 1. ダウンロード

下記URLへアクセスします。
https://github.com/ikegami-yukino/mecab/releases
mecab-64-0.996.2.exeをクリックして、ダウンロードを開始します．
ファイルは、適当な場所に保存してください．


### 2. インストール

ダウンロードしたexeを起動し，「OK」をクリック．

#### 辞書の文字コードの選択
「UTF-8」を選択して、「次へ」をクリック．

#### 使用許諾契約書の同意
「同意する」にチェックを入れて、「次へ」をクリックします．

#### インストール先の指定
初期では「C:\Program Files\MeCab」が設定されています。
変更する場合は、存在するディレクトリに変更します。
そして、「次へ」をクリック。

#### プログラムグループの指定
「プログラムグループを作成しない」にチェックいれます。
Pythonから利用する上では、グループは必要ありません。
「次へ」をクリック。


#### インストール準備完了
インストール先を確認します。
問題なければ、「インストール」をクリック。

インストールが開始。
その途中で次のダイアログが出る場合は「OK」をクニック

### 3. パスの設定
環境変数にMeCabをインストールしたフォルダのパスを設定します。
今回は、「C:\soft\MeCab」にインストールしました。
そのため、設定するパスは「C:\soft\MeCab\bin￥」となります。

Windowsマークキーを押して「sysdm.cpl」と検索して、Enterを押してください。

#### システムのプロパティ
「詳細設定」のタブを開きます。
#### システムのプロパティ -  詳細設定
右下の環境変数を起動
システム環境変数の「Path」にMecabをインストールしたフォルダにある「bin」を指定します。

### 4. 確認

ターミナルやコマンドライン上で以下のコマンドを押下してバージョンが出てくればOK
~~~
$ mecab -v
~~~
-> mecab of 0.996ba

### 参考サイト
- 下記URLから「MecabのWindowsへのｚインストール」を行う（「PythonからMecabを利用する」の直前まで）
https://self-development.info/mecab%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%81%A6python%E3%81%A7%E4%BD%BF%E3%81%86%E3%80%90windows%E3%80%91/


