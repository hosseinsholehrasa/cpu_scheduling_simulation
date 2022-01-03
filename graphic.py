import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk, Image
from simulator import Simulator


class AnimatedGIF(tk.Label, object):
    def __init__(self, master, path, forever=True, bg='gray95'):
        self.bg = bg
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im)
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError:
            pass

        self._last_index = len(self._frames) - 1

        self._delay = 40

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0], background=self.bg)

    def start_animation(self, frame=None):
        if self._is_running:
            return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame], background=self.bg)

        self._master.after(self._delay, self._animate_gif)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running:
            return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_gif(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc], background=self.bg)

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_gif)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_gif)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)


def run():
    main_window = tk.Tk()
    main_window.geometry('850x700+350+40')
    main_window.title("CPU Scheduling Simulation")
    main_window.resizable(0, 0)
    canvas = tk.Canvas(main_window, width=600, height=400)
    canvas.pack()
    bg = tk.Label(main_window, bg='gray95')
    bg.place(relwidth=1, relheight=1)

    animation = AnimatedGIF(main_window, "gk.gif")
    animation.place(x=-1, y=-1)

    # generate button
    def generte_button_command():
        path = 'data2.csv'
        number = 1000
        result = Simulator.generate_processes_data(path, number)
        if result:
            messagebox.showinfo("Info", f"{number} processes generated in {path}")
    btn_generate = tk.Button(main_window, text='Generate Processes', font=("chiller", 18), height=2, width=20,
                             bg="deeppink3", fg="yellow", command=generte_button_command)
    btn_generate.place(x=250, y=250)
    # load button
    btn_load = tk.Button(main_window, text='Load Processes', font=("chiller", 18),
                         height=2, width=20, bg="maroon3", fg="yellow")
    btn_load.place(x=250, y=350)

    # exit button
    def exit_button_command():
        m1 = messagebox.askyesno("Exit Box", "are you sure you want to exit?")
        if m1:
            main_window.destroy()

    b_exit = tk.Button(main_window, text="exit", font=("chiller", 17),
                       height=2, width=10, bg="maroon3", fg="yellow", command=exit_button_command)
    b_exit.place(x=330, y=450)

    main_window.mainloop()
