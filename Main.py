from tkinter import*
from PIL import ImageTk, Image
import JsonManage

class Window:

    def __init__(self, master, W, H):

        self.master = master
        self.W = W
        self.H = H
        
        self.canv = Canvas(master, width = W, height = H, bg = '#232426',
                           highlightthickness = 0, borderwidth = 0)
        self.canv.pack(side = LEFT)

        self.Path = ''
        self.BG = '#146098'
        self.File = 'Files/config.json'

        self.CreateBg()

    def CreateBg(self):

        self.pic = ImageTk.PhotoImage(Image.open(self.Path+'Images/bg.png') \
                                      .resize((self.W, self.H),
                                              Image.ANTIALIAS))
        
        pic_window = self.canv.create_image(0, 0, image = self.pic,
                                            anchor = NW)

        self.canv.tag_lower(pic_window)

        self.CheckUpdatesBut()

    def CheckUpdatesBut(self):

        im = Image.open(self.Path + 'Images/CheckForUpdates.png')
        im = im.resize((round(0.8823*self.W), round(0.22*self.H)),
                       Image.ANTIALIAS)
        self.CheckImg = ImageTk.PhotoImage(im)

        self.CheckBut = Button(self.canv, bg = self.BG, relief = FLAT,
                               borderwidth = 0, cursor = "hand2",
                               highlightthickness = 0,
                               activebackground = self.BG,
                               image = self.CheckImg,
                               command = lambda: JsonManage.setup(self.File))
        
        self.canv.create_window(self.W//2, round(0.845*self.H),
                                anchor = CENTER, window = self.CheckBut)

        self.MainDesk()

    def MainDesk(self):
        
        self.I = 0
        self.Elements = []
        self.CenterImages(self.Path + 'Images/Logo.png')

        txt = 'Your current version: 0.4.1'

        self.PrintText(txt, (self.W//2, round(0.08*self.H)))

    def CenterImages(self, way):

        im = Image.open(way)
        im.thumbnail((round(0.7877*self.W), round(0.2153*self.H)),
                     Image.ANTIALIAS)

        self.Elements.append(ImageTk.PhotoImage(im))
        self.canv.create_image(self.W//2, self.H//2, anchor = CENTER,
                               image = self.Elements[self.I])

        self.I += 1

    def PrintText(self, txt, coord):

        Text = Label(self.canv, text = txt, justify = CENTER,
                     font = ('Calibri', 24, 'bold'),
                     bg = self.BG, fg = 'white')

        self.Elements.append(Text)
        
        self.canv.create_window(coord,  window = self.Elements[self.I],
                                anchor = N)

        self.I += 1

    def Wait(self):

        pass


if __name__ == "__main__":

    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("{}x{}+2+3".format(w//5*2, h//5*2))
    root.title("Setup manager")
    root.resizable(False, False)

    win = Window(root, w//5*2, h//5*2)
    root.mainloop()

#Json_manage.CurrentVersion()
#Json_manage.Setup()
#path = Path('Files/reduced-config.0.4.1.json')
    

