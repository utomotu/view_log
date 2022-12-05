# CSVファイルの文字化け
# https://qiita.com/devrookiecom/items/faf2b6ee6f9e058022cc
# 書き込みで謎の改行が入る
# https://qiita.com/ryokurta256/items/defc553f5165c88eac95

import csv
import os

import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from janome.tokenizer import Tokenizer
import pandas as pd
import create_wordcloud as cw

hinshi_list = ["その他", "感動詞", "記号", "形容詞", "名詞", "助詞", "助動詞", "接続詞", "接頭詞", "動詞", "副詞", "連体詞"] #抽象的なリストの「漫画」の具体例
# hinshi_list = ["その他", "感動詞", "記号", "形容詞", "名詞",] #抽象的なリストの「漫画」の具体例

def addwriteCsv(date, time, contents, openFileName = "csvTes.csv"):
    file = open(openFileName, 'a', newline="")
    w = csv.writer(file)
    w = w.writerow([date,time,contents])
    file.close()

class read_csv():
    def __init__(self, filename):   
        self.result_data = []
        self.full_data =[]#CSVのfullデータ

        self.day = [] # fullデータのうち日付のみのデータ（重複無し）
        self.windowOB = []## fullデータのうちwindoeのみのデータ（重複無し）
        self.speaker = [] # USER OR PCのみのデータ（重複無し）
        self.USER_amout = 0
        self.PC_amout = 0
        self.filepath = filename
        # self.
        # path のうちファイルネームと拡張子に分割
        path = (os.path.basename(filename))
        filename, fileext = os.path.splitext(os.path.basename(path))
        self.open_filename = filename
        self.fileext = fileext
        # 読み込んでself.day,  self.windowOB ,self.speakerに重複無しデータの挿入
        self.readCsv(self.filepath)
    def re_init(self, filename):
        self.result_data = []
        self.full_data =[]#CSVのfullデータ

        self.day = [] # fullデータのうち日付のみのデータ（重複無し）
        self.windowOB = []## fullデータのうちwindoeのみのデータ（重複無し）
        self.speaker = [] # USER OR PCのみのデータ（重複無し）
        self.USER_amout = 0
        self.PC_amout = 0
        self.filepath = filename
        # self.
        # path のうちファイルネームと拡張子に分割
        path = (os.path.basename(filename))
        filename, fileext = os.path.splitext(os.path.basename(path))
        self.open_filename = filename
        self.fileext = fileext
        # 読み込んでself.day,  self.windowOB ,self.speakerに重複無しデータの挿入
        self.readCsv(self.filepath)

    def hinsh_list(self, hinshilist,save_file_name):
        word_only_data = [[]]
        word_only_data.clear()
        for row in enumerate(self.full_data):
            # if i in choiced_iterate:
            # if(row[3]!=""):
            self.result_data.append(row[1][:5]+":"+row[6]+":"+row[3])
            word_only_data.append([row[6],row[3]])
        cw.create_choiced_wordcloud(word_only_data,save_file_name,hinshilist)
        return self.result_data

    def compar_list(self, list,save_file_name):

        choiced_day = set(list) & set(self.day)
        choiced_windowOB = set(list) & set(self.windowOB)
        choiced_speaker = set(list) & set(self.speaker)
        choiced_hinshi =set(list) & set(hinshi_list) 
        # print(choiced_day,choiced_wa)
        choiced_day = sorted(choiced_day)
        choiced_speaker = sorted(choiced_speaker)
        # print(self.full_data[0][0])
        
        choiced_iterate_day=[]
        choiced_iterate_wa=[]
        choiced_iterate_winob=[]

        for j, row in enumerate(self.full_data):
            for i, col in enumerate(row):
                # col[0]などで特定の要素をだす
                if i == 1 and col[:2] in choiced_day:
                    choiced_iterate_day.append(int(j))
                if i == 6 and col in choiced_speaker:
                    choiced_iterate_wa.append(int(j))
                if i == 7 and col in choiced_windowOB:
                    choiced_iterate_winob.append(int(j))
        if not choiced_iterate_day or not choiced_iterate_wa:# どちらかが片方ならば or 
            choiced_iterate = set(choiced_iterate_day) or set(choiced_iterate_wa)  or set(choiced_iterate_winob)
            print("OR")
        else: # 両方とも何かが入っていれば
            choiced_iterate = set(choiced_iterate_day) & set(choiced_iterate_wa) & set(choiced_iterate_winob)
            print("AND")
        # result_data = []
        self.result_data.clear()
        word_only_data = [[]]
        word_only_data.clear()
        
        self.USER_amout = 0
        self.PC_amout = 0
        # 選択された時刻の行のみ取り出してword_only_dataにappendする
        for i, row in enumerate(self.full_data):
            if i in choiced_iterate:
                if(row[3]!=""):
                    self.result_data.append(row[1][:5]+":"+row[6]+":"+row[3])
                    word_only_data.append([row[6],row[3]])
                    if(row[6]=="PC"):
                        self.PC_amout += int(row[5])
                        # print(str(row[5]))
                    else:
                        self.USER_amout += int(row[5])
                        # print((row[5]))

        print("choiced_PCword_amount:"+str(self.PC_amout))
        print("choiced_USERword_amount:"+str(self.USER_amout))
        
        cw.create_choiced_wordcloud(word_only_data,save_file_name, choiced_hinshi)
        
        return self.result_data

    def get_day(self):
        return self.day
    def get_windowOB(self):
        return self.windowOB
    def get_wa(self):
        return self.speaker
    def get_result_data(self):
        return self.result_data

    def readCsv(self, openFileName):
        
        def dbc():
            self.day=set(self.day)
            self.windowOB=set(self.windowOB)
            self.speaker=set(self.speaker)
            
            self.day=sorted(self.day)
            self.windowOB=sorted(self.windowOB)
            self.speaker=sorted(self.speaker)

        file = open(openFileName, 'r', encoding="utf_8")
        data = csv.reader(file)
        for row in data:
            self.full_data.append(row)
            try:
                if(row[3]!=""):
                    self.result_data.append(row[1][:5]+":"+row[6]+":"+row[3])
                    # テキストボックス用FULLデータの挿入
            except BaseException as e:
                print(e)
            for i, col in enumerate(row):
                if i == 1:#日付
                    self.day.append(col[:2])
                if i == 6:#発話内容
                    self.speaker.append(col)
                if i == 7:#WINDOW名
                    self.windowOB.append(col)
        file.close()
        dbc()   

    # 分かち書きを入手 
    def mecab_owakati(self):
        # 分かち書きのみ出力する設定にする
        # mecab = MeCab.Tagger("-Ochasen")
        # mecab = MeCab.Tagger("-Owakati")
        # mecab = MeCab.Tagger()
        # mecab.parse('')
        # node = mecab.parseToNode(text)
        # mecab = MeCab.Tagger('-Ochasen')
        # node = mecab.parseToNode(text)
        # tagger = MeCab.Tagger("-Ochasen")

        # node = mecab.parseToNode(text)
        only_full_uttrance = []
        tagger = MeCab.Tagger("-Owakati")
        tagger.parse('')
        for row in self.full_data:
            only_full_uttrance.append(row[3])
            # sample_txt = row[3]
            # result = tagger.parse(sample_txt)
            # print(result)
        # モデルの生成
        vectorizer = TfidfVectorizer(smooth_idf = False)
        # TF-IDFの計算
        values = vectorizer.fit_transform(only_full_uttrance).toarray()
        # 特徴量ラベルの取得
        words = vectorizer.get_feature_names_out()
        #結果のプリント
        print(values)
        print(words)
        
        df = pd.DataFrame(values, columns = words)
        print(df.T.sort_values(by=0,ascending=False)[0])
        print('---------------')
        print(df.T.sort_values(by=1,ascending=False)[1])
            
  
# readCsv("2022-10-26.csv")
# b = read_csv("full_log/2022-10-26_zemi.csv")
# b.mecab_owakati()
