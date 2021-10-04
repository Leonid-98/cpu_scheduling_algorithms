from operator import itemgetter
import numpy as np


def get_processes_from_string(string):
    # abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]]
    return [[int(time) for time in process.split(",")] for process in string.split(";")]


string = "1,10;3,3;4,1;8,6;15,2"
processes_queue = sorted(get_processes_from_string(string), key=itemgetter(0))

expected_processes = len(processes_queue)
low_priority_q = []
high_priority_q = []
done_processes = []

tact = 0
name = 1

execution_order = []

while len(done_processes) < expected_processes:
    iterations = range(len(processes_queue))
    for i in iterations:
        try:
            if tact == processes_queue[i][0]:
                if processes_queue[i][1] <= 3:
                    high_priority_q.append({"name": f"P{name}", "sys_info": processes_queue.pop(i), "wt": 0})
                else:
                    low_priority_q.append({"name": f"P{name}", "sys_info": processes_queue.pop(i), "wt": 0})
                name += 1
        except IndexError:
            pass

    if high_priority_q:
        high_priority_q = sorted(high_priority_q, key=lambda dict: dict["sys_info"][0])
        current_process = high_priority_q.pop(0)
        for waiting_process in high_priority_q:
            waiting_process["wt"] += 1
        if low_priority_q:
            for waiting_process in low_priority_q:
                waiting_process["wt"] += 1

        current_process["sys_info"][1] -= 1
        execution_order.append([current_process["name"], tact])

        if current_process["sys_info"][1] > 0:
            high_priority_q.append(current_process)
        else:
            done_processes.append(current_process)

    elif low_priority_q:
        low_priority_q = sorted(low_priority_q, key=lambda dict: dict["sys_info"][0])
        current_process = low_priority_q.pop(0)
        for waiting_process in low_priority_q:
            waiting_process["wt"] += 1

        current_process["sys_info"][1] -= 1
        execution_order.append([current_process["name"], tact])

        if current_process["sys_info"][1] > 0:
            high_priority_q.append(current_process) if current_process["sys_info"][1] <= 3 else low_priority_q.append(current_process)
        else:
            done_processes.append(current_process)

    tact += 1

print(execution_order)
print(np.mean([i["wt"] for i in done_processes]))
