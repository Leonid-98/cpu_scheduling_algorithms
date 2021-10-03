from operator import itemgetter
import numpy as np


def get_processes_from_string(string):
    # abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]]
    return [[int(time) for time in process.split(",")] for process in string.split(";")]


string = "1,10;3,3;4,1;8,6;15,2"
processes_queue = sorted(get_processes_from_string(string), key=itemgetter(0))
expected_processes = len(processes_queue)
waiting_queue = []
done_processes = []

tact = 0
name = 1

while len(done_processes) < expected_processes:
    iterations = range(len(processes_queue))
    for i in iterations:
        try:
            if tact >= processes_queue[i][0]:
                wt = tact - processes_queue[i][0]
                waiting_queue.insert(0, {"name": f"P{name}", "sys_info": processes_queue.pop(i), "wt": wt})
                name += 1
        except IndexError:
            pass
        
    if waiting_queue:
        waiting_queue = sorted(waiting_queue, key=lambda dict: dict["sys_info"][0])
        current_process = waiting_queue.pop(0)
        for waiting_process in waiting_queue:
            waiting_process["wt"] += 1
        
        current_process["sys_info"][1] -= 1
        print(tact, current_process)

        if current_process["sys_info"][1] > 0:
            waiting_queue.append(current_process)
        else:
            done_processes.append(current_process)

    tact += 1


print(np.mean([i["wt"] for i in done_processes]))
