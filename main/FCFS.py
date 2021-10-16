from numpy import mean


class FCFS:
    def __init__(self, processes_queue):
        execution_history, self.awt = self.main(processes_queue)
        self.execution_order = self.convert_history_to_order(execution_history)

    def main(self, processes_queue):
        execution_history = []
        expected_processes = len(processes_queue)
        done_processes = []

        waiting_queue = []

        tact = 0
        name = 1

        while len(done_processes) < expected_processes:
            # kontrollin, kas sain uued protsessid
            taken_processes = []
            for process in processes_queue:
                if tact >= process[0]:
                    wt = tact - process[0]
                    waiting_queue.append({"name": f"P{name}", "sys_info": process, "wt": wt})
                    name += 1
                    taken_processes.append(process)
            processes_queue = [elem for elem in processes_queue if elem not in taken_processes]

            if waiting_queue:
                # käivitan protsess
                current_process = waiting_queue.pop(0)
                current_process["sys_info"][1] -= 1
                execution_history.append([current_process["name"], tact])
                # kalkuleerin ootamisajad
                for waiting_process in waiting_queue:
                    waiting_process["wt"] += 1
                # panen tagasi
                waiting_queue.insert(0, current_process) if current_process.get("sys_info")[1] > 0 else done_processes.append(current_process)

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
