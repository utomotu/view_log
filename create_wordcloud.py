# ライブラリのインポート
from matplotlib.pyplot import text
from wordcloud import WordCloud
import csv
import MeCab
import collections

from PIL import Image

# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer

# import Container
stop_words = ['れ','て','感じ','もう','し','ん','よう','ー','の','ー','ー'
                'そう', 'ない', 'いる', 'する', 'まま', 'よう',
              'てる', 'なる', 'こと', 'もう', 'いい', 'ある',
              'ゆく', 'れる', 'なっ', 'ちゃっ', 'ちょっ',
              'ちょっ', 'やっ', 'あっ', 'ちゃう', 'その', 'あの','あと',
              'この', 'どの', 'それ', 'あれ', 'これ', 'どれ',
              'から', 'なら', 'だけ', 'じゃあ', 'られ', 'たら', 'のに',
              'って', 'られ', 'ずっ', 'じゃ', 'ちゃ', 'くれ', 'なんて', 'だろ',
              'でしょ', 'せる', 'なれ', 'どう', 'たい', 'けど', 'でも', 'って',
              'まで', 'なく', 'もの', 'ここ', 'どこ', 'そこ', 'さえ', 'なく',
              'たり', 'なり', 'だっ', 'まで', 'ため', 'ながら', 'より', 'られる', 'です' ,'風','気','別','人']
print(sorted(stop_words))
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
    word_count = c.most_common(100)#[('あと', 18), ('人', 12), ('スペシャル', 12),....]
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
 
    return tt,word_count

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

# @lru_cache(maxsize=None)
def get_pos(word):
    parsed_lines = tagger.parse(word).split("\n")[:-2]
    features = [l.split('\t')[1] for l in parsed_lines]
    pos = [f.split(',')[0] for f in features]
    pos1 = [f.split(',')[1] for f in features]

    # 名詞の場合は、 品詞細分類1まで返す
    if pos[0] == "名詞":
        return f"{pos[0]}-{pos1[0]}"

    # 名詞以外の場合は 品詞のみ返す
    else:
        return pos[0]
        
import matplotlib.cm as cm
import matplotlib.colors as mcolors
######################################
# 頻出度で単語色を分ける
######################################
# # これが単語ごとに色を戻す関数
# 品詞ごとに整数値を返す辞書を作る
pos_color_index_dict = {}
# カラーマップ指定
cmap = cm.get_cmap("tab20")
def pos_color_func(word, font_size, position, orientation, random_state=None,
                   **kwargs):
    # 品詞取得
    pos = get_pos(word)
    # 初登場の品詞の場合は辞書に追加
    if pos not in pos_color_index_dict:
        pos_color_index_dict[pos] = len(pos_color_index_dict)
    color_index = pos_color_index_dict[pos]
    # カラーマーップでrgbに変換
    rgb = cmap(color_index)
    return mcolors.rgb2hex(rgb)

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

def create_choiced_wordcloud(word_only_data, save_file_name, hinshilist,switch_view, swith_v_value):
    ######################################
    # 3種（PC, USER, common）のWordCloud生成
    ######################################
    def ggg(word_only_data):
        data = word_only_data
        tPC = "";tUSER = "";tAll=""
        
        for row in data:
            if(row[0]=="USER"):# その列がUSERなら
                tUSER += str(row[1])+" "
                tAll +=  str(row[1])+" "
            else:# その列がPCなら
                tPC += str(row[1])+" "
                tAll +=  str(row[1])+" "
        return tUSER, tPC, tAll
    t = ggg(word_only_data)#PCとUserにテキスト分割する
    UU = get_noun(t[0],save_file_name+'_co_USER.csv',hinshilist)
    PP = get_noun(t[1],save_file_name+'_co_PC.csv',hinshilist)
    ALL = get_noun(t[2],save_file_name+'_co_ALL.csv',hinshilist)
    
    # print(ALL)
    teUSER = UU[0] #
    tePC   = PP[0]
    wordcountUSER = UU[1]
    wordcountPC   = PP[1]#[('あと', 18), ('人', 12), ...  ]

    wordcount_common = {};del_wordcount_PC = {};del_wordcount_USERs = {}
    print("USER")
    print(UU)
    print("PC")
    print(PP)
    
    # print(word_only_data)
    # for i, wspc in enumerate(ALL[1]):
        # print(wspc)

    for i, wspc in enumerate(wordcountPC):
        # print(wspc)
        for j, weuser in enumerate(wordcountUSER):
            # print(weuser)
            if wspc[1]>1 and weuser[1]>1 and wspc[0] == weuser[0]:#単語情報が一致かつ出現回数1以上なら
                cc = int(wspc[1])+int(weuser[1])
                wordcount_common[wspc[0]] = cc
                # print(wordcount_common)
            if wspc[1]>1 and weuser[1]>1 and wspc[0] != weuser[0]:#単語情報が一致かつ出現回数1以上なら:
                del_wordcount_PC[wspc[0]] = int(wspc[1])
                del_wordcount_USERs[weuser[0]] = int(weuser[1])

    #　合致する単語はPC,USERからそれぞれ抜き取りを行う
    for key, value in wordcount_common.items():
        if key in del_wordcount_PC:
            del del_wordcount_PC[key]

    for key, value in wordcount_common.items():
        if key in del_wordcount_USERs:
            del del_wordcount_USERs[key]
            # print(key)


    # print(del_wordcount_PC)
    # print(del_wordcount_USERs)
    # print(wordcount_common)

    
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
    wws = 500
    # if swith_v_value:
    #     print("bTEtUser")
    #     print(teUSER)
    #     print("bcommon")
    #     print(wordcount_common)
    #     teUSER = sorted(teUSER)
    #     tePC = sorted(tePC)
    #     wordcount_common = sorted(wordcount_common)
    #     print("acommon")
    #     print(teUSER)
    #     print("acommon")
    #     print(wordcount_common)
    try:
        wordcloud.generate(teUSER)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_USER.png') 
    except BaseException as e:
        img = Image.new("L", (wws, wws), 255)
        img.save(VIEWLOG_DIR_PATH+'checed_USER.png')
        
        print(e)
    try:
        wordcloud.generate(tePC)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_PC.png') 
    except BaseException as e:
        img = Image.new("L", (wws, wws), 255)
        img.save(VIEWLOG_DIR_PATH+'checed_PC.png')
        
        print(e)
    try:
        wordcloud.fit_words(wordcount_common)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_AndValue.png') 
    except BaseException as e:
        # 何も生成されない時は
        img = Image.new("L", (wws, wws), 255)
        img.save(VIEWLOG_DIR_PATH+'checed_AndValue.png')
        print(e)
    if switch_view:
        try:
            wordcloud.fit_words(del_wordcount_USERs)
            wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_USER.png') 
        except BaseException as e:
            img = Image.new("L", (wws, wws), 255)
            img.save(VIEWLOG_DIR_PATH+'checed_USER.png')
            print(e)
        try:
            wordcloud.fit_words(del_wordcount_PC)
            wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_PC.png') 
        except BaseException as e:
            img = Image.new("L", (wws, wws), 255)
            img.save(VIEWLOG_DIR_PATH+'checed_PC.png')
            
            print(e)
    return ALL
