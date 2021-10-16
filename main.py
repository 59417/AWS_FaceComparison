try:
    import Tkinter as tk
except:
    import tkinter as tk
    
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageTk
import os
import pandas as pd
import CompareFace
import dataframe_image as dfi
    
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1600x900")
        self.title('點名系統')
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        bt1 = tk.Button(self, text='學生名單', width = 20 , height = 3,
                        font=('DFKai-SB', 15), 
                        command=lambda: master.switch_frame(PageOne))
        bt1.pack(side='top', pady=20)
        bt2 = tk.Button(self, text='開始點名', width = 20 , height = 3,
                        font=('DFKai-SB', 15), 
                        command=lambda: master.switch_frame(PageTwo))
        bt2.pack(side='top', pady=20)
        bt3 = tk.Button(self, text='出席總表', width = 20 , height = 3,
                        font=('DFKai-SB', 15), 
                        command=lambda: master.switch_frame(PageThree))
        bt3.pack(side='top', pady=20)
        bt4 = tk.Button(self, text='離開', width = 20 , height = 3,
                        font=('DFKai-SB', 15),
                        command=lambda: master.destroy())
        bt4.pack(side='top', pady=20)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="學生名單", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        self.listbox = tk.Listbox(self, width=60, height=40)
        self.updateTable()
        self.listbox.pack(side="left", fill="y", padx=10)
        self.listbox.bind("<<ListboxSelect>>", self.selectStudent)
        
        frameid = tk.Frame(self)
        frameid.pack(side="top", fill="x", pady=5)
        label1=tk.Label(frameid, text="學號：")
        self.entry1 = tk.Entry(frameid)
        label1.grid(row=0, column=0)
        self.entry1.grid(row=0, column=1)
        
        frameName = tk.Frame(self)
        frameName.pack(side="top", fill="x", pady=5)
        label1=tk.Label(frameName, text="姓名：")
        self.entry2 = tk.Entry(frameName)
        label1.grid(row=0, column=0)
        self.entry2.grid(row=0, column=1)

        img = Image.open('defaultImage.jpg')                    
        # 讀取圖片
        img = img.resize((round(img.width * 300 / img.height), 300))   
        # 縮小圖片
        imgTk =  ImageTk.PhotoImage(img)                        
        # 轉換成Tkinter可以用的圖片
        self.lbl_2 = tk.Label(self, image=imgTk, height=300)                   
        # 宣告標籤並且設定圖片
        self.lbl_2.image = imgTk
        self.lbl_2.pack()                            

        frame2 = tk.Frame(self)
        frame2.pack(side="top", fill="x", pady=5)
        button1 = tk.Button(frame2, text="上傳照片",
                            command= lambda: self.uploadPhoto())
        button2 = tk.Button(frame2, text="儲存",
                            command= lambda: self.savePhoto())
        button3 = tk.Button(frame2, text="刪除",
                            command= lambda: self.removeStudent())
        button4 = tk.Button(frame2, text="返回",
                  command=lambda: master.switch_frame(StartPage))
        
        button1.pack(side="left", fill="y", padx=5)
        button2.pack(side="left", fill="y", padx=5)
        button3.pack(side="left", fill="y", padx=5)
        button4.pack(side="left", fill="y", padx=5)
    
    def uploadPhoto(self):
        self.selectFilePath = askopenfilename()
        img = Image.open(self.selectFilePath)                    
        # 讀取圖片
        img = img.resize((round(img.width * 300 / img.height), 300))   
        # 縮小圖片
        imgTk =  ImageTk.PhotoImage(img)                        
        # 宣告標籤並且設定圖片
        self.lbl_2.configure(image=imgTk)
        self.lbl_2.image = imgTk
        
    def savePhoto(self):
        selectFile = Image.open(self.selectFilePath)
        selectFile.save('./students/%s%s.jpg'%(
            self.entry1.get(), self.entry2.get()))
        self.updateTable()
        
    def selectStudent(self, event): 
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            studentIdName = event.widget.get(index)
            self.entry1.delete(0,'end')
            self.entry1.insert(0,studentIdName[:2])
            self.entry2.delete(0,'end')
            self.entry2.insert(0,studentIdName[2:])
        else:
            self.entry1.delete(0,'end')
            self.entry2.delete(0,'end')
            
        img = Image.open('./students/%s.jpg'%(studentIdName))                    
        # 讀取圖片
        img = img.resize((round(img.width * 300 / img.height), 300))   
        # 縮小圖片
        imgTk =  ImageTk.PhotoImage(img)                        
        # 宣告標籤並且設定圖片
        self.lbl_2.configure(image=imgTk)
        self.lbl_2.image = imgTk
        self.selectFilePath = './students/%s.jpg'%(studentIdName)
        
    def removeStudent(self):
        os.remove(self.selectFilePath)
        self.updateTable()
    
    def updateTable(self):
        path = './students' 
        namejpg = sorted(list(os.listdir(path)))  
        if ('.jpg' not in namejpg[0]): 
            del namejpg[0]  #第一項若為['.DS_Store']需刪除
        self.listbox.delete(0,'end')
        for i, name in enumerate(namejpg):
            self.listbox.insert(i+1, name[:-4])
            

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="開始點名", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        frame_noshow = tk.Frame(self)
        frame_noshow.pack(side="right", fill="y", pady=5)
        lbl_1 = tk.Label(frame_noshow, text='未到學生', bg='yellow', fg='red', 
                         font=('Arial', 18))
        lbl_1.pack(side="top", fill="x", padx=5)
                
        self.listbox = tk.Listbox(frame_noshow, width=30, height=30)
        self.listbox.pack(side="top", fill="x", pady=10)

        img = Image.open('defaultTeam.jpg')                    
        # 讀取圖片
        img = img.resize((round(img.width * 600 / img.height), 600))   
        # 縮小圖片
        imgTk =  ImageTk.PhotoImage(img)                        
        # 轉換成Tkinter可以用的圖片
        self.lbl_2 = tk.Label(self, image=imgTk, height=600)                   
        # 宣告標籤並且設定圖片
        self.lbl_2.image = imgTk
        self.lbl_2.pack()     
        
        framePhoto = tk.Frame(self)
        framePhoto.pack(side="left", fill="x", pady=5)
        button1 = tk.Button(framePhoto, text="上傳點名照片",
                            command= lambda: self.uploadPhoto())
        button2 = tk.Button(framePhoto, text="開始辨識", 
                            command= lambda: self.startReg())
        button3 = tk.Button(framePhoto, text="返回",
                  command=lambda: master.switch_frame(StartPage))
        button1.pack(side="left", fill="y", padx=5)
        button2.pack(side="left", fill="y", padx=5)
        button3.pack(side="right", fill="y", padx=5)
        
    def uploadPhoto(self):
        self.selectFilePath = askopenfilename()
        img = Image.open(self.selectFilePath)                    
        # 讀取圖片
        img = img.resize((round(img.width * 600 / img.height), 600))   
        # 縮小圖片
        imgTk =  ImageTk.PhotoImage(img)                        
        # 宣告標籤並且設定圖片
        self.lbl_2.configure(image=imgTk)
        self.lbl_2.image = imgTk
        
            
    def finalUpdatePhoto(self, finalName):
        img = Image.open(finalName)                    
        # 讀取圖片
        img = img.resize((round(img.width * 600 / img.height), 600))   
        # 縮小圖片
        imgTk =  ImageTk.PhotoImage(img)                        
        # 宣告標籤並且設定圖片
        self.lbl_2.configure(image=imgTk)
        self.lbl_2.image = imgTk
        
    def startReg(self):
        self.result_df = CompareFace.main(self.selectFilePath)
        self.finalUpdatePhoto(self.result_df.columns[0] + '.jpg')
        noshow_df = self.result_df.loc[self.result_df[self.result_df.columns[0]]==0]
        readdf = pd.read_csv('student_info.csv')
        outputdf = pd.concat([readdf,self.result_df],axis = 1)
        
        
        noshow_df = outputdf.iloc[noshow_df.index]
        noshow_df['idName'] = noshow_df['ID'].apply(str) + noshow_df['name']
        
        
        self.updateTable(noshow_df['idName'])
        dfi.export(outputdf, 'dataframe.png')
        outputdf.to_csv('student_info.csv', sep=',', index=False)


    def updateTable(self, noshowList):
        self.listbox.delete(0,'end')
        for i, name in enumerate(noshowList):
            self.listbox.insert(i+1, name)
        
class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="出席總表", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        if os.path.exists('./dataframe.png'):
            img = Image.open('./dataframe.png')                    
            # 讀取圖片
            img = img.resize((round(img.width * 800 / img.height), 800))   
        # 縮小圖片
            imgTk =  ImageTk.PhotoImage(img)                        
            # 轉換成Tkinter可以用的圖片
            self.lbl_2 = tk.Label(self, image=imgTk, height=800)                   
            # 宣告標籤並且設定圖片
            self.lbl_2.image = imgTk
            self.lbl_2.pack()     
        
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()