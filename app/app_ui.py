import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import webbrowser
import customtkinter as ctk

LARGE_FONT = ("Verdana", 12)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(width=False, height=False)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frames = {}

        # self.container.grid_rowconfigure(0, weight=1)
        # self.container.grid_columnconfigure(0, weight=1)

        for F in (Home, One, Two):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)
        self.title("Sudoku Solver")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller
        self.image_path = None
        self.controller.title("Sudoku Solver")
        self.titlelabel = tk.Label(self, text="AI Sudoku Solver", relief=tk.RAISED, font="Consolas 18",
                                   bg="cyan")
        self.titlelabel.grid(row=0, columnspan=8, sticky="ew")
        self.selimg = tk.Button(self, text='Open image', command=self._open_img, relief=tk.RAISED, fg="blue",
                                bg="light blue", borderwidth=3, padx=20)
        self.selimg.grid(row=1, column=0, padx=5, pady=5)
        self.imagepathdisplay = tk.Entry(self, fg="gray", width=40, font="Consolas 12", borderwidth=3)
        self.imagepathdisplay.insert(0, "No Image Selected")
        self.imagepathdisplay.grid(row=1, column=1, padx=5, pady=5)

        self.imglabel = tk.Label(self, text="Preview", font="Consolas 10")
        self.imglabel.grid(row=2, columnspan=2, sticky="w", padx=3, pady=3)

        self.img = ImageTk.PhotoImage(Image.open("default_img.png").resize((490, 450), Image.ANTIALIAS))
        self.imgpanel = tk.Label(self, image=self.img)
        self.imgpanel.grid(row=3, columnspan=2, padx=15, pady=3)

        self.exitbut = tk.Button(self, text="Exit", command=self._exit, padx=30, fg="red", bg="lightblue")
        self.exitbut.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.nextbut = tk.Button(self, text="Next", command=self._next, padx=30, fg="gray")
        self.nextbut.grid(row=4, column=1, padx=5, pady=5, sticky="e")
        self.mylink = tk.Label(self, text="@SiddhantMahalle", borderwidth=3, relief=tk.SUNKEN, fg="blue",
                               cursor="hand2")

        self.mylink.grid(row=5, columnspan=6, sticky="ew")
        self.mylink.bind("<Button-1>", lambda e: self._callback("https://github.com/siddhantmahalle"))

        # label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)

        # button = tk.Button(self, text="Visit Page 1",
        #                    command=lambda: controller.show_frame(One))
        # button.pack()
        #
        # button2 = tk.Button(self, text="Visit Page 2",
        #                     command=lambda: controller.show_frame(Two))
        # button2.pack()

    def _open_img(self):
        try:
            filename = tk.filedialog.askopenfilename(title='open')
        except:
            return

        try:
            img = Image.open(filename)
        except:
            messagebox.showerror("ERROR", "Non Image File selected")
            return

        self.selectedimagepath = filename
        self.imagepathdisplay.configure(fg="black")
        self.imagepathdisplay.delete(0, tk.END)
        self.imagepathdisplay.insert(0, filename)
        img = img.resize((490, 450), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.imgpanel.configure(image=img)
        self.img = img
        self.nextbut.configure(fg="black")

    def _callback(self, url):
        webbrowser.open_new(url)

    def _next(self):
        if self.selectedimagepath is None:
            messagebox.showerror("Error", "Image not selected!")
            return
        self.controller.frames[One].setselectedimgpath()
        self.controller.get_and_set_board()
        self.controller.show_frame(One)
        self.controller.title("One")

    def _exit(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.controller.cleanup()
            self.controller.destroy()
        else:
            pass


class One(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Home))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(Two))
        button2.pack()


class Two(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Home))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(One))
        button2.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
