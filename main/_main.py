from operator import itemgetter
from tkinter import *

from FCFS import FCFS
from FCFS2x import FCFS2x
from RR3 import RR3
from SRTF import SRTF


class MyGui(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("...")
        master.geometry(f"{1540}x{500}")
        master.resizable(False, False)
        self.font = ("Bahnschrift SemiBold", 12)

        self.outercanvas = Canvas(master, bg="#e1e8f4", width=1540, height=500)
        self.outercanvas.pack()
        self.innercanvas = Canvas(self.outercanvas, width=1500, height=101, bg="#424242", highlightthickness=0)
        self.outercanvas.create_window(20, 20, anchor=NW, window=self.innercanvas)

        run_btn = Button(self.outercanvas, text="Run", font=self.font, command=lambda: self.draw_using_fcfs())
        self.outercanvas.create_window(20, 140, anchor=NW, height=30, width=80, window=run_btn)

        clear_btn = Button(self.outercanvas, text="Clear", font=self.font, command=lambda: self.innercanvas.delete("all"))
        self.outercanvas.create_window(160, 140, anchor=NW, height=30, width=80, window=clear_btn)

        self.entry = Entry(self.outercanvas, font=self.font)
        self.entry.insert(END, "1,10;3,3;4,1;8,6;15,2")
        self.outercanvas.create_window(20, 180, anchor=NW, height=30, width=220, window=self.entry)

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

    def convert_string_to_process_queue(self, string):
        # abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]] ning kohe sorrteerib saabumise aja kaudu
        return sorted([[int(time) for time in process.split(",")] for process in string.split(";")], key=itemgetter(0))

    def draw_process_on_canvas(self, div, process_name, start_time, completion_time, color):
        x1 = div * start_time
        x2 = div * completion_time
        self.innercanvas.create_rectangle(x1 - 1, -1, x2, 101, fill=color, width=0)
        self.innercanvas.create_text((x1 + x2) / 2, 50, text=process_name, font=self.font)
        self.innercanvas.create_text(x1 + 15, 90, text=start_time, font=self.font)
        self.innercanvas.create_text(x2 - 15, 90, text=completion_time, font=self.font)

    def draw_using_fcfs(self):
        self.innercanvas.delete("all")
        processes_queue = self.convert_string_to_process_queue(self.entry.get())
        fcfs2x = SRTF(processes_queue)
        execution_order = fcfs2x.get_execution_order()
        awt = fcfs2x.get_awt()
        last_tact = execution_order[-1][-1][-1]
        # div = palju pikslit ühes taktis
        div = int(round(1500 / last_tact))
        for process in execution_order:
            name = process[0]
            start = process[1][0]
            stop = process[1][1]
            self.draw_process_on_canvas(div, name, start, stop, self.colors.get(name))


if __name__ == "__main__":
    root = Tk()
    my_gui = MyGui(root)
    my_gui.mainloop()
