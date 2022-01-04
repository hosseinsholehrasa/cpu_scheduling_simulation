import time
import tkinter as tk
from tkinter import messagebox

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


def show_information_page(data: dict, simulator):
    information_page = tk.Toplevel()
    information_page.geometry('650x600+350+40')
    information_page.title(f"{simulator.algorithm} Information")
    information_page.minsize(width=400, height=400)
    information_page.maxsize(width=850, height=700)

    # background
    label_image = tk.PhotoImage(file=gp_folder / 'bg.png')
    label_bg = tk.Label(information_page, image=label_image, relief=tk.FLAT)
    label_bg.place(relwidth=1, relheight=1)

    # rerun algorithm
    def rerun_button():
        simulator.run()
        print(simulator.__str__())
        simulator.save_result_simulation()
        information_page.destroy()
        show_information_page(simulator.json_export(), simulator)

    # plot algorithm result button
    def plot_algorithm_result_button():
        simulator.plot_algorithm_result()

    # exit button
    def exit_button_command():
        m1 = messagebox.askyesno("Exit Box", "are you sure you want to exit?")
        if m1:
            information_page.destroy()

    b_exit = tk.Button(
        information_page, text="exit", font=("chiller", 17),
        height=2, width=10, bg="maroon3", fg="yellow", command=exit_button_command
    ).place(x=330, y=450)

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

        # label
        label = tk.Label(
            algorithm_page, text='CPU Scheduling Simulation', font=("Courier", 30)
        ).place(x=120, y=30)

        def choose_algorithm_button(algorithm: str):
            if algorithm not in simulator.algorithms_list:
                messagebox.showerror("Error", "Invalid Algorithm")
                return 0
            simulator.set_algorithm(algorithm)
            simulator.run()
            print(simulator.__str__())
            simulator.save_result_simulation()
            simulate_data = simulator.json_export()
            # show information
            show_information_page(simulate_data, simulator)

        # algorithm buttons

        # FCFS button
        btn_fcfs = tk.Button(
            algorithm_page, text='FCFS', font=("chiller", 18), height=2, width=8,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("FCFS")
        )
        btn_fcfs.place(x=70, y=200)

        # preemptive priority
        btn_pp = tk.Button(
            algorithm_page, text='Preemptive Priority', font=("chiller", 18), height=2, width=15,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("PreemptivePriority")
        ).place(x=220, y=200)

        # non preemptive priority
        btn_p = tk.Button(
            algorithm_page, text='Non-Preemptive Priority', font=("chiller", 18), height=2, width=18,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("NonPreemptivePriority")
        ).place(x=475, y=200)

        # RR
        btn_rr = tk.Button(
            algorithm_page, text='RR', font=("chiller", 18), height=2, width=8,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("RR")
        ).place(x=70, y=350)

        # preemptive SF
        btn_psfj = tk.Button(
            algorithm_page, text='Preemptive SFJ', font=("chiller", 18), height=2, width=15,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("PreemptiveSFJ")
        ).place(x=220, y=350)

        # non-preemptive SFJ
        btn_sfj = tk.Button(
            algorithm_page, text='Non-Preemptive SFJ', font=("chiller", 18), height=2, width=18,
            bg="maroon3", fg="yellow", command=lambda: choose_algorithm_button("NonPreemptiveSFJ")
        ).place(x=475, y=350)

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
            m1 = messagebox.askyesno("Analyzer", "Do you want to run all algorithms first?")
            if m1:
                for alg in simulator.algorithms_list:
                    s = Simulator(alg)
                    s.read_processes_data("data2.csv")
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
        path = 'data2.csv'
        number = 1000
        result = Simulator.generate_processes_data(path, number)
        if result:
            messagebox.showinfo("Info", f"{number} processes generated in {path}")
            # going to next page
            simulator = Simulator("FCFS")
            simulator.read_processes_data(path)
            algo_page(simulator)

    btn_generate = tk.Button(main_window, text='Generate Processes', font=("chiller", 18), height=2, width=20,
                             bg="maroon3", fg="yellow", command=generate_button_command)
    btn_generate.place(x=250, y=250)

    # load button
    def load_button_command():
        path = 'data2.csv'
        simulator = Simulator("FCFS")
        result = simulator.read_processes_data(path)
        if result:
            messagebox.showinfo("Info", f"{simulator.total_process} loaded processes from {path}")
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
