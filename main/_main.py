from tkinter import *
from FCFS import FCFS
from operator import itemgetter
from numpy import mean


class MyGui(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("...")
        master.geometry(f"{1540}x{500}")
        master.resizable(False, False)
        self.font = ("@Microsoft YaHei UI", 12)

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
            0: "#a83232",
            1: "#3aa832",
            2: "#4c96e0",
            3: "#e04c94",
            4: "#cde04c",
            5: "#e04cc5",
        }

    def get_processes_from_string(self, string):
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
        processes_queue = self.get_processes_from_string(self.entry.get())
        fcfs = FCFS(processes_queue)
        execution_order: dict = fcfs.execution_order
        last_tact = max(execution_order, key=lambda x: x["completion"]).get("completion")
        # div = palju pikslit ühes taktis
        div = int(round(1500 / last_tact))
        i = 0
        for process in execution_order:
            self.draw_process_on_canvas(div, process.get("name"), process.get("start"), process.get("completion"), self.colors.get(i))
            i += 1
        awt = mean([x["wt"] for x in execution_order])  # TODO
        print(awt)


if __name__ == "__main__":
    root = Tk()
    my_gui = MyGui(root)
    my_gui.mainloop()
