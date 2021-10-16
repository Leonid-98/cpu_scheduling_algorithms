from numpy import mean


class FCFS2x:
    def __init__(self, processes_queue):
        execution_history, self.awt = self.main(processes_queue)
        self.execution_order = self.convert_history_to_order(execution_history)

    def main(self, processes_queue):
        execution_history = []
        expected_processes = len(processes_queue)
        done_processes = []

        low_priority_q = []
        high_priority_q = []

        tact = 0
        name = 1

        while len(done_processes) < expected_processes:
            # iterations = range(len(processes_queue))
            # for i in iterations:
            #     try:
            #         if tact >= processes_queue[i][0]:
            #             wt = tact - processes_queue[i][0]
            #             if processes_queue[i][1] <= 3:
            #                 high_priority_q.append({"name": f"P{name}", "sys_info": processes_queue.pop(i), "wt": wt})
            #             else:
            #                 low_priority_q.append({"name": f"P{name}", "sys_info": processes_queue.pop(i), "wt": wt})
            #             name += 1
            #     except IndexError:
            #         pass

            taken_processes = []
            for process in processes_queue:
                if tact >= process[0]:
                    wt = tact - process[0]
                    if process[1] <= 3:
                        high_priority_q.append({"name": f"P{name}", "sys_info": process, "wt": wt})
                    else:
                        low_priority_q.append({"name": f"P{name}", "sys_info": process, "wt": wt})
                    name += 1
                    taken_processes.append(process)
            processes_queue = [elem for elem in processes_queue if elem not in taken_processes]

            if high_priority_q:
                current_process = high_priority_q.pop(0)
                for waiting_process in high_priority_q:
                    waiting_process["wt"] += 1
                if low_priority_q:
                    for waiting_process in low_priority_q:
                        waiting_process["wt"] += 1

                current_process["sys_info"][1] -= 1
                execution_history.append([current_process["name"], tact])

                if current_process["sys_info"][1] > 0:
                    high_priority_q.insert(0, current_process)
                else:
                    done_processes.append(current_process)

            elif low_priority_q:
                current_process = low_priority_q.pop(0)
                for waiting_process in low_priority_q:
                    waiting_process["wt"] += 1

                current_process["sys_info"][1] -= 1
                execution_history.append([current_process["name"], tact])

                if current_process["sys_info"][1] > 0:
                    if current_process["sys_info"][1] <= 3:
                        high_priority_q.insert(0, current_process)
                    else:
                        low_priority_q.insert(0, current_process)
                else:
                    done_processes.append(current_process)

            tact += 1
        awt = round(mean([i["wt"] for i in done_processes]), 2)

        return execution_history, awt

    def convert_history_to_order(self, execution_history):
        prev_elem = None
        execution_order = []
        for i in range(len(execution_history)):
            name = execution_history[i][0]
            tact = execution_history[i][1]
            if prev_elem != name:
                execution_order.append([name, [tact, tact + 1]])
            else:
                execution_order[-1][1][1] += 1
            prev_elem = name

        return execution_order

    def get_awt(self):
        return self.awt

    def get_execution_order(self):
        return self.execution_order


if __name__ == "__main__":
    fcfs2x = FCFS2x([[1, 10], [3, 3], [4, 1], [8, 6], [15, 2]])
    order = fcfs2x.get_execution_order()
    awt = fcfs2x.get_awt()
    print(order)
    print(awt)
