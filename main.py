import tkinter as tk
from tkinter import ttk
from ttkwidgets import CheckboxTreeview #pip install ttkwidgetsでインストール
from PIL import Image
import tkinter.messagebox as mb
import os
import tkinter.font as tkFont

import  csv_operate as csop

DIR_NAME = "../speech_to_text_2121040"
VIEWLOG_DIR_PATH = DIR_NAME+"/VIEWLOG_FILE/"#ログを保存する場所
DAY = "時刻"
HINSHI = "品詞"

# ディレクトリが存在しない場合、ディレクトリを作成する
if not os.path.exists(DIR_NAME):
    os.makedirs(DIR_NAME)
if not os.path.exists(VIEWLOG_DIR_PATH):
    os.makedirs(VIEWLOG_DIR_PATH)

class Display_log():
    def __init__(self):
        self.csv_data:csop
        self.FILE_PATH =""
        self.root = tk.Tk() #tkinterでGUIを作成
        self.root.title('View Log') #GUIタイトル
        screenWidth = int(self.root.winfo_screenwidth())#Window横幅
        screenHeight = int(self.root.winfo_screenheight())#Window縦幅
        screenHeight = screenHeight*6/7
        self.root.geometry(str(screenWidth)+"x"+str(int(screenHeight)+10))
        self.read_data = ""
        
        width00 = int(screenWidth/6);width01 = int(screenWidth-width00)
        height00 = int(screenHeight/3);height01 = int(screenHeight-height00)
        heightline = 9#チェックボックスとテキストボックスの行数# print(width00,width01,height00,height01)
        
        fontsize= 16
        viewfont = tkFont.Font(size = fontsize, weight = "bold")

        self.dataname = ttk.Label(text="状況",font=viewfont)
        self.dataname.pack(in_= self.root ,side = tk.TOP, expand=True,anchor=tk.S) 

        # ##############
        # packと仲良くなろう https://imagingsolution.net/program/python/tkinter/widget_layout_pack/
        # ##############

        ##################
        # result表示
        ##################
        frame_top = tk.Frame(self.root, borderwidth = 2, relief = tk.SUNKEN)
        # チェックボックスツリー
        self.ct_area = CheckboxTreeview(height=heightline , show='tree') #GUIの中にチェックボックスツリービューを表示する場所を作る
        #チェックボックスツリービューを設置
        self.ct_area.pack(in_ =  frame_top ,side = tk.LEFT,ipadx = 30, ipady = 1)
        
        # テキストボックス：フルログ用
        column = ('日', '時間',"話者", '認識結果')
        self.tree = ttk.Treeview(height=heightline-2, columns=column)
        self.tree["show"] = "headings"
        self.tree.column(0, width=40)
        self.tree.column(1, width=80)
        self.tree.column(2, width=50)
        self.tree.column(3, width=width01)
        # 列の見出し設定
        self.tree.heading(0,text='日')
        self.tree.heading(1, text='時間',anchor='center')
        self.tree.heading(2, text='', anchor='w')
        self.tree.heading(3, text='認識結果', anchor='w')
        #  self.tree.heading('Score',text='Score', anchor='center')
        
        self.tree.pack(in_ =  frame_top, side = tk.LEFT,ipadx = 30, ipady = 11)
        frame_top.pack(fill = tk.X)
        
        ##################
        # スケールバー～ラベル位置（オプションをいくつか設定）
        # https://imagingsolution.net/program/python/tkinter/scale_trackbar/
        ##################
        
        self.time_scale = tk.Scale(
                        self.root,  
                        command = self._time_scale_command,
                        orient=tk.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                        length = screenWidth,   # 全体の長さ
                        width = 15,             # 全体の太さ
                        sliderlength = 20,      # スライダー（つまみ）の幅
                        from_ = 0, to = 24, # 最小値（開始の値 # 最大値（終了の値）
                        resolution=0.5,         # 変化の分解能(初期値:1)
                        tickinterval=0,         # 目盛りの分解能(初期値0で表示なし)
                        showvalue=False,         # スライダー上の値を非表示にする
                        label = "時刻：0時から0分"
                        )
        self.time_scale.pack()

        self.mometn_scale = tk.Scale(
                        self.root,  
                        command = self._time_scale_command,
                        orient=tk.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                        length = screenWidth,           # 全体の長さ
                        width = 15,             # 全体の太さ
                        sliderlength = 20,      # スライダー（つまみ）の幅
                        from_ = 0, to = 24, # 最小値（開始の値 # 最大値（終了の値）
                        resolution=0.5,           # 変化の分解能(初期値:1)
                        tickinterval=0,        # 目盛りの分解能(初期値0で表示なし)
                        showvalue=False      # スライダー上の値を非表示にする
                        # label = "取得時刻30分おき（時間）"
                        )
        self.mometn_scale.pack()
        
        ##################
        # ButtonFRRAME：ボタンをフレームに入れて横並びで配置
        ##################
        frame_button = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT)
        ffbwidth = 9
        self.swith_value: bool = False
        self.swith_v_value: bool = False
        ffb = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT, pady=5, padx=5,width=ffbwidth)
        # select_checkbox_button = ttk.Button(text="選択確認", command=lambda:[self._treebox_check(),self._img_show()])
        select_checkbox_button = ttk.Button(text="フルデータ確認", command=lambda:[self.full_data_list("dsa")])
        
        select_file_button = ttk.Button(text="ファイル選択", command=lambda:[self._select_full_log()])
        select_switch = ttk.Button(text="抜き取りOFF", command=lambda:[click()])
        select_switch_v = ttk.Button(text="昇順", command=lambda:[click_v()])

        def click():
            if self.swith_value:
                select_switch.config(text='抜き取りOFF')
                self.swith_value = not self.swith_value
                
            else:
                select_switch.config(text='抜き取りON')
                self.swith_value = not self.swith_value
        
        def click_v():
            if self.swith_v_value:
                select_switch_v.config(text='昇順')
                self.swith_v_value = not self.swith_v_value
                
            else:
                select_switch_v.config(text='降順')
                self.swith_v_value = not self.swith_v_value
        
        select_checkbox_button.pack(in_= ffb,side = tk.LEFT, expand=True)
        # select_file_button.pack(in_= ffb,side = tk.LEFT, expand=True)
        select_switch.pack(in_= ffb,side = tk.LEFT, expand=True)
        # select_switch_v.pack(in_= ffb,side = tk.LEFT, expand=True)
    
        ffbb = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT, pady=5, padx=5,width=ffbwidth)
        
        self.entry1 = ttk.Entry(width=8)
        word_button = ttk.Button(text="単語検索", command=lambda:[self._resarch_word()])
        self.entry1.pack(in_=ffbb, side=tk.LEFT, anchor="w", padx=4, pady=4, expand=True)
        word_button.pack(in_= ffbb,side = tk.LEFT, expand=True)
        self.freqence_word = ttk.Label(text="")
        self.freqence_word.pack(in_= ffbb,side = tk.LEFT, expand=True)
        
        self.wordlistbox = tk.Listbox(height=heightline,width=25)
        
        ffb.pack(in_= frame_button,side = tk.TOP)#ボタン横並び
        ffbb.pack(in_= frame_button,side = tk.TOP)#ボタン横並び
        self.wordlistbox.pack(in_= frame_button, side = tk.TOP,ipadx = 30, ipady = 11)        
        
        frame_button.pack(in_= self.root,side = tk.LEFT, expand=True)
        frame_imgUSER = tk.Frame(relief = tk.FLAT)
        frame_imgPC = tk.Frame(relief = tk.FLAT)
        frame_imgcommn = tk.Frame(relief =tk.RIDGE)

        frame_imgUSER.pack(in_= self.root, side = tk.LEFT, expand=True)
        frame_imgcommn.pack(in_= self.root,side = tk.LEFT, expand=True)
        frame_imgPC.pack(in_= self.root,side = tk.LEFT, expand=True)
        
        ##################
        # USER側のFrame
        ##################
        self.lUSER = ttk.Label(text="ユーザ発話",font=viewfont)
        self.lUSER.pack(in_= frame_imgUSER ,side = tk.TOP) 
        # canvasUSER=tk.Canvas(width=640,height=426,bd=0, highlightthickness=0, relief='ridge')
        self.canvasUSER=tk.Canvas(relief= tk.RAISED)
        self.canvasUSER.pack(in_= frame_imgUSER ,side = tk.TOP)
        self.labelUSER = ttk.Label(text=":",font=viewfont)
        self.labelUSER.pack(in_= frame_imgUSER ,side = tk.TOP)        
        ##################
        # PC側のFrame
        ##################
        
        lPC = ttk.Label(text="PC音声", font=viewfont)
        lPC.pack(in_= frame_imgPC ,side = tk.TOP)
        self.canvasPC=tk.Canvas(relief= tk.RAISED)
        self.canvasPC.pack(in_= frame_imgPC ,side = tk.TOP)
        self.labelPC = ttk.Label(text=":", font=viewfont)
        self.labelPC.pack(in_= frame_imgPC ,side = tk.TOP)


        ##################
        # andVlueのFrame
        ##################
        
        label = ttk.Label(text="共通単語",font=viewfont)
        label.pack(in_= frame_imgcommn ,side = tk.TOP)
        self.canvascommn=tk.Canvas(relief= tk.RAISED)
        self.canvascommn.pack(in_= frame_imgcommn ,side = tk.TOP)
        label = ttk.Label(text="  ",font=viewfont)
        label.pack(in_= frame_imgcommn,side = tk.TOP)        

        # 特定のIMGを取得してキャンバスに描画
        self._img_show()

        # ##########################################
        # ファイル名取得後CSVファイルの読み込み
        # ##########################################
        self._select_full_log()
        self.view_log()

        # ##########################################
        # CSVファイルの読み込後の処理
        # ##########################################
        self.time_scale.config(from_ = self.csv_data.startday.strftime("%H"),  to =  self.csv_data.endday.strftime("%H"))
        # self.csv_data.scale_list(startscaletime, scalemomenttime, self.ct_area.get_checked(), DIR_NAME+filename)
        self._img_show()

        self.root.mainloop()
    def full_data_list(self, dummy_parameter):
        path = (os.path.basename(self.FILE_PATH))
        filename, fileext = os.path.splitext(os.path.basename(path))
        self.csv_data.full_data_list(self.ct_area.get_checked(), DIR_NAME+filename)
        self._img_show()


    def _time_scale_command(self, dummy_parameter):      
        # 引数について　https://stackoverflow.com/questions/23842770/python-function-takes-1-positional-argument-but-2-were-given-how
        # startscaletime  = math.modf(float(self.time_scale.get()))# スケールバーの値取得
        startscaletime = float(self.time_scale.get())
        floatstartscale = startscaletime-int(startscaletime)
        tt = format(int(startscaletime), '02')+":"+format(int(floatstartscale*60), '02')#format(数字,0埋め方)
        scalemomenttime = (self.mometn_scale.get())# スケールバーの値取得
        tt2 = str(scalemomenttime)+"時間"
        self.time_scale.config(label="時刻 : "+str(tt)+"から"+str(tt2))
        
        path = (os.path.basename(self.FILE_PATH))
        filename, fileext = os.path.splitext(os.path.basename(path))
        self.csv_data.scale_list(startscaletime, scalemomenttime, self.ct_area.get_checked(), DIR_NAME+filename)
        self._img_show()
        
    def _img_show(self):
        try:   
            # 画像を指定              
            imgsize = int(250)                                                    
            img = Image.open(VIEWLOG_DIR_PATH+'checed_PC.png')
            img = img.resize(( imgsize, imgsize ))
            img.save(VIEWLOG_DIR_PATH+'checked_resizePC.png')
            
            img = Image.open(VIEWLOG_DIR_PATH+'checed_USER.png')
            img = img.resize(( imgsize, imgsize ))
            img.save(VIEWLOG_DIR_PATH+'checed_resizeUSER.png')

            img = Image.open(VIEWLOG_DIR_PATH+'checed_AndValue.png')
            img = img.resize(( imgsize, imgsize ))
            img.save(VIEWLOG_DIR_PATH+'checed_resizeAndValue.png')

            imgUSER     = tk.PhotoImage(file=VIEWLOG_DIR_PATH+'checed_resizeUSER.png')
            imgPC       = tk.PhotoImage(file=VIEWLOG_DIR_PATH+'checked_resizePC.png')
            imgcommn = tk.PhotoImage(file=VIEWLOG_DIR_PATH+'checed_resizeAndValue.png')

            self.canvasPC.delete('p1')
            self.canvasUSER.delete('p1')
            self.canvascommn.delete('p1')

            # キャンバスに画像を表示する       
            self.canvasUSER.create_image(10,10,image=imgUSER,tag='p1', anchor = tk.NW)
            self.canvasPC.create_image(10,10,image=imgPC,tag='p1', anchor = tk.NW)
            self.canvascommn.create_image(10,10,image=imgcommn,tag='p1', anchor = tk.NW)

        except BaseException as e:
            print(e)
        
    # Pythonでファイル名と拡張子に分割 https://kino-code.com/python_os_path_splitex/
    def get_filename_and_exe(PATH):
        file, ext = os.path.splitext(PATH)
        value =  (file,ext)
        return value

    # FULLCSVDATAをGUI上で選択肢て読み込む処理
    def _select_full_log(self):
        self.FILE_PATH = tk.filedialog.askopenfilename(filetypes=[("csvファイル", "*.csv")])#CSVファイル形式のみをブラウザから選択する
        return_YN = mb.askyesno("以下のファイルを開きますか?", self.FILE_PATH)
        #上記のクリックの結果を元に処理を変化させる。
        if return_YN == False: #「No」をクリックされた時の処理
            print("No!!!")
        elif return_YN == True: #「Yes」をクリックされた時の処理
            try:
                # CSVデータ格納用クラス変数に代入する．ボタン選択でも実行可能なようにする
                self.csv_data = csop.read_csv(self.FILE_PATH,self.swith_value, self.swith_v_value)
                self.read_data = self.csv_data.get_result_data()
                data_name = self.csv_data.data_name
                self.dataname.config(text=data_name)
                ##################
                # 読み込んだ過去ログの表示
                ##################
                # df:pd
                df = self.csv_data.pdfulldata
                for i in range(len(df)):
                    try:
                        self.tree.insert("", "end", values=(df.iloc[i]["日"], df.iloc[i]["時"], df.iloc[i]["デバイス"], df.iloc[i]["認識結果"]))
                    except:
                        self.tree.insert("", "end", values=(df.iloc[i]["日"], df.iloc[i]["時"], df.iloc[i]["デバイス"], df.iloc[i]["認識結果"]))
                
                
                # なんの処理してるんだ棟．．．．
                # self.csv_data.re_init(self.FILE_PATH)     
            except BaseException as e:
                print("Error read CSV file")
                print (e)
        # return self.FILE_PATH
    
    def _treebox_check(self):
        self.csv_data.set_swith_value(self.swith_value, self.swith_v_value)#スイッチバリューを反映させておく
        path = (os.path.basename(self.FILE_PATH))

        filename, fileext = os.path.splitext(os.path.basename(path))
        self.read_data = self.csv_data.compar_list(self.ct_area.get_checked(), DIR_NAME+filename)
        
        self.labelUSER.config(text=str(self.csv_data.USER_amout)+"字")
        self.labelPC.config(text=str(self.csv_data.PC_amout)+"字")
        
        self.csv_data.re_init(self.FILE_PATH)
        mmww = self.csv_data.get_mono_word_listy()
        # print(mmww)
        for wspc in mmww[1]:
            self.wordlistbox.insert(tk.END, wspc[0])
            print(wspc[0])
    def _resarch_word(self):
        # indices =self.wordlistbox.curselection()
        # index = indices[0]
        # try:
        #     resarch_word = self.wordlistbox.get(index)
        #     self.entry1.config(text = resarch_word)
        #     # print(resarch_word)
        # except:
        resarch_word = self.entry1.get()
        print(resarch_word)
        
        #列番号を元に更新する
        cc = 0 
        dd = self.read_data
        # for i,text in enumerate(dd):
        #     if resarch_word in text:
        #         self.listbox2.itemconfig(int(i), {'bg': 'ffffff'})
        
        # for i,text in enumerate(dd):
        #     if resarch_word in text:
        #         self.listbox2.itemconfig(int(i), {'bg': '#f0e68c'})
        #         cc+=1
        print(cc)
        self.freqence_word.config(text=str(cc)+"回")
                            
    def view_log(self):
        abstract_list = [HINSHI] #抽象的なリスト
        hinshi_list = ["感動詞", "形容詞", "名詞", "接続詞", "動詞", "副詞", "連体詞"] #抽象的なリストの「漫画」の具体例
        # チェックボックスに情報を付与
        for abstract in abstract_list:
            self.ct_area.insert("", "0", abstract, text=abstract)        
            if abstract == HINSHI:
                for i in hinshi_list:
                    self.ct_area.insert(abstract, "end", i, text = i)
                    if(i == "名詞"):
                        self.ct_area.change_state(i, "checked")

if __name__ == "__main__":
    b=Display_log()