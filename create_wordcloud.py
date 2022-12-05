# ライブラリのインポート
from matplotlib.pyplot import text
from wordcloud import WordCloud
import csv
import MeCab
import collections

# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer

# import Container
stop_words = ['感じ','もう','し','ん','よう','ー','の','ー','ー'
                'そう', 'ない', 'いる', 'する', 'まま', 'よう',
              'てる', 'なる', 'こと', 'もう', 'いい', 'ある',
              'ゆく', 'れる', 'なっ', 'ちゃっ', 'ちょっ',
              'ちょっ', 'やっ', 'あっ', 'ちゃう', 'その', 'あの',
              'この', 'どの', 'それ', 'あれ', 'これ', 'どれ',
              'から', 'なら', 'だけ', 'じゃあ', 'られ', 'たら', 'のに',
              'って', 'られ', 'ずっ', 'じゃ', 'ちゃ', 'くれ', 'なんて', 'だろ',
              'でしょ', 'せる', 'なれ', 'どう', 'たい', 'けど', 'でも', 'って',
              'まで', 'なく', 'もの', 'ここ', 'どこ', 'そこ', 'さえ', 'なく',
              'たり', 'なり', 'だっ', 'まで', 'ため', 'ながら', 'より', 'られる', 'です']
DIR_NAME = "../speech_to_text_2121040"
VIEWLOG_DIR_PATH = DIR_NAME+"/VIEWLOG_FILE/"#ログを保存する場所

# CSVFILENAME ="./sr_copy"
mecab = MeCab.Tagger()
mecab.parse('')
# node = mecab.parseToNode(text)

tagger = MeCab.Tagger("-Ochasen")

def readCsv(openFileName):
    file = open(openFileName, 'r', encoding="utf-8")
    data = csv.reader(file)
    text = ""
    text2 = ""
    co = 0
    textsum1 = 0
    textsum2 = 0
    for row in data:
        co+=1
        # print(row[4])
        if(row[6]=="USER"):
            text = text+str(row[3])+" "
            textsum1 += int(row[5])

        else:
            text2 = text2+str(row[3])+" "
            textsum2 += int(row[5])
            
        # for col in row:
            # print(col)#, end=',')
            # text = text+str(col[3])
        # print()
    file.close()
    # print(co)
    # print(textsum1,textsum2)
    return text, text2

"""
def mecab_tt(text):    
    # 分かち書きのみ出力する設定にする
    # mecab = MeCab.Tagger("-Ochasen")
    # mecab = MeCab.Tagger("-Owakati")
    # mecab = MeCab.Tagger()
    # mecab.parse('')
    # node = mecab.parseToNode(text)
    # mecab = MeCab.Tagger('-Ochasen')
    # node = mecab.parseToNode(text)
 
    # tagger = MeCab.Tagger("-Ochasen")
    mecab.parse('')
    result = mecab.parseToNode(text)
    # print(result)
    # mecab.parse('')
    lines = result.split('\n')
    nounAndVerb = []#「名詞」と「動詞」を格納するリスト
    hinshiList = []
    for line in  lines:
        feature = line.split('\t')
        # print(feature)
        if len(feature) != 1: #'EOS'と''を省く
            info = feature[1].split(',')
            hinshi = info[0]
            if hinshi in ('名詞'):
                hinshiList.append(["名詞",feature[0]])
                if info[6]=="*":
                    nounAndVerb.append(info[0])
                else:
                    nounAndVerb.append(info[6])
            elif hinshi in ('動詞'): 
                hinshiList.append(["動詞", feature[0]])
            else:
                hinshiList.append(["その他", feature[0]])
    return hinshiList
"""

def get_noun(text,savefilename,hinshilist):
    #MeCabで形態素解析
    mecab = MeCab.Tagger('-Ochasen')
    node = mecab.parseToNode(text)
    words = []
    tt=""
    while node is not None:
        #品詞と品詞細分類１を抽出
        pos_type = node.feature.split(',')[0]
        subtype = node.feature.split(',')[1]

        # 品詞が名詞、品詞細分類１が一般のとき
        # if pos_type in["感動詞"]or["名詞"]or["フィラー"]or["形容詞"]:
        # if pos_type in["名詞"]:
        if pos_type in hinshilist:
            if node.surface not in stop_words:
                if pos_type in ["名詞"]:
                    if subtype in ['一般']:
                        words.append(node.surface)
                        tt = tt + str(node.surface)+" "
                else:
                    words.append(node.surface)
                    tt = tt + str(node.surface)+" "
                
        node = node.next
        # 出現数を集計し、ソート
        #   words_count = Counter(words)
        #   result = words_count.most_common()
    
    #単語の数カウント
    c = collections.Counter(words)
    word_count = c.most_common(100)
    print(word_count)
    # 
    # fl = open("choiced_count_deta.csv", 'a', encoding="utf_8", newline="")
    # w = csv.writer(fl)
    # for i in word_count:
    #     print(i[0],i[1])
    #     w = w.writerow(i[0],str(i[1]))
       
    # fl.close()
    # savefilename =  CSVFILENAME+"_count.csv"
    files = open(savefilename, 'a', encoding="utf_8", newline="")
    
    # 全体のファイルの保存
    for i in word_count:
        for j, contents in enumerate(i):
            if j==0:
                word_a = str(contents)
                # print(word_a)
            else:
                num_a = str(contents)
                # print(num_a)
        wo = csv.writer(files)
        wo = wo.writerow([str(word_a), str(num_a)])
    files.close()
    # print(c.most_common(100))
 
    return tt

# https://toukei-lab.com/python-mecab
# def tfidf(word_list):
#     docs = np.array(word_list)#Numpyの配列に変換する
#     #単語を配列ベクトル化して、TF-IDFを計算する
#     vecs = TfidfVectorizer(
#                 token_pattern=u'(?u)bw+b'#文字列長が 1 の単語を処理対象に含めることを意味します。
#                 ).fit_transform(docs)
#     vecs = vecs.toarray()
#     return vecs
# def cossim(v1,v2):
#     return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def create_word_cloud_for_file(CSVFILENAME):
    a = readCsv(CSVFILENAME+".csv")
    te=get_noun(a[0],CSVFILENAME+'_count_USER.csv')
    text2=get_noun(a[1],CSVFILENAME+'_count_PC.csv')
    
    # parse = tagger.parse(a[0])
    # parse = tagger.parse(a[1])
    # Windowsにインストールされているフォントを指定 
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/HGRSGU.TTC',width=500, height=500,stopwords=stop_words, max_words=30,background_color="white", colormap="summer")
    # wordcloud = WordCloud(width=1920, height=1080)
    # ワードクラウドの作成
    wordcloud.generate(te)
    # wordcloud.fit_words(text)
    # WindowsパソコンのPドライブ直下に画像を保存
    # wordcloud.to_file('wc.png') 
    wordcloud.to_file(CSVFILENAME+'USER.png') 

    wordcloud.generate(text2)
    # wordcloud.fit_words(text2)
    # wordcloud.to_file('./wc2.png') 
    wordcloud.to_file(CSVFILENAME+'PC.png') 

def create_choiced_wordcloud(word_only_data, save_file_name, hinshilist):
    
    def ggg(word_only_data):#PCとUserにテキスト分割する
        data = word_only_data
        text = ""
        text2 = ""
        co = 0
        # print(data)
        # その列がUSERなら
        for row in data:
            # print(row[0])
            if(row[0]=="USER"):
                text = text+str(row[1])+" "
                # textsum1 += int(row[5])
            else:
                text2 = text2+str(row[1])+" "
        return text, text2

    # a = readCsv("./sr.csv")
    a = ggg(word_only_data)
    te=get_noun(a[0],save_file_name+'_co_USER.csv',hinshilist)
    text2=get_noun(a[1],save_file_name+'_co_PC.csv',hinshilist)

    # vecs = tfidf(te)
    # print(vecs[1],vecs[0])
    # Windowsにインストールされているフォントを指定 
    # 縦書きの削除　prefer_horizontal=1
    wordcloud = WordCloud(
                font_path='C:/Windows/Fonts/HGRSGU.TTC',
                width=500, 
                height=500,
                stopwords=stop_words, 
                max_words=30,
                background_color="white", 
                prefer_horizontal=1,
                colormap="summer"
                )
    # wordcloud = WordCloud(width=1920, height=1080)
    # ワードクラウドの作成
    try:
        wordcloud.generate(te)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_USER.png') 
    except BaseException as e:
        print(e)
    try:
        wordcloud.generate(text2)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_PC.png') 
    except BaseException as e:
        print(e)
