from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from PIL import ImageTk, Image
# from threading import Thread

import json
import json_update


class Window(object):

    def __init__(self, master, root_w, root_h):

        # Main window sizes

        self.master = master
        self.min_w = self.w = root_w
        self.min_h = self.h = root_h

        self.canv = None

        # Creating variables

        self.path = ""
        self.file = "files/reduced-config.json"
        self.updates = "changes.json"

        # Colors

        self.bg_main = Style().change_scroll_bg
        self.bg_code = Style().code_scroll_bg

        self.scroll_color = Style().scroll_color

        # Apply buttons

        self.pic = None
        self.apply_img = []
        self.apply_buts_coord = None

        # Entry sections

        self.entries_h = None
        self.entry_sections = []
        self.version_enter = None

        # Code

        self.code_frame = None
        self.code_scroll = None
        self.code = None

        # Changes

        self.changes_frame = None
        self.changes_scroll = None

        self.notice_font = None
        self.notice = []
        self.j = 0

        # Versions

        self.versions = {}

        # Modules

        self.menubutton = None
        self.module = "main"

    def main(self):

        # Create canvas bind on changing size

        self.create_canvas()

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

        self.entries_h = [
            round(0.237 * self.h),
            round(0.276 * self.h),
            round(0.527 * self.h),
            round(0.566 * self.h),
            round(0.845 * self.h)
        ]

        [self.create_entry_sections(i) for i in range(5)]

        # Create listbox with versions

        self.create_modules_listbox()

        # Create entry for version

        self.create_version_entry()

        # Show start code from file

        self.create_code_scrolls()
        self.show_code()

        # Show changes

        self.create_changes_scroll()
        self.show_changes()

    def create_canvas(self):

        self.canv = Canvas(self.master, width=self.w, height=self.h, bd=0,
                           bg=self.bg_main, highlightthickness=0)

        self.canv.pack(anchor=W, fill="both", expand=True)

        self.canv.bind("<Configure>", self.change_window_size)

    def change_window_size(self, event):

        if event.width >= self.min_w and event.height >= self.min_h:

            w_scale = float(event.width) / self.w
            h_scale = float(event.height) / self.h

            self.w = event.width
            self.h = event.height

            self.canv.scale("all", 0, 0, w_scale, h_scale)
            self.canv.after(30, self.create_bg)

    def create_bg(self):

        self.pic = ImageTk.PhotoImage(Image.open(self.path +
                                                 'images/background.png')
                                      .resize((self.w, self.h),
                                              Image.ANTIALIAS))

        self.canv.create_image(0, 0, image=self.pic, anchor=NW)

    def create_apply_buts(self, name, j):

        im = Image.open(self.path + 'images/apply_but.png')
        im = im.resize((round(0.091 * self.w), round(0.0537 * self.h)),
                       Image.ANTIALIAS)
        self.apply_img.append(ImageTk.PhotoImage(im))

        apply_but = Button(self.canv, bg=self.bg_main, cursor="hand2",
                           relief=FLAT, bd=0, highlightthickness=0,
                           activebackground="white",
                           image=self.apply_img[j],
                           command=lambda arg=name:
                           self.change_file(arg))

        self.canv.create_window(self.apply_buts_coord[j],
                                anchor=CENTER, window=apply_but)

    def create_entry_sections(self, j):

        entry_w = round(0.01485 * self.w)

        enter = Entry(self.canv, width=entry_w, bg='#e8e9ea',
                      selectbackground='#85888b',
                      font=('Calibri', 13, 'bold italic'))

        self.entry_sections.append(enter)

        self.canv.create_window(round(0.18 * self.w), self.entries_h[j],
                                anchor="center", window=enter)

    def create_modules_listbox(self):

        data = self.open(self.file)

        forms = ["main"]
        forms.extend(list(data["modules"].keys()))

        self.menubutton = Menubutton(self.canv, text="main module",
                                     bg=self.bg_main, fg="white",
                                     relief="flat", bd=1,
                                     highlightthickness=1,
                                     font="Calibri 12 bold italic",
                                     activebackground=self.bg_main,
                                     activeforeground="white",
                                     cursor="hand2", width=16)

        self.menubutton.menu = Menu(self.menubutton,
                                    fg="#343b40", tearoff=0,
                                    font="Calibri 11 bold italic",
                                    activebackground=self.bg_main,
                                    activeforeground="white",
                                    activeborderwidth=0)

        self.menubutton["menu"] = self.menubutton.menu

        for link in forms:
            self.menubutton.menu.add_command(
                label=link,
                command=lambda temp=link: self.module_select(temp))

        self.canv.create_window(round(0.04 * self.w), round(0.0254 * self.h),
                                anchor=NW, window=self.menubutton)

    def module_select(self, link):

        self.module = link
        self.menubutton.configure(text=link)

        data = self.open(self.file)

        if self.module == "main":
            inf = data
        else:
            inf = data["modules"][self.module]

        self.create_code_scrolls()
        self.code.destroy()

        self.show_code(json.dumps(inf, indent=2, ensure_ascii=False).strip())
        self.show_changes(clear=True)

    def create_version_entry(self):

        coord = (round(0.159 * self.w), round(0.0254 * self.h))
        entry_w = round(0.009 * self.w)

        self.version_enter = Entry(self.canv, width=entry_w, bg='#e8e9ea',
                                   selectbackground='#85888b',
                                   font=('Calibri', 16, 'bold italic'))

        self.canv.focus_set()

        self.version_enter.bind("<KeyRelease>",
                                lambda event: self.show_changes(clear=True))

        self.canv.create_window(coord, anchor=NW, window=self.version_enter)

    def create_code_scrolls(self):

        # Set style for code scroll bars

        Style().vertical_scrollbar_code()
        Style().horizontal_scrollbar_code()

        # Creating scroll region for code

        section = Frame(self.canv)
        self.canv.create_window(round(0.7786 * self.w),
                                round(0.5472 * self.h),
                                anchor="center", window=section)

        self.code_scroll = Canvas(section, highlightthickness=0,
                                  width=round(0.41 * self.w),
                                  height=round(0.843 * self.h),
                                  bg=self.bg_code, bd=0)

        vsb = ttk.Scrollbar(section, orient=VERTICAL,
                            command=self.code_scroll.yview)
        hsb = ttk.Scrollbar(section, orient=HORIZONTAL,
                            command=self.code_scroll.xview)

        self.code_scroll.config(yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        hsb.pack(side=BOTTOM, fill=X)

        self.code_frame = ttk.Frame(self.code_scroll)

        self.code_scroll.pack()
        self.code_scroll.create_window((0, 0), window=self.code_frame, anchor=NW)

        self.code_frame.bind("<Configure>", lambda event: self.code_configure())
        self.code_frame.bind_all("<MouseWheel>", self.mouse_wheel)

        # Creating rectangle to cover the area

        self.code_scroll.create_rectangle(0, 0, round(0.41 * self.w),
                                          round(0.841 * self.h),
                                          fill=self.bg_code,
                                          outline=self.bg_code)

    def show_code(self, txt=None):

        # Load versions and check JSON file

        try:
            # Parsing
            self.write(self.file, self.open(self.file))

            data = self.open(self.file)

            changes = self.open(self.updates)

            self.versions["main"] = list(changes.get("main", [data["settings_version"]]))
            for key in data["modules"]:
                self.versions[key] = list(changes.get(
                    key, [data["modules"][key]["settings_version"]]
                    )
                )

            if self.module != "main":
                data = data["modules"][self.module]

        except json.decoder.JSONDecodeError:
            data = 'Incorrect JSON file'

        # Show code from file with ability to copy text

        code_font = Font(family='Droid Sans Mono', size=13)

        data = json.dumps(data, indent=2, ensure_ascii=False)
        data = txt if txt else data

        row = len(data.split('\n'))
        column = max(map(lambda a: len(a), data.split('\n')))

        self.code = Text(self.code_frame, width=column + 1, height=row + 1,
                         bg=self.bg_code, fg='white', font=code_font,
                         selectbackground=self.scroll_color,
                         bd=0, highlightthickness=0)

        self.code.insert(END, data)
        self.code['state'] = DISABLED

        self.code.pack(side=LEFT)

    def code_configure(self):

        self.code_scroll \
            .configure(scrollregion=self.code_scroll.bbox("all"))

    def changes_configure(self):

        self.changes_scroll \
            .configure(scrollregion=self.changes_scroll.bbox("all"))

    def mouse_wheel(self, event):

        # Connecting mouse wheel to all scrollbars

        cursor_x = self.master.winfo_pointerx() - self.master.winfo_rootx()

        if cursor_x > round(0.56 * self.w):
            self.code_scroll.yview_scroll(-1*(event.delta//120), "units")
        else:
            self.changes_scroll.yview_scroll(-1*(event.delta//120), "units")

    def change_version(self, module, new_version):

        data = self.open(self.file)

        if module == "main":
            data['settings_version'] = new_version
        else:
            data["modules"][module]['settings_version'] = new_version

        self.write(self.file, data)

    def change_file(self, func_name):

        current_version = self.version_enter.get()
        if len(self.versions[self.module]) == 0:
            previous_versions = []
            last = None
        else:
            previous_versions = self.versions[self.module][:-1]
            last = self.versions[self.module][-1]

        # Check if the version is not last or empty

        if current_version in previous_versions:
            error = "You can change only\n" + \
                    "last version"
            self.show_changes(error)

        elif current_version == "":
            error = 'Please, write version'
            self.show_changes(error)

        else:
            try:
                # Set last versions

                if current_version != last:
                    self.versions[self.module].append(current_version)
                    self.change_version(self.module, current_version)

                # Update code if there are no errors

                inf = self.open(self.file)
                data = inf if self.module == "main" \
                    else inf["modules"][self.module]

                self.update_code(func_name, data)

                self.write(self.file, inf)

                # Update modules listbox

                if self.module == "main":
                    self.create_modules_listbox()

                # Clear entries

                for enter in self.entry_sections:
                    enter.delete(0, 'end')

                self.code.destroy()
                self.show_code()

            # Checking for errors

            except (TypeError, IndexError, KeyError):
                error = 'Incorrect way\n' + \
                        'Please, try again'
                self.show_changes(error)

            except json.decoder.JSONDecodeError:
                error = 'Wrong data\n' + \
                        'Please, try again'
                self.show_changes(error)

    def update_code(self, name, data):

        # Start update functions from json_update

        funcs = ['add', 'move', 'delete']

        way = self.entry_sections[funcs.index(name) * 2].get()
        inf = self.open(self.updates)

        if self.module == "main" and (len(way.split("/")) != 2 or
                                      way.split("/")[0] != "modules" or
                                      name == "move"):

            # Check for operations in main module

            error = 'You can only add and delete\n' + \
                    'modules in main module'
            self.show_changes(error)

        elif name == 'add' or name == 'move':

            ch = self.entry_sections[funcs.index(name) * 2 + 1].get()

            # Checking for match up in changes

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
                way_new = getattr(json_update, name)(way, data, ch)

                # Add settings version in new module
                if self.module == "main":
                    data["modules"][way.split("/")[1]] = {}

                    ch = ch if isinstance(json.loads(ch), str) \
                        else "\"0.1.0\""

                    data["modules"][way.split("/")[1]]["settings_version"] = \
                        json.loads(ch)

                self.add_changes(name, way_new, ch)

        else:
            ch = json_update.finder(way, data)

            getattr(json_update, name)(way, data)
            self.add_changes(name, way, ch)

    def add_changes(self, name, way, value):

        # Write changes in file

        version = self.version_enter.get()

        data_old = self.open(self.updates)

        # Add module in changes.json if it's not exist
        data = data_old.get(self.module, False)
        if not data:
            data_old[self.module] = {}
            data = data_old[self.module]

        # Add version in changes.json if it's not exist
        version_exist = data.get(version, False)
        if not version_exist:
            data[version] = []

        inf = {name: way}

        if name == 'add':
            inf['data'] = json.loads(value)
        elif name == 'move':
            inf['to'] = value
        else:
            inf['value'] = value

        data[version].append(inf)

        self.write(self.updates, data_old)
        self.show_changes(clear=True)

    def create_changes_scroll(self):

        # Set changes scrollbar style

        Style().vertical_scrollbar_changes()

        # Creating vertical scrollbar for changes

        section = Frame(self.canv)
        self.canv.create_window(round(0.427 * self.w), round(0.546 * self.h),
                                anchor="center", window=section)

        self.changes_scroll = Canvas(section, highlightthickness=0,
                                     width=round(0.23 * self.w),
                                     height=round(0.87 * self.h),
                                     bg=self.bg_main, bd=0)

        vsb = ttk.Scrollbar(section, orient=VERTICAL,
                            style="Changes.Vertical.TScrollbar",
                            command=self.changes_scroll.yview)

        self.changes_scroll.config(yscrollcommand=vsb.set)

        vsb.pack(side=RIGHT, fill=Y)

        self.changes_frame = ttk.Frame(self.changes_scroll)

        self.changes_scroll.pack()
        self.changes_scroll.create_window(0, 0, window=self.changes_frame,
                                          anchor=NW)

        self.changes_frame.bind("<Configure>",
                                lambda event: self.changes_configure())
        self.changes_frame.bind_all("<MouseWheel>", self.mouse_wheel)

        # Creating rectangle to cover the area

        self.changes_scroll.create_rectangle(0, 0, round(0.23 * self.w),
                                             round(0.87 * self.h),
                                             fill=self.bg_main,
                                             outline=self.bg_main)

    def show_changes(self, error=None, clear=None, refresh_code=None):

        # Clear section

        if clear or self.j == 0:
            [n.destroy() for n in self.notice]
            self.j = 0

            if clear == "delete_version":
                try:
                    self.versions[self.module].pop(-1)
                    self.change_version(self.module,
                                        self.versions[self.module][-1])
                except IndexError:
                    pass

            if refresh_code:
                self.code.destroy()
                self.show_code()

        # Set font

        self.notice_font = Font(family="Conduit ITC Light", size=14)

        # Print errors and changes from file

        data = self.open(self.updates)
        module = data.get(self.module, False)

        if module:
            changes = module.get(self.version_enter.get(), False)
        else:
            changes = module

        if error:

            self.create_notice(error, 'nw', color='#bf5051', draw_line=True)

        elif changes:

            for change in changes:

                txt = ''
                for key, value in change.items():
                    txt += str(key.title()) + ': ' + str(value) + '\n'

                delete = None
                if self.version_enter.get() == \
                        self.versions[self.module][-1]:
                    delete = len(list(changes)) - 1

                self.create_notice(txt.strip(), 'nw', draw_line=True,
                                   delete_but=delete)
                self.j += 1

        else:

            coord = (round(0.23 * self.min_w) // 2,
                     round(0.87 * self.min_h) // 2)

            height = round(0.87 * self.min_h)

            txt = "No changes found"

            self.create_notice(txt, 'center', coord, height, side='center')

    def create_notice(self, txt, anchor, coord=None, height=None,
                      draw_line=None, color=None, side=None,
                      delete_but=None):

        # Show current change

        font = color if color else "white"
        side = side if side else "left"
        coord = coord if coord else (0, 0)

        indent = 63
        height = height if height else indent + 10

        if delete_but == self.j:
            height += 45

        canvas = Canvas(self.changes_frame, width=round(0.23 * self.min_w),
                        bg=self.bg_main, height=height,
                        bd=0, highlightthickness=0,)

        for line in txt.split("\n"):
            self.create_label(canvas, line, coord, anchor, side, font)
            coord = (0, 25) if coord == (0, 0) else coord

        # Create delete button to last change

        if delete_but == self.j:
            but = Button(canvas, bd=1, text='Undo', cursor='hand2',
                         activebackground=self.bg_main, width=32,
                         highlightcolor="white", highlightthickness=1,
                         font=self.notice_font, relief=SOLID,
                         bg=self.bg_main, fg="#b1292a",
                         command=lambda num=self.j, text=txt:
                         self.cancel_action(num, text))
            canvas.create_window(round(0.22 * self.min_w) // 2, indent,
                                 anchor=N, window=but)
            indent += 50

        if draw_line:
            canvas.create_line(0, indent, round(0.22 * self.min_w), indent,
                               fill="#5e6367", width=3)

        self.notice.append(canvas)

        canvas.grid(row=self.j, column=0)

    def create_label(self, canvas, txt, coord, anchor, side, font):

        lbl = Label(canvas, text=self.cut_inf(txt), bg=self.bg_main, fg=font,
                    font=self.notice_font, justify=side, cursor="hand2")

        if txt != "No changes found":
            lbl.bind("<Button-1>", lambda event: self.insert_text(txt))

        canvas.create_window(coord, anchor=anchor, window=lbl)

    def cancel_action(self, n, txt):

        # Undo the action

        data = self.open(self.updates)

        changes = data[self.module][self.version_enter.get()]
        changes.pop(n)

        # Delete version if length of list changes is equally zero

        clear = True
        if len(changes) == 0:
            del data[self.module][self.version_enter.get()]
            clear = 'delete_version'

        inf = self.open(self.file)
        code = inf if self.module == "main" else inf["modules"][self.module]

        json_update.undo(txt, code)

        self.write(self.updates, data)
        self.write(self.file, inf)

        if self.module == "main":
            self.create_modules_listbox()

        self.show_changes(clear=clear, refresh_code=True)

    def insert_text(self, txt):

        if self.canv.focus_get() not in self.entry_sections:
            self.entry_sections[0].focus_set()

        self.canv.focus_get().delete(0, 'end')
        self.canv.focus_get().insert(END, txt.split(': ')[1])

    @staticmethod
    def cut_inf(s):

        # Cut information if it is too long

        return s if len(list(s)) < 31 else s[:31] + '...'

    @staticmethod
    def open(file):

        with open(file, 'r') as jr:
            return json.loads(jr.read())

    @staticmethod
    def write(file, data):

        with open(file, 'w') as jw:
            json.dump(data, jw, indent=2, ensure_ascii=False)


class Style(object):

    def __init__(self):

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.code_scroll_bg = "#252a2e"
        self.change_scroll_bg = "#2c3237"

        self.scroll_color = "#929597"

    def vertical_scrollbar_code(self):

        self.style.configure("Vertical.TScrollbar",
                             gripcount=0,
                             background=self.scroll_color,
                             darkcolor=self.scroll_color,
                             lightcolor=self.scroll_color,
                             troughcolor=self.code_scroll_bg,
                             bordercolor=self.code_scroll_bg,
                             arrowcolor=self.scroll_color)

    def horizontal_scrollbar_code(self):

        self.style.configure("Horizontal.TScrollbar",
                             gripcount=0,
                             background=self.scroll_color,
                             darkcolor=self.scroll_color,
                             lightcolor=self.scroll_color,
                             troughcolor=self.code_scroll_bg,
                             bordercolor=self.code_scroll_bg,
                             arrowcolor=self.scroll_color)

    def vertical_scrollbar_changes(self):

        self.style.configure("Changes.Vertical.TScrollbar",
                             gripcount=0,
                             background=self.scroll_color,
                             darkcolor=self.scroll_color,
                             lightcolor=self.scroll_color,
                             troughcolor=self.change_scroll_bg,
                             bordercolor=self.change_scroll_bg,
                             arrowcolor=self.scroll_color)


if __name__ == "__main__":

    # Creating main window

    root = Tk()
    root.title("Setup manager")

    # root.iconbitmap("images/logo.ico")

    screen_size = (root.winfo_screenwidth(), root.winfo_screenheight())

    h = round(0.7*screen_size[1])
    w = h//9*16

    x = screen_size[0] // 2 - w // 2
    y = screen_size[1] // 2 - h // 2

    root.geometry("{}x{}+{}+{}".format(w, h, x, y))

    Window(root, w, h).main()

    root.mainloop()
