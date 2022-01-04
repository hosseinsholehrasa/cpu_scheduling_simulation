import time
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

from PIL import ImageTk, Image
from simulator import Simulator
from pathlib import Path

gp_folder = Path('graphics/')


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


def show_information_page(simulator):
    information_page = tk.Toplevel()
    information_page.geometry('550x450+350+40')
    information_page.title(f"{simulator.algorithm} Information")
    information_page.minsize(width=450, height=400)
    information_page.maxsize(width=650, height=600)

    # background
    label_image = tk.PhotoImage(file=gp_folder / 'bg.png')
    label_bg = tk.Label(information_page, image=label_image, relief=tk.FLAT)
    label_bg.place(relwidth=1, relheight=1)

    # information lables
    tk.Label(
        information_page, text=f'{simulator.__str__()}', font=("Courier", 16)
    ).pack()

    # plot algorithm result button
    def plot_algorithm_result_button():
        m3 = messagebox.askokcancel("Waiting", "You have to wait until images be generate "
                                               "You can find images in 'results' folder \n"
                                               "Do you want to continue")
        if not m3:
            return 0
        simulator.plot_algorithm_result()

    tk.Button(
        information_page, text='plot result', font=("chiller", 18), height=2, width=8,
        bg="maroon3", fg="yellow", command=plot_algorithm_result_button
    ).pack(side=tk.BOTTOM)

    # rerun algorithm
    def rerun_button():
        m2 = messagebox.askokcancel("Waiting", "You have to wait until simulation be complete "
                                               "then your screen will unfreeze!\n Do you want to continue\n"
                                               "(30-60 seconds need)")
        if not m2:
            return 0
        simulator.read_processes_data()
        simulator.run()
        print(simulator.__str__())
        simulator.save_result_simulation()
        information_page.destroy()
        show_information_page(simulator)

    tk.Button(
        information_page, text='Re Run', font=("chiller", 18), height=2, width=8,
        bg="maroon3", fg="yellow", command=rerun_button
    ).pack(side=tk.BOTTOM)

    information_page.mainloop()


def run():
    main_window = tk.Tk()
    main_window.geometry('850x700+350+40')
    main_window.title("CPU Simulator")
    main_window.resizable(0, 0)

    animation = AnimatedGIF(main_window, gp_folder / "gk.gif")
    animation.place(x=-1, y=-1)

    label = tk.Label(main_window, text='CPU Scheduling Simulation', font=("Courier", 32))
    label.place(x=100, y=30)

    ########################################## Algo page ########################################################
    # Next page after menu to choose an algorithm
    def algo_page(simulator=None):
        algorithm_page = tk.Toplevel()
        main_window.withdraw()
        algorithm_page.title("CPU Simulator")
        algorithm_page.geometry("850x700+350+40")
        algorithm_page.resizable(0, 0)

        # animation
        animation = AnimatedGIF(algorithm_page, gp_folder / "giphy.gif")
        animation.place(x=-1, y=-1)

        def choose_algorithm_button(algorithm: str):
            if algorithm not in simulator.algorithms_list:
                messagebox.showerror("Error", "Invalid Algorithm")
                return 0
            m2 = messagebox.askokcancel("Waiting", "You have to wait until simulation be complete "
                                                   "then your screen will unfreeze!\n Do you want to continue\n"
                                                   "(30-60 seconds need)")
            if not m2:
                return 0

            simulator.set_algorithm(algorithm)
            simulator.read_processes_data()
            simulator.run()
            print(simulator.__str__())
            simulator.save_result_simulation()

            # show information page
            show_information_page(simulator)

        # algorithm buttons

        # FCFS button
        btn_fcfs = tk.Button(
            algorithm_page, text='FCFS', font=("chiller", 18), height=2, width=8,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("FCFS")
        ).place(x=60, y=200)

        # preemptive priority
        btn_pp = tk.Button(
            algorithm_page, text='Preemptive Priority', font=("chiller", 18), height=2, width=15,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("PreemptivePriority")
        ).place(x=220, y=200)

        # non preemptive priority
        btn_p = tk.Button(
            algorithm_page, text='Non-Preemptive Priority', font=("chiller", 18), height=2, width=18,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("NonPreemptivePriority")
        ).place(x=480, y=200)

        # RR
        btn_rr = tk.Button(
            algorithm_page, text='RR', font=("chiller", 18), height=2, width=8,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("RR")
        ).place(x=60, y=300)

        # preemptive SF
        btn_psfj = tk.Button(
            algorithm_page, text='Preemptive SFJ', font=("chiller", 18), height=2, width=15,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("PreemptiveSFJ")
        ).place(x=220, y=300)

        # non-preemptive SFJ
        btn_sfj = tk.Button(
            algorithm_page, text='Non-Preemptive SFJ', font=("chiller", 18), height=2, width=18,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("NonPreemptiveSFJ")
        ).place(x=480, y=300)

        # back
        def back_button_command():
            algorithm_page.destroy()
            main_window.deiconify()

        btn_back = tk.Button(
            algorithm_page, text='back', font=("chiller", 18), height=2, width=8,
            bg="maroon3", fg="yellow", command=back_button_command
        ).place(x=30, y=600)

        # analyze all algorithms
        def analyze_all_button():
            m1 = messagebox.askyesno(
                "Analyzer", "Do you want to run all algorithms first?\n(You have to wait)", icon='warning'
            )
            if m1:
                for alg in simulator.algorithms_list:
                    s = Simulator(alg)
                    s.read_processes_data()
                    s.run()
                    print(s.__str__())
                    s.save_result_simulation()
            simulator.analyze_algorithms()

        btn_analyzer = tk.Button(
            algorithm_page, text='Analyze All', font=("chiller", 18), height=2, width=10,
            bg="maroon3", fg="yellow", command=analyze_all_button
        ).place(x=640, y=600)

        algorithm_page.mainloop()

    ########################################## main page ########################################################

    # generate button
    def generate_button_command():
        path = 'data.csv'
        answer = simpledialog.askinteger("generation number", "How many processes do you want?",
                                         parent=main_window)
        if answer:
            number = answer
        else:
            return 0

        result = Simulator.generate_processes_data(path, number)
        if result:
            messagebox.showinfo("Info", f"{number} processes generated in {path}")
            # going to next page
            simulator = Simulator("FCFS")
            simulator.read_processes_data()
            algo_page(simulator)

    btn_generate = tk.Button(main_window, text='Generate Processes', font=("chiller", 18), height=2, width=20,
                             bg="maroon3", fg="yellow", command=generate_button_command)
    btn_generate.place(x=250, y=250)

    # load button
    def load_button_command():
        path = 'data.csv'
        simulator = Simulator("FCFS")
        result = simulator.read_processes_data()
        if result:
            messagebox.showinfo("Info", f"{len(simulator.processes)} loaded processes from {path}")
            # going to next page
            algo_page(simulator)

    btn_load = tk.Button(main_window, text='Load Processes', font=("chiller", 18), height=2, width=20,
                         bg="maroon3", fg="yellow", command=load_button_command)
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
