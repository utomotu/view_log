# ライブラリのインポート
from matplotlib.pyplot import text
from wordcloud import WordCloud
import csv
import MeCab
import collections
import random

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
              'たり', 'なり', 'だっ', 'まで', 'ため', 'ながら', 'より', 'られる', 'です' ,'風','気','別','人','粘']
print(sorted(stop_words))
DIR_NAME = "../speech_to_text_2121040"
VIEWLOG_DIR_PATH = DIR_NAME+"/VIEWLOG_FILE/"#ログを保存する場所
WCCONTETSLOG_PATH = DIR_NAME+"/WC_RESULT/"

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

def get_noun(text ,hinshilist):
    #MeCabで形態素解析
    mecab = MeCab.Tagger('-Ochasen')
    # print("text")
    # print(text)
    node = mecab.parseToNode(text)
    words = []
    tt=""
    firaCheck = False
    tmpword = "keyword"
    firadt = {}
    firanextWordtext = ""
    while node is not None:
        #品詞と品詞細分類１を抽出
        pos_type = node.feature.split(',')[0]
        subtype = node.feature.split(',')[1]

        # 品詞が名詞、品詞細分類１が一般のとき
        # if pos_type in["感動詞"]or["名詞"]or["フィラー"]or["形容詞"]:
        # if pos_type in["名詞"]:
        
        if node.surface not in stop_words:
            #フィラーの次の単語を取得する（品詞FULL選択時のみ適用可能）
            # if pos_type not in ["助詞"] or ["助動詞"]:
            if firaCheck:
                # print(node.surface)
                if pos_type in ["助詞"]:
                    firaCheck=True
                elif pos_type in ["助動詞"]:
                    firaCheck=True
                elif pos_type in ["接頭詞"]:
                    firaCheck=True
                elif pos_type in ["記号"]:
                    firaCheck=True
                elif pos_type in ["その他"]:
                    firaCheck=True
                else:
                    try:
                        firadt[tmpword] += str(node.surface)+' '  
                    except:
                        firadt[tmpword] = str(node.surface)+' '  
                    
                    firanextWordtext += str(node.surface)+' '
                    firaCheck=False
            if pos_type in ["フィラー"]:
                tmpword = node.surface
                firaCheck=True
    
            if pos_type in hinshilist:
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
    print(   "nextfira")
    print(firadt)
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
    
    # print(c.most_common(100))
 
    return tt,word_count, firanextWordtext

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

def create_word_cloud_for_file(CSVFILENAME):
    a = readCsv(CSVFILENAME+".csv")
    te=get_noun(a[0])
    text2=get_noun(a[1])
    
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
    UU = get_noun(t[0],hinshilist)
    PP = get_noun(t[1],hinshilist)
    ALL = get_noun(t[2],hinshilist)
    # UU[2] #"   " フィラーの後の単語のみ
    teUSER = UU[0]
    # print("teUSER")
    # print(teUSER)
    # print(UU[1])


    wordcountUSER = UU[1]    
    wordcountPC   = PP[1]#[('あと', 18), ('人', 12), ...  ]
    
    worddictUser = {}; worddictPC = {}; del_wordcount_PC = {}; del_wordcount_USERs = {}    

    files = open(WCCONTETSLOG_PATH+save_file_name+"US.csv", 'a', encoding="utf_8", newline="")
    # 全体のファイルの保存
    for contents in UU[1]:
        wo = csv.writer(files)
        wo = wo.writerow([str(contents[0]), str(contents[1])])
        # WC入力用辞書型の頻度リスト
        worddictUser[contents[0]] = contents[1]
        del_wordcount_USERs[contents[0]] = contents[1] 
    files.close()

    files = open(WCCONTETSLOG_PATH+save_file_name+"PC.csv", 'a', encoding="utf_8", newline="")
    # 全体のファイルの保存
    for contents in PP[1]:
        wo = csv.writer(files)
        wo = wo.writerow([str(contents[0]), str(contents[1])])
        # WC入力用辞書型の頻度リスト
        worddictPC[contents[0]] = contents[1]
        del_wordcount_PC[contents[0]] = contents[1]
    files.close()
    # print("wordcountUSER")
    # print(worddictUser)
    # print("wordcountPC")
    # print(worddictPC)

    wordcount_common = {}#
    
    for i, wspc in enumerate(wordcountPC):
        # print(wspc)
        for j, weuser in enumerate(wordcountUSER):
            # print(weuser)
            if wspc[1]>1 and weuser[1]>1 and wspc[0] == weuser[0]:#単語情報が一致かつ出現回数1以上なら
                cc = int(wspc[1])+int(weuser[1])
                wordcount_common[wspc[0]] = cc
               
            # if wspc[1]>1 and weuser[1]>1 and wspc[0] != weuser[0]:#単語情報が一致かつ出現回数1以上なら:
            #     del_wordcount_PC[wspc[0]] = int(wspc[1])
            #     del_wordcount_USERs[weuser[0]] = int(weuser[1])
    print("wordcount_common")
    print(wordcount_common)
    #　合致する単語はPC,USERからそれぞれ抜き取りを行う
    for key, value in wordcount_common.items():
        if key in del_wordcount_PC:
            del del_wordcount_PC[key]

    for key, value in wordcount_common.items():
        if key in del_wordcount_USERs:
            del del_wordcount_USERs[key]

    
    def pos_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None,**kwargs):
        # 品詞取得
        print("hinshilist")
        # print(list(hinshilist))
        for i in list(hinshilist):
            # rgb = cmap(color_index)
            # return mcolors.rgb2hex(rgb)
            pos_color_index_dict[i] = len(pos_color_index_dict)
        print("pos_color_index_dict")
        print(pos_color_index_dict)
        color_index = pos_color_index_dict[hinshilist]
        print("color_index")
        print(color_index)

        # pos = get_pos(word)
        # 初登場の品詞の場合は辞書に追加
        # if pos not in pos_color_index_dict:
            # pos_color_index_dict[pos] = len(pos_color_index_dict)
        # color_index = pos_color_index_dict[pos]
        # カラーマーップでrgbに変換
        rgb = cmap(color_index)
        return mcolors.rgb2hex(rgb)

    # pos_color_func()
    def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        # 0,128,0 緑色
        
        h = int(139) # h = int(360.0 * 21.0 / 255.0)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(random.randint(60, 120)) / 255.0)
        # https://www.frontier.maxell.co.jp/blog/posts/32.html
        # H色相　S彩度　L輝度
        return "hsl({}, {}%, {}%)".format(h, s, l)

    color_func = random_color_func
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
                # colormap = color_func
                color_func=color_func
    )
    # wordcloud = WordCloud(width=1920, height=1080)
    # ワードクラウドの作成
    wws = 500
    # if swith_v_value:
    #     print("bTEtUser")
    #     print(teUSER)
    #     print("bcommon")
    #     print(wordcount_common)
    #     print(wordcount_common)
    #     teUSER = sorted(teUSER)
    #     tePC = sorted(tePC)
    #     wordcount_common = sorted(wordcount_common)
    #     print("acommon")
    #     print(teUSER)
    #     print("acommon")
    #     print(wordcount_common)
    
    ######################################################################
    # フィラー語の単語PC/USER側のワードクラウド生成　単語が何も無ければ白紙を生成
    ######################################################################
    try:
        wordcloud.generate(UU[2])#["test test test "]
        # wordcloud.generate_from_frequencies(worddictUser)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'firac_USER_.png') # inputstyle:{'やばい': 29, 'まずい': 17, '強い': 16, '難しい': 11, 'よかっ': 10, '厳しい': 5, '早く': 6, 'すごい': 12}
        wordcloud.to_file(WCCONTETSLOG_PATH+save_file_name+'_fira_USER.png') 
        
    except BaseException as e:
        # img = Image.new("L", (wws, wws), 255)
        # img.save(VIEWLOG_DIR_PATH+'checed_USER_fira.png')
        print(e)
    try:
        wordcloud.generate(PP[2])#["test test test "]
        # wordcloud.generate_from_frequencies(worddictUser)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'fira_PC.png') # inputstyle:{'やばい': 29, 'まずい': 17, '強い': 16, '難しい': 11, 'よかっ': 10, '厳しい': 5, '早く': 6, 'すごい': 12}
        wordcloud.to_file(WCCONTETSLOG_PATH+save_file_name+'_fira_PC.png') 
        
    except BaseException as e:
        # img = Image.new("L", (wws, wws), 255)
        # img.save(VIEWLOG_DIR_PATH+'checed_USER.png')
        print(e)
    ######################################################################
    # USER側のワードクラウド生成　単語が何も無ければ白紙を生成
    ######################################################################
    try:
        # wordcloud.generate(teUSER)#["test test test "]
        wordcloud.generate_from_frequencies(worddictUser)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'USER_from_frequencies.png')
        wordcloud.fit_words(worddictUser)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'USER_fit_word.png')
        wordcloud.generate(teUSER)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'USER_generate.png')
        wordcloud.generate_from_text(teUSER)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'USER_generate_from_text.png')

        wordcloud.generate_from_frequencies(worddictUser)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_USER.png') # inputstyle:{'やばい': 29, 'まずい': 17, '強い': 16, '難しい': 11, 'よかっ': 10, '厳しい': 5, '早く': 6, 'すごい': 12}
        wordcloud.to_file(WCCONTETSLOG_PATH+save_file_name+'_USER.png') 
        
    except BaseException as e:
        img = Image.new("L", (wws, wws), 255)
        img.save(VIEWLOG_DIR_PATH+'checed_USER.png')
        print(e)
    ######################################################################
    # PC側のワードクラウド生成　単語が何も無ければ白紙を生成
    ######################################################################
    try:
        # wordcloud.generate(tePC)
        wordcloud.generate_from_frequencies(worddictPC)
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_PC.png') 
        wordcloud.to_file(WCCONTETSLOG_PATH+save_file_name+'_PC.png') 
    except BaseException as e:
        img = Image.new("L", (wws, wws), 255)
        img.save(VIEWLOG_DIR_PATH+'checed_PC.png')
        
        print(e)
    ######################################################################
    # 共通単語のワードクラウド生成　単語が何も無ければ白紙を生成
    ######################################################################
    try:
        # wordcloud.fit_words(wordcount_common)
        wordcloud.generate_from_frequencies(wordcount_common) 
        wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_common.png') 
        wordcloud.to_file(WCCONTETSLOG_PATH+save_file_name+'_Common.png')
    except BaseException as e:
        # 何も生成されない時は
        img = Image.new("L", (wws, wws), 255)
        img.save(VIEWLOG_DIR_PATH+'checed_common.png')
        img.save(WCCONTETSLOG_PATH+save_file_name+'_Common.png') 
        print(e)
    ######################################################################
    # 共通単語の抜き取りがONなら，USER/PCから共通単語を抜いたワードクラウドを生成しなおす
    ######################################################################
    if switch_view:
        print("delet word cloud USER/PC")
        print(del_wordcount_USERs)
        print(del_wordcount_PC)
        try:
            # del_wordcount_USERs={'確か': 1, '一応': 2, 'すぐ': 2, 'もしか': 2, 'なぜ': 2, 'まあ': 2, 'そろそろ': 2, 'ますます': 2, 'ガンガン': 2, 'ブツブツ': 2, 'ほとんど': 2, 'やっぱり': 2, '少し': 2, 'さ': 2, 'もしや': 2, 'なんとなく': 2, 'よく': 2, 'どうも': 2, 'まず': 2, 'もうすぐ': 2, 'もっと': 2, 'おいおい': 2, 'だいたい': 2, 'ピッ': 2, 'さすが': 2, 'とりあえず': 2, '何で': 2, 'さらに': 2, 'よろしく': 2}
            wordcloud.generate_from_frequencies(del_wordcount_USERs)
            # wordcloud.fit_words(del_wordcount_USERs)
            # wordcloud.generate_from_frequencies(worddictUser)
            wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_USER.png') 
        except BaseException as e:
            img = Image.new("L", (wws, wws), 255)
            img.save(VIEWLOG_DIR_PATH+'checed_USER.png')
            print(e)
        try:
            wordcloud.generate_from_frequencies(del_wordcount_PC)
            # wordcloud.fit_words(del_wordcount_PC)
            wordcloud.to_file(VIEWLOG_DIR_PATH+'checed_PC.png') 
        except BaseException as e:
            img = Image.new("L", (wws, wws), 255)
            img.save(VIEWLOG_DIR_PATH+'checed_PC.png')
            print(e)

    return UU[1], PP[1]
