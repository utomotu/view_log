import tkinter as tk
from tkinter import ttk
from turtle import width
from ttkwidgets import CheckboxTreeview #pip install ttkwidgetsでインストール
from PIL import Image, ImageTk
import tkinter.messagebox as mb
import os


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
        self.FILE_PATH =""
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
        # packと仲良くなろう https://imagingsolution.net/program/python/tkinter/widget_layout_pack/
        # ##############
        frame_top = tk.Frame(self.root, borderwidth = 2, relief = tk.SUNKEN)
        # チェックボックスツリー
        self.ct_area = CheckboxTreeview(height=heightline-3 , show='tree') #GUIの中にチェックボックスツリービューを表示する場所を作る
        #チェックボックスツリービューを設置
        self.ct_area.pack(in_ =  frame_top ,side = tk.LEFT,ipadx = 30, ipady = 1)
        # テキストボックス：フルログ用
        self.listbox2 = tk.Listbox(height=heightline,width=width01-500)
        self.listbox2.pack(in_ =  frame_top, side = tk.LEFT,ipadx = 30, ipady = 11)
        frame_top.pack(fill = tk.X)
        
        ##################
        # ButtonFRRAME：ボタンをフレームに入れて横並びで配置
        ##################
        frame_button = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT, pady=5, padx=5,width=width01)
        select_checkbox_button = ttk.Button(text="選択確認", command=lambda:[self._treebox_check(),self._img_show()])
        select_file_button = ttk.Button(text="ファイル選択", command=lambda:[self._select_full_log()])

        select_checkbox_button.pack(in_= frame_button,side = tk.RIGHT, expand=True)
        select_file_button.pack(in_= frame_button,side = tk.RIGHT, expand=True)
        ##################
        # PC側のFrame
        ##################
        frame_imgPC = tk.Frame(self.root, borderwidth = 2, relief = tk.FLAT)
        label = ttk.Label(text="PC")
        label.pack(in_= frame_imgPC ,side = tk.TOP)
        self.canvasPC=tk.Canvas()
        self.canvasPC.pack(in_= frame_imgPC ,side = tk.TOP)
        ##################
        # USER側のFrame
        ##################
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
        self.view_log()

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
        self.FILE_PATH = tk.filedialog.askopenfilename(filetypes=[("csvファイル", "*.csv")])#CSVファイル形式のみをブラウザから選択する
        return_YN = mb.askyesno("以下のファイルを開きますか?", self.FILE_PATH)
        #上記のクリックの結果を元に処理を変化させる。
        if return_YN == False: #「No」をクリックされた時の処理
            print("No!!!")
        elif return_YN == True: #「Yes」をクリックされた時の処理
            res = ""
            try:
                print("true")         
                # CSVデータ格納用クラス変数に代入する．ボタン選択でも実行可能なようにする
                self.csv_data=csop.read_csv(self.FILE_PATH)
                ##################
                # 過去ログの表示
                ##################
                dd = self.csv_data.get_result_data()
                self.listbox2.delete(0, tk.END)# ボックスの中をリセット
                for col in dd:
                    self.listbox2.insert(tk.END, col)
                    # self.listbox2.config()
                # なんの処理してるんだ棟．．．．
                # self.csv_data.re_init(self.FILE_PATH)    
                ##################
                # チェックボックスの更新
                ##################
                book_list =self.csv_data.get_day()
                    # insert(親、インデックス、iid=なし、**kw )[ソース]
                    # 新しいアイテムを作成し、新しく作成されたアイテムのアイテム識別子を返します。
                    # パラメーター：	
                    # parent ( str ) – 親アイテムの識別子
                    # index ( intまたは"end" ) – 親の子のリストのどこに新しい項目を挿入するか
                    # iid ( Noneまたはstr ) – アイテム識別子。iid はツリーにまだ存在してはなりません。iid が None の場合、新しい一意の識別子が生成されます。
                    # kwttk.Treeview.insert() –メソッドに渡されるその他のオプション
                try:
                    self.ct_area.delete(DAY)
                    self.ct_area.insert("", "0", DAY, text=DAY)
                
                    for book in book_list:
                        self.ct_area.insert(DAY, "end", book, text = book+"時")
                    self.ct_area.change_state(DAY, "checked")
                except BaseException as e:
                    print (e) 
            except:
                print ("Error."+res)
        # return self.FILE_PATH
    
    def _treebox_check(self):
        path = (os.path.basename(self.FILE_PATH))
        filename, fileext = os.path.splitext(os.path.basename(path))
        dd = self.csv_data.compar_list(self.ct_area.get_checked(), DIR_NAME+filename)
        self.listbox2.delete(0, tk.END)
        for col in dd:
            self.listbox2.insert(tk.END, col)
            # self.listbox2.config()
        self.csv_data.re_init(self.FILE_PATH)
            
    def view_log(self):
        abstract_list = [DAY, HINSHI] #抽象的なリスト
        book_list =self.csv_data.get_day()
        hinshi_list = ["その他", "感動詞", "記号", "形容詞", "名詞", "助詞", "助動詞", "接続詞", "接頭詞", "動詞", "副詞", "連体詞"] #抽象的なリストの「漫画」の具体例
        # hinshi_list = ["その他", "感動詞", "記号", "形容詞", "名詞", "助詞", "助動詞", "接続詞", "接頭詞", "動詞", "副詞", "連体詞"] #抽象的なリストの「漫画」の具体例
        try:
            self.ct_area.delete(DAY)
        except:
            print("error")
        # チェックボックスに情報を付与
        for abstract in abstract_list:
            self.ct_area.insert("", "0", abstract, text=abstract)
            if abstract == DAY:
                for book in book_list:
                    self.ct_area.insert(abstract, "end", book, text = book+"時")
                    
            if abstract == HINSHI:
                for i in hinshi_list:
                    self.ct_area.insert(abstract, "end", i, text = i)
                    if(i == "名詞"):
                        print("adasdasda")
                        self.ct_area.change_state(i, "checked")
        self.ct_area.change_state(DAY, "checked")
if __name__ == "__main__":
    b=Display_log()