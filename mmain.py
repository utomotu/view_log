import tkinter as tk
from tkinter import ttk

root = tk.Tk() #tkinterでGUIを作成
root.title('View Log') #GUIタイトル
screenWidth = int(root.winfo_screenwidth())
screenHeight = int(root.winfo_screenheight())
root.geometry(str(screenWidth)+"x"+str(int(screenHeight*2/3)))

root.mainloop()# root.geometry("1200x700") #GUIの大きさ