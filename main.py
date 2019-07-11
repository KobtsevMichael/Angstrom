from tkinter import*
from tkinter import ttk
from tkinter.font import Font
from PIL import ImageTk, Image

import json
import json_update


class Window:

    def __init__(self, master, root_w, root_h):

        # Creating main window

        self.master = master
        self.w = root_w
        self.h = root_h
        
        self.canv = Canvas(master, width=self.w, height=self.h, bg='#232426',
                           highlightthickness=0, borderwidth=0)
        self.canv.pack(side=LEFT)

        # Creating variables

        self.path = ''
        self.bg = '#146098'
        self.file = 'Test/basic.json'

        self.bg = "#2c3237"
        self.bg2 = "#252a2e"
        self.scroll_color = "#929597"

        self.pic = None
        self.apply_img = []
        self.apply_buts_coord = None

        self.entry_sections = []
        self.enter_h = None
        self.version_enter = None

        self.code_scroll = None
        self.code = None

        self.frame = None
        self.changes_scroll = None

        self.notice_font = None
        self.notice = []
        self.j = 0

        self.start_version = 0

        self.main()

    def main(self):

        # Creating background

        self.create_bg()

        # Set names and coordinates for apply buttons

        funcs = ['add', 'move', 'delete']
        self.apply_buts_coord = [
            (round(0.2114 * self.w), round(0.335 * self.h)),
            (round(0.2114 * self.w), round(0.627 * self.h)),
            (round(0.2114 * self.w), round(0.922 * self.h))
        ]

        [self.create_apply_buts(funcs[i], i) for i in range(3)]

        # Set coordinates for enter sections

        self.enter_h = [
            round(0.224 * self.h),
            round(0.263 * self.h),
            round(0.514 * self.h),
            round(0.553 * self.h),
            round(0.829 * self.h)
        ]

        [self.create_entry_sections(i) for i in range(5)]

        # Create entry for version

        self.create_version_entry()

        # Show start code from file

        self.set_scrolls_style()
        self.show_code()

        # Show changes

        self.create_changes_scroll()
        self.show_changes()

    def create_bg(self):

        self.pic = ImageTk.PhotoImage(Image.open(self.path + 'Images/bg.png')
                                      .resize((self.w, self.h), Image.ANTIALIAS))

        self.canv.create_image(0, 0, image=self.pic, anchor=NW)

        self.canv.tag_lower(self.pic)

    def create_apply_buts(self, name, j):

        im = Image.open(self.path+'Images/ApplyBut.png')
        im = im.resize((round(0.091 * self.w), round(0.0537 * self.h)),
                       Image.ANTIALIAS)
        self.apply_img.append(ImageTk.PhotoImage(im))

        apply_but = Button(self.canv, bg=self.bg, relief=FLAT,
                           borderwidth=0, cursor="hand2",
                           highlightthickness=0,
                           activebackground=self.bg,
                           image=self.apply_img[j],
                           command=lambda arg=name:
                               self.change_file(arg))
        
        self.canv.create_window(self.apply_buts_coord[j],
                                anchor=CENTER, window=apply_but)

    def create_entry_sections(self, j):

        enter = Entry(self.canv, width=20, bg='#e8e9ea',
                      selectbackground='#85888b',
                      font=('Calibri', 13, 'bold italic'))

        self.entry_sections.append(enter)

        self.canv.create_window(round(0.109 * self.w), self.enter_h[j],
                                anchor=NW, window=enter)

    def create_version_entry(self):

        coord = (round(0.146 * self.w), round(0.025 * self.h))

        self.version_enter = Entry(self.canv, width=13, bg='#e8e9ea',
                                   selectbackground='#85888b',
                                   font=('Calibri', 16, 'bold'))

        self.canv.focus_set()

        self.version_enter.bind("<KeyRelease>",
                                lambda event: self.show_changes(clear=True))

        self.canv.create_window(coord, anchor=NW, window=self.version_enter)

    def set_scrolls_style(self):

        # Set style for code scroll bars

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Horizontal.TScrollbar",
                        gripcount=0,
                        background=self.scroll_color,
                        darkcolor=self.scroll_color,
                        lightcolor=self.scroll_color,
                        troughcolor=self.bg2,
                        bordercolor=self.bg2,
                        arrowcolor=self.scroll_color)

        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=self.scroll_color,
                        darkcolor=self.scroll_color,
                        lightcolor=self.scroll_color,
                        troughcolor=self.bg2,
                        bordercolor=self.bg2,
                        arrowcolor=self.scroll_color)

    def show_code(self):

        # Creating scroll region for code

        section = Frame(self.canv)
        self.canv.create_window(self.w - 12, self.h - 15,
                                anchor=SE, window=section)

        self.code_scroll = Canvas(section, highlightthicknes=0,
                                  width=round(0.41 * self.w),
                                  height=round(0.843 * self.h),
                                  bg=self.bg2, bd=0)

        vsb = ttk.Scrollbar(section, orient=VERTICAL,
                            command=self.code_scroll.yview)
        hsb = ttk.Scrollbar(section, orient=HORIZONTAL,
                            command=self.code_scroll.xview)

        self.code_scroll.config(yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        hsb.pack(side=BOTTOM, fill=X)

        frame = ttk.Frame(self.code_scroll)

        self.code_scroll.pack()
        self.code_scroll.create_window((0, 0), window=frame, anchor=NW)

        frame.bind("<Configure>", lambda event: self.code_configure())
        frame.bind_all("<MouseWheel>", self.mouse_wheel)

        self.code_scroll.create_rectangle(0, 0, round(0.409 * self.w),
                                          round(0.841 * self.h),
                                          fill=self.bg2,
                                          outline=self.bg2)

        # Set first version and check JSON file
        try:
            self.change_version()

            with open('changes.json', 'r') as f:
                inf = json.loads(f.read())

            for key, value in inf.items():
                if value == "first":
                    self.start_version = key

            with open(self.file, 'r') as f:
                data = f.read()

        except json.decoder.JSONDecodeError:
            data = 'Incorrect JSON file'

        # Show code from file with ability to copy text

        code_font = Font(family='Droid Sans Mono', size=13)

        row = len(data.split('\n'))
        column = max(map(lambda x: len(x), data.split('\n')))

        self.code = Text(frame, width=column+1, height=row+1,
                         bg=self.bg2, fg='white', font=code_font,
                         selectbackground=self.scroll_color,
                         bd=0, highlightthicknes=0)

        self.code.insert(END, data)
        self.code['state'] = DISABLED

        self.code.pack(side=LEFT)

    def code_configure(self):

        self.code_scroll\
            .configure(scrollregion=self.code_scroll.bbox("all"))

    def changes_configure(self):

        self.changes_scroll\
            .configure(scrollregion=self.changes_scroll.bbox("all"))

    def mouse_wheel(self, event):

        # Connecting mouse wheel to all scrollbars

        cursor_x = self.canv.winfo_pointerx()

        if cursor_x > round(0.65 * self.w):
            self.code_scroll.yview_scroll(-1*(event.delta//120), "units")
        else:
            self.changes_scroll.yview_scroll(-1*(event.delta//120), "units")

    def change_version(self, new_version=None):

        with open(self.file, 'r') as jr:
            data = json.loads(jr.read())

        if new_version:
            data['settings_version'] = new_version

        with open(self.file, 'w') as jw:
            json.dump(data, jw, indent=2, ensure_ascii=False)

    def change_file(self, func_name):

        with open(self.file, 'r') as jr:
            data = json.loads(jr.read())

        if self.version_enter.get() == self.start_version:
            pass

        elif self.version_enter.get() != "":

            try:

                self.update(func_name, data)

                with open(self.file, 'w') as jw:
                    json.dump(data, jw, indent=2, ensure_ascii=False)

                self.code.destroy()
                self.show_code()

        # Checking for errors

            except (IndexError, KeyError):
                error = 'Incorrect way\n' + \
                        'Please, try again'
                self.show_changes(error)

            except json.decoder.JSONDecodeError:
                error = 'Wrong data\n' + \
                        'Please, try again'
                self.show_changes(error)

        else:
            error = 'Please, write version'
            self.show_changes(error)

    def update(self, name, data):

        # Start update functions from json_update

        funcs = ['add', 'move', 'delete']

        way = self.entry_sections[funcs.index(name) * 2].get()

        with open('changes.json', 'r') as f:
            inf = json.loads(f.read())

        if name == 'add' or name == 'move':

            ch = self.entry_sections[funcs.index(name) * 2 + 1].get()

            # Check for match up in changes
            match = False
            for change in inf.get(self.version_enter.get(), []):
                v = list(change.values())
                if v[0] == way and v[1] == ch:
                    match = True

            if match:
                error = 'Incorrect way\n' + \
                        'Please, try again'
                self.show_changes(error)
            else:
                getattr(json_update, name)(way, data, ch)
                self.add_changes(name, way, ch)

        else:
            getattr(json_update, name)(way, data)
            self.add_changes(name, way)

    def add_changes(self, name, way, value=None):

        # Write changes in file

        version = self.version_enter.get()

        with open('changes.json', 'r') as f:
            data = json.loads(f.read())

        version_exist = data.get(version, False)
        if not version_exist:
            data[version] = []

        inf = {name: way}

        if name == 'add':
            inf['data'] = json.loads(value)
        if name == 'move':
            inf['to'] = value

        data[version].append(inf)

        with open('changes.json', 'w') as write:
            json.dump(data, write, indent=2, ensure_ascii=False)

        self.show_changes(clear=True)

    def create_changes_scroll(self):

        # Set changes scrollbar style

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("My.Vertical.TScrollbar",
                        gripcount=0,
                        background=self.scroll_color,
                        darkcolor=self.scroll_color,
                        lightcolor=self.scroll_color,
                        troughcolor=self.bg,
                        bordercolor=self.bg,
                        arrowcolor=self.scroll_color)

        # Creating vertical scrollbar for changes

        section = Frame(self.canv)
        self.canv.create_window(round(0.31*self.w), round(0.11 * self.h),
                                anchor=NW, window=section)

        self.changes_scroll = Canvas(section, highlightthicknes=0,
                                     width=round(0.23 * self.w),
                                     height=round(0.87 * self.h),
                                     bg=self.bg, bd=0)

        vsb = ttk.Scrollbar(section, orient=VERTICAL,
                            style="My.Vertical.TScrollbar",
                            command=self.changes_scroll.yview)

        self.changes_scroll.config(yscrollcommand=vsb.set)

        vsb.pack(side=RIGHT, fill=Y)

        self.frame = ttk.Frame(self.changes_scroll)

        self.changes_scroll.pack()
        self.changes_scroll.create_window(0, 0, window=self.frame, anchor=NW)

        self.frame.bind("<Configure>", lambda event: self.changes_configure())
        self.frame.bind_all("<MouseWheel>", self.mouse_wheel)

        # Creating rectangle to cover the area

        self.changes_scroll.create_rectangle(0, 0, round(0.23 * self.w),
                                             round(0.87 * self.h),
                                             fill=self.bg,
                                             outline=self.bg)

    def show_changes(self, error=None, clear=None):

        # Clear section

        if clear or self.j == 0:
            [n.destroy() for n in self.notice]
            self.j = 0

        # Set font

        self.notice_font = Font(family="Conduit ITC Light", size=14)

        # Cut information if it is too long

        def cut_inf(s):

            s = str(s)
            return s if len(list(s)) < 28 else s[:29] + '...'

        # Print changes from file and errors

        with open('changes.json', 'r') as f:
            data = json.loads(f.read())

        changes = data.get(self.version_enter.get(), False)

        if error:

            self.create_notice(error, (0, 0), 'nw', color='#bf5051',
                               line=True)

        elif changes and changes != "first":

            self.change_version(self.version_enter.get())

            for change in changes:

                txt = ''
                for key, value in change.items():
                    txt += cut_inf(key.title()) + ': ' + \
                           cut_inf(value) + '\n'

                self.create_notice(txt.strip(), (0, 0), 'nw', line=True)
                self.j += 1

        else:

            coord = (round(0.23 * self.w)//2, round(0.87 * self.h)//2)
            height = round(0.87 * self.h)

            if changes == "first":
                txt = "You can't change\n" + \
                      "start version"
            else:
                txt = "No changes found"

            self.create_notice(txt, coord, 'center', height, side='center')

    def create_notice(self, txt, coord, anchor, height=None,
                      line=None, color=None, side=None):

        # Print current change

        font = color if color else "white"
        side = side if side else "left"

        indent = 70 if len(txt.split('\n')) == 2 else 50
        height = height if height else indent + 10

        canvas = Canvas(self.frame, width=round(0.23 * self.w), bg=self.bg,
                        highlightthicknes=0, bd=0, height=height)

        lbl = Label(self.frame, text=txt, bg=self.bg, fg=font,
                    font=self.notice_font, justify=side)
        canvas.create_window(coord, anchor=anchor, window=lbl)

        if line:
            canvas.create_line(0, indent, round(0.22 * self.w), indent,
                               fill=self.scroll_color)

        self.notice.append(canvas)

        canvas.grid(row=self.j, column=0)


if __name__ == "__main__":

    # Creating main window

    root = Tk()

    screen_size = (root.winfo_screenwidth(), root.winfo_screenheight())
    w, h = map(lambda x: round(0.7 * x), screen_size)

    root.geometry("{}x{}+2+3".format(w, h))
    root.title("Setup manager")
    root.resizable(False, False)

    win = Window(root, w, h)
    root.mainloop()
