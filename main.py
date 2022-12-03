import tkinter as tk
from tkinter import ttk
from turtle import width
from ttkwidgets import CheckboxTreeview #pip install ttkwidgetsでインストール
from PIL import Image, ImageTk
import tkinter.messagebox as mb
import os


import  csv_operate as csop

FILE_PATH =""

DIR_NAME = "../speech_to_text_2121040"
VIEWLOG_DIR_PATH = DIR_NAME+"/VIEWLOG_FILE/"#ログを保存する場所

# ディレクトリが存在しない場合、ディレクトリを作成する
if not os.path.exists(DIR_NAME):
    os.makedirs(DIR_NAME)
if not os.path.exists(VIEWLOG_DIR_PATH):
    os.makedirs(VIEWLOG_DIR_PATH)

class Display_log():
    def __init__(self):
        # ##############
        # wigwtの配置 
        # ##############
        self.root = tk.Tk() #tkinterでGUIを作成
        self.root.title('View Log') #GUIタイトル
        screenWidth = int(self.root.winfo_screenwidth())#Window横幅
        screenHeight = int(self.root.winfo_screenheight())#Window縦幅
        screenHeight = screenHeight*6/7
        self.root.geometry(str(screenWidth)+"x"+str(int(screenHeight)))
        
        width00 = int(screenWidth/6);width01 = int(screenWidth-width00)
        height00 = int(screenHeight/3);height01 = int(screenHeight-height00)
        heightline = 17#チェックボックスとテキストボックスの行数# print(width00,width01,height00,height01)
        # ##############
        # wigwtの配置 
        # packと仲良くなろう https://imagingsolution.net/program/python/tkinter/widget_layout_pack/
        # ##############
        frame_top = tk.Frame(self.root, borderwidth = 2, relief = tk.SUNKEN)
        # frame_tool_bar.pack(fill = tk.X)
        # チェックボックスツリー
        ct_area = CheckboxTreeview(height=heightline-3 , show='tree') #GUIの中にチェックボックスツリービューを表示する場所を作る
        # ct_area.grid(row=0,column=0) #チェックボックスツリービューを設置
        ct_area.pack(in_ =  frame_top ,side = tk.LEFT,ipadx = 30, ipady = 1)
        # テキストボックス：フルログ用
        listbox2 = tk.Listbox(height=heightline,width=width01-500)
        # listbox2.grid(row=0,column=1)
        listbox2.pack(in_ =  frame_top, side = tk.LEFT,ipadx = 30, ipady = 11)
        frame_top.pack(fill = tk.X)
    
        # ButtonFRRAME：ボタンをフレームに入れて横並びで配置
        frame_button = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT, pady=5, padx=5,width=width01)
        # frame = tk.Frame(self.root,width=200,height=200)
        self.select_button = ttk.Button(text="選択確認", command=self._img_show)
        self._button = ttk.Button(text="ファイル選択", command=self._select_full_log)

        self.select_button.pack(in_= frame_button,side = tk.RIGHT, expand=True)
        self._button.pack(in_= frame_button,side = tk.RIGHT, expand=True)

        # PC側のFrame
        frame_imgPC = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT)
        label = ttk.Label(text="PC")
        label.pack(in_= frame_imgPC ,side = tk.TOP)
        self.canvasPC=tk.Canvas()
        self.canvasPC.pack(in_= frame_imgPC ,side = tk.TOP)
    
        # USER側のFrame
        frame_imgUSER = tk.Frame(borderwidth = 2, relief = tk.FLAT)
        label = ttk.Label(text="USER")
        label.pack(in_= frame_imgUSER ,side = tk.TOP)        
        # canvasUSER=tk.Canvas(width=640,height=426,bd=0, highlightthickness=0, relief='ridge')
        self.canvasUSER=tk.Canvas()
        self.canvasUSER.pack(in_= frame_imgUSER ,side = tk.TOP)
        
        # 特定のIMGを取得してキャンバスに描画
        self._img_show()
        frame_button.pack(side = tk.LEFT)
        frame_imgPC.pack(side = tk.LEFT, expand=True)
        frame_imgUSER.pack(side = tk.LEFT, expand=True)
        # ##########################################
        # ファイル名取得後CSVファイルの読み込み
        # ##########################################
        self._select_full_log()
        self.root.mainloop()
    
    def _img_show(self):
        try:   
            # 画像を指定              
            imgsize = int(200)                                                    
            img = Image.open(VIEWLOG_DIR_PATH+'checed_PC.png')
            img = img.resize(( imgsize, imgsize ))
            img.save(VIEWLOG_DIR_PATH+'checked_resizePC.png')
            img = Image.open(VIEWLOG_DIR_PATH+'checed_USER.png')
            img = img.resize(( imgsize, imgsize ))
            img.save(VIEWLOG_DIR_PATH+'checed_resizeUSER.png')

            imgUSER = tk.PhotoImage(file=VIEWLOG_DIR_PATH+'checed_resizeUSER.png')
            imgPC = tk.PhotoImage(file=VIEWLOG_DIR_PATH+'checked_resizePC.png')

            self.canvasPC.delete('p1')
            self.canvasUSER.delete('p1')

            # キャンバスに画像を表示する       
            self.canvasUSER.create_image(105,10,image=imgUSER,tag='p1', anchor = tk.NW)
            self.canvasPC.create_image(105,10,image=imgPC,tag='p1', anchor = tk.NW)

        except BaseException as e:
            print(e)
        

    # Pythonでファイル名と拡張子に分割 https://kino-code.com/python_os_path_splitex/
    def get_filename_and_exe(PATH):
        file, ext = os.path.splitext(PATH)
        value =  (file,ext)
        return value

    # FULLCSVDATAをGUI上で選択肢て読み込む処理
    def _select_full_log(self):
        FILE_PATH = tk.filedialog.askopenfilename(filetypes=[("csvファイル", "*.csv")])#CSVファイル形式のみをブラウザから選択する
        return_YN = mb.askyesno("以下のファイルを開きますか?", FILE_PATH)
        #上記のクリックの結果を元に処理を変化させる。
        if return_YN == False: #「No」をクリックされた時の処理
            print("No!!!")
        elif return_YN == True: #「Yes」をクリックされた時の処理
            res = ""
            try:
                print("true")
            except:
                print ("Error."+res)
        # CSVデータ格納用クラス変数に代入する．ボタン選択でも実行可能なようにする
        self.csv_data=csop.read_csv(FILE_PATH)
        self._img_show()
        return FILE_PATH
    
    def view_log(self):
        USER_OR_PC = "話者"
        DAY = "時刻"
        WINDOW_OB = "開いていたwindow"
        HINSHI = "品詞"
        abstract_list = [USER_OR_PC, DAY, WINDOW_OB,HINSHI] #抽象的なリスト
        book_list =self.csv_data.get_day()
        sport_list = self.csv_data.get_wa()
        car_list = self.csv_data.get_windowOB()
        hinshi_list = ["その他", "感動詞", "記号", "形容詞", "名詞", "助詞", "助動詞", "接続詞", "接頭詞", "動詞", "副詞", "連体詞"] #抽象的なリストの「漫画」の具体例

        ct_area = CheckboxTreeview(self.root, height=14, show='tree') #GUIの中にチェックボックスツリービューを表示する場所を作る
        ct_area.grid(row=0,column=0) #チェックボックスツリービューを設置

        for abstract in abstract_list:
            ct_area.insert("", "0", abstract, text=abstract)
            if abstract == DAY:
                for book in book_list:
                    ct_area.insert(abstract, "end", book, text = book+"時")

            if abstract ==USER_OR_PC:
                for sport in sport_list:
                    ct_area.insert(abstract, "end", sport, text = sport)

            if abstract == WINDOW_OB:
                for i, car in enumerate(car_list):
                        try:
                            ct_area.insert(abstract, "end", car, text = car)
                        except BaseException as e:
                            print(e)            
                            ct_area.insert(abstract, "end", "読み込み不可"+str(i), text = "window名読み込み不可")
            if abstract == HINSHI:
                for i in hinshi_list:
                    ct_area.insert(abstract, "end", i, text = i)
        listbox2 = tk.Listbox(self.root,height=15,width=320)
        data = self.csv_data.get_result_data()

        for col in data:
            listbox2.insert(tk.END, col)  
        # listbox2.pack(side=tk.LEFT)
        listbox2.grid(row=0,column=1)

        def check():
        #    print(ct_area.get_checked())
            path = (os.path.basename(FILE_PATH))
            filename, fileext = os.path.splitext(os.path.basename(path))
            dd = self.csv_data.compar_list(ct_area.get_checked(), DIR_NAME+filename)
            listbox2.delete(0, tk.END)
            for col in dd:
                listbox2.insert(tk.END, col)
            self.csv_data.re_init(FILE_PATH)

        # canvasサイズも画面サイズと同じにして描画   
        frame = tk.Frame(self.root,width=300)

        frameUSER = tk.Frame(frame)
        label = ttk.Label(frameUSER, text="USER")
        self.canvasUSER=tk.Canvas(frameUSER)

        framePC = tk.Frame(frame)
        labelp = ttk.Label(framePC, text="PC")
        self.canvasPC=tk.Canvas(framePC)
        # canvasUSER=tk.Canvas(frameUSER ,width=640,height=426,bd=0, highlightthickness=0, relief='ridge')

        frameUSER.pack(side=tk.LEFT)
        framePC.pack(side=tk.LEFT)

        label.pack()
        self.canvasUSER.pack()

        labelp.pack()
        self.canvasPC.pack()

        frame.grid(row=1,column=1,sticky=tk.NW,pady=30)

        # print(reload_fulllog)

if __name__ == "__main__":
    b=Display_log()