from operator import itemgetter
import numpy as np


def get_processes_from_string(string):
    # abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]]
    return [[int(time) for time in process.split(",")] for process in string.split(";")]


string = "4,2;12,3;13,2;1,10"
processes_queue = sorted(get_processes_from_string(string), key=itemgetter(0))

processes_queue = [[0, 5], [1, 3], [3, 6], [5, 1], [6, 4]]
expected_processes = len(processes_queue)
waiting_queue = []
done_processes = []

tact = 0
name = 1
is_process_were_executed = False

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
        current_process = waiting_queue.pop(0)
        is_process_were_executed = True

        ############################
        execution_time = 0
        if current_process["sys_info"][1] - 3 < 0:
            execution_time = current_process.get("sys_info")[1]
            current_process["sys_info"][1] = 0
            for waiting_process in waiting_queue:
                waiting_process["wt"] += execution_time
        else:
            execution_time = 3
            current_process["sys_info"][1] -= 3
            for waiting_process in waiting_queue:
                waiting_process["wt"] += 3

        print(tact, current_process)
        #############################


        if current_process.get("sys_info")[1] > 0:
            waiting_queue.append(current_process)
        else:
            done_processes.append(current_process)

        is_process_were_executed = True
        tact += execution_time

    if is_process_were_executed:
        is_process_were_executed = False
    else:
        tact += 1

    if tact == 50:
        break

print(np.mean([i["wt"] for i in done_processes]))
