from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from pytube import YouTube
from threading import *
from io import BytesIO
import urllib.request
import os
from tkinter import messagebox
from win10toast import ToastNotifier


class y:
    def __init__(self,root) -> None:
        self.root = root
        root.title("mp3/mp4 downloader")
        root.geometry("500x200")
        root.resizable(False,False)
        root.iconbitmap(r"C:\Users\earle\Pythonenv\env\projects\elaina.ico")
        self.videopath = r"C:\Users\earle\Pythonenv\env\projects\Video"
        self.songpath = r"C:\Users\earle\Pythonenv\env\projects\Song"

        lefts = Frame(root)
        leftsbottom = Frame(lefts)
        rights = Frame(root)
        bottoms = Frame(root)
        bottomsright = Frame(bottoms)

        bottoms.pack(side = BOTTOM , fill=X, )
        bottomsright.pack(side= RIGHT)
        rights.pack(side = RIGHT, fill = BOTH)
        lefts.pack(fill= BOTH, expand = True)
        leftsbottom.pack(fill= X, side= BOTTOM, expand= True)
    
        self.label1 = Label(lefts,text ="Channel: ", anchor = "w", justify = LEFT)
        self.label2 = Label(lefts,text ="Title: ", anchor = "w", justify = LEFT)
        self.label3 = Label(lefts,text ="Publish Date: ", anchor = "w", justify = LEFT)
        self.label4 = Label(lefts,text ="Length: ", anchor = "w", justify = LEFT)
        self.label5 = Label(lefts,text ="Keywords: ", anchor = "w", justify = LEFT)
        self.progressbar = ttk.Progressbar(leftsbottom, orient=HORIZONTAL, mode = "indeterminate", length = 100)

        self.image_path= r"C:\Users\earle\Pythonenv\env\projects\placeholderjpg.jpg"
        self.original = Image.open(self.image_path)
        resized = self.original.resize((150,150), Image.Resampling.LANCZOS)
        self.image_ref = ImageTk.PhotoImage(resized)
        self.image = Label(rights, image = self.image_ref)

        self.e1 = Entry(bottoms, font =("Futura", 16))
        self.b1 = Button(bottomsright, text = "📁", height = 2, width = 11,  command = self.folder)
        self.b2 = Button(bottomsright, text = "mp3", height = 2, width = 11, command = self.mp3thread)
        self.b3 = Button(bottomsright, text = "mp4", height = 2, width = 11, command = self.mp4thread)

        self.image.pack(fill=BOTH, expand=True, padx = 3, pady=5)

        self.label1.pack(fill=BOTH, expand= True)
        self.label2.pack(fill=BOTH, expand= True)
        self.label3.pack(fill=BOTH, expand= True)
        self.label4.pack(fill=BOTH, expand= True)
        self.label5.pack(fill=BOTH, expand= True)

        self.progressbar.pack(fill=X, expand= True, padx = 2)

        
        self.e1.pack(fill=BOTH, expand=True, padx = 3, pady=3)
        self.b1.pack(side = RIGHT, anchor= "se", pady=3, padx= 3)
        self.b3.pack(side = RIGHT, anchor= "se", pady=3)
        self.b2.pack(side = RIGHT, anchor= "se" , padx= 3, pady = 3)   

        self.e1.focus_set()      
    
    def mp3(self):
        try:
            link = self.e1.get()
            self.progressbar.start()

            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            title = yt.title
            thumbnail_url = yt.thumbnail_url
            publishd = yt.publish_date
            keywords = yt.keywords[:3]
            author = yt.author
            length = yt.length
            self.changeimg(thumbnail_url, title, publishd, keywords, author, length)

            vid = yt.streams.filter(only_audio=True).first()
            output = vid.download(self.songpath)
            base, ext = os.path.splitext(output)
            mp3_file = base + ".mp3"
            os.rename(output, mp3_file)

            self.message(title,author)
            self.progressbar.stop()

        except Exception as e:
            self.progressbar.stop()
            messagebox.showerror("Exception occured", e)

    def mp4(self):
        try:
            link = self.e1.get()
            self.progressbar.start()

            yt = YouTube(link)
            title = yt.title
            thumbnail_url = yt.thumbnail_url
            publishd = yt.publish_date
            keywords = yt.keywords[:3]
            author = yt.author
            length = yt.length
            self.changeimg(thumbnail_url, title, publishd, keywords, author, length)

            video = yt.streams.get_highest_resolution()
            video.download(self.videopath)

            self.message(title,author)
            self.progressbar.stop()

        except Exception as e:
            self.progressbar.stop()
            messagebox.showerror("Exception occured", e)
            

    def folder(self):
        os.startfile(r"C:\Users\earle\Pythonenv\env\projects")

    def mp3thread(self):
        t2 = Thread(target = self.mp3)
        t2.start()

    def mp4thread(self):
        t1 = Thread(target= self.mp4)
        t1.start()


    def changeimg(self, link, title, publishd, keywords, author, length):
        self.e1.delete(0, "end")
        
        self.label1.config(text = "Channel: " + author)
        self.label2.config(text = "Title: " + title)
        self.label3.config(text = "Publish date: " + str(publishd))
        self.label4.config(text = "Length : " + str(length) + " seconds")
        self.label5.config(text = "Keywords: " + ", ".join(keywords))
    
        u = urllib.request.urlopen(link)
        raw_data = u.read()
        u.close()

        self.orig = Image.open(BytesIO(raw_data))
        resized = self.orig.resize((150,150), Image.Resampling.LANCZOS)
        self.im_ref = ImageTk.PhotoImage(resized)

        self.image.configure(image=self.im_ref)
    
    def message(self, title, author):
        toast = ToastNotifier()
        toast.show_toast(
            author,
            title,
            duration = 10,
            icon_path = r"C:\Users\earle\Pythonenv\env\projects\elaina.ico",
            threaded=True
        )

root = Tk()
gui = y(root)
root.mainloop()



