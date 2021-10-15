import itertools
from operator import index, itemgetter
from tkinter import *
from PIL import ImageTk

from FCFS import FCFS
from FCFS2x import FCFS2x
from RR3 import RR3
from SRTF import SRTF


class MyGui(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.width = 1000
        master.title("Protsessoriaja haldus")
        master.geometry(f"{self.width + 40}x{350}")
        master.resizable(False, False)
        self.font = ("Bahnschrift SemiBold", 12)
        self.colors = {
            "P1": "#0CF799",
            "P2": "#4B43EB",
            "P3": "#EB008E",
            "P4": "#D4750B",
            "P5": "#D8F50F",
            "P6": "#0CF716",
            "P7": "#0B86D4",
            "P8": "#A000EB",
            "P9": "#D43C0B",
            "P10": "#F5D00F",
            "P11": "#33D4AC",
            "P12": "#D43366",
        }
        defaults_for_option_menu = [
            "Enda oma üleval",
            "0,7;1,5;2,3;3,1;4,2;5,1",
            "0,2;1,4;12,4;15,5;21,10",
            "0,4;1,5;2,2;3,1;4,6;6,3",
        ]
        self.option_menu_choise = defaults_for_option_menu[0]

        self.outercanvas = Canvas(master, bg="#dbf7ff", width=self.width + 40, height=350)
        self.outercanvas.pack()

        self.innercanvas = Canvas(self.outercanvas, width=self.width, height=101, bg="#7b9ba4", highlightthickness=0)
        self.outercanvas.create_window(20, 20, anchor=NW, window=self.innercanvas)

        fcfs_btn = Button(self.outercanvas, text="FCFS", font=self.font, command=lambda: self.calculate_schedue_and_draw("fcfs"))
        self.outercanvas.create_window(20, 140, anchor=NW, height=30, width=80, window=fcfs_btn)

        fcfs2x_btn = Button(self.outercanvas, text="FCFS2X", font=self.font, command=lambda: self.calculate_schedue_and_draw("fcfs2x"))
        self.outercanvas.create_window(120, 140, anchor=NW, height=30, width=80, window=fcfs2x_btn)

        rr3_btn = Button(self.outercanvas, text="RR3", font=self.font, command=lambda: self.calculate_schedue_and_draw("rr3"))
        self.outercanvas.create_window(220, 140, anchor=NW, height=30, width=80, window=rr3_btn)

        srtf_btn = Button(self.outercanvas, text="SRTF", font=self.font, command=lambda: self.calculate_schedue_and_draw("srtf"))
        self.outercanvas.create_window(320, 140, anchor=NW, height=30, width=80, window=srtf_btn)

        clear_btn = Button(self.outercanvas, text="Reset", font=self.font, command=lambda: self.reset_inner_canvas())
        self.outercanvas.create_window(420, 140, anchor=NW, height=30, width=80, window=clear_btn)

        self.awt_label = Label(self.outercanvas, text="Keskmine ootamis aeg: --", font=self.font, bg="#dbf7ff")
        self.outercanvas.create_window(250, 180, anchor=NW, height=30, width=210, window=self.awt_label)

        self.entry = Entry(self.outercanvas, font=self.font, state=NORMAL)
        self.entry.insert(END, "1,10;3,3;4,1;8,6;15,2")
        self.outercanvas.create_window(20, 180, anchor=NW, height=30, width=220, window=self.entry)

        self.option_menu_var = StringVar()
        self.option_menu_var.set(defaults_for_option_menu[0])
        self.option_menu = OptionMenu(
            self.outercanvas, self.option_menu_var, *defaults_for_option_menu, command=lambda event_choice: self.check_option_menu_choise(event_choice)
        )
        self.option_menu.config(font=self.font)
        menu = master.nametowidget(self.option_menu.menuname)
        menu.config(font=self.font)
        self.outercanvas.create_window(20, 220, anchor=NW, height=30, width=220, window=self.option_menu)

        self.name_label = Label(self.outercanvas, text="Operatsioonisüsteemid (LTAT.06.001)\nLeonid Tšigrinski 2021", font=self.font, bg="#dbf7ff")
        self.outercanvas.create_window(630, 140, anchor=NW, height=50, width=300, window=self.name_label)

    def convert_string_to_process_queue(self, string):
        """abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]] ning kohe sorrteerib saabumise aja kaudu"""
        return sorted([[int(time) for time in process.split(",")] for process in string.split(";")], key=itemgetter(0))

    def reset_inner_canvas(self):
        """event funktsion, puhastab sisemine canvas"""
        self.innercanvas.delete("all")
        self.awt_label["text"] = "Keskmine ootamis aeg: --"
        self.entry.delete(0, END)
        self.entry.insert(END, "1,10;3,3;4,1;8,6;15,2")

    def check_option_menu_choise(self, event_choice):
        """event funktsion option menu jaoks"""
        self.option_menu_choise = event_choice
        if event_choice == "Enda oma üleval":
            self.entry.config(state=NORMAL)
        else:
            self.entry.config(state=DISABLED)

    def calculate_schedue_and_draw(self, algorithm: str):
        """event põhifunktsioon arvutamise jaoks"""
        self.innercanvas.delete("all")

        processes_queue = None
        if self.option_menu_choise == "Enda oma üleval":
            processes_queue = self.convert_string_to_process_queue(self.entry.get())
        else:
            processes_queue = self.convert_string_to_process_queue(self.option_menu_choise)

        algorithm_class = None
        if algorithm == "fcfs":
            algorithm_class = FCFS(processes_queue)
        elif algorithm == "fcfs2x":
            algorithm_class = FCFS2x(processes_queue)
        elif algorithm == "rr3":
            algorithm_class = RR3(processes_queue)
        elif algorithm == "srtf":
            algorithm_class = SRTF(processes_queue)

        execution_order = algorithm_class.get_execution_order()
        self.draw_process_on_canvas(execution_order)

        awt = algorithm_class.get_awt()
        self.awt_label["text"] = "Keskmine ootamis aeg: " + str(awt)

    def draw_process_on_canvas(self, execution_order):
        """abifunktsioon calculate_schedue_and_draw(algorithm) jaoks, joonistab protsessid ja taktid"""
        last_tact = execution_order[-1][-1][-1]
        # palju pikslit ühes taktis
        div = int(round(self.width / last_tact))
        # [P1, [2,6]], [P2, [6, 8] --> [2, 6], [6, 8] --> {2, 6, 8} --> [2, 6, 8]
        critical_tacts = list(set(itertools.chain.from_iterable([process[1] for process in execution_order])))
        # joonista riskülikud (protsessid)
        for process in execution_order:
            name = process[0]
            start = process[1][0]
            stop = process[1][1]

            x1 = div * start
            x2 = div * stop
            self.innercanvas.create_rectangle(x1 - 1, -1, x2, 101, fill=self.colors.get(name), width=0)
            self.innercanvas.create_text((x1 + x2) / 2, 50, text=name, font=self.font)
        # joonista vajalikud taktid
        self.innercanvas.create_text(div * critical_tacts[0] + 10, 90, text=critical_tacts[0], font=self.font)
        for tact in critical_tacts[1:-1]:
            self.innercanvas.create_text(div * tact - 1, 90, text=tact, font=self.font)
        self.innercanvas.create_text(div * critical_tacts[-1] - 11, 90, text=critical_tacts[-1], font=self.font)


if __name__ == "__main__":
    root = Tk()
    my_gui = MyGui(root)
    my_gui.mainloop()
