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
                execution_history.append([current_process["name"], tact])

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
                execution_history.append([current_process["name"], tact])

                if current_process["sys_info"][1] > 0:
                    high_priority_q.append(current_process) if current_process["sys_info"][1] <= 3 else low_priority_q.append(current_process)
                else:
                    done_processes.append(current_process)

            tact += 1
        awt = mean([i["wt"] for i in done_processes])

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