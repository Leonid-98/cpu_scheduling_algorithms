from numpy import mean


class RR3:
    def __init__(self, processes_queue):
        execution_history, self.awt = self.main(processes_queue)
        self.execution_order = self.convert_history_to_order(execution_history)

    def main(self, processes_queue):
        execution_history = []
        expected_processes = len(processes_queue)
        done_processes = []

        tact = 0
        name = 1
        is_process_were_executed = False

        waiting_queue = []
        

        while len(done_processes) < expected_processes:
            taken_processes = []
            new_arrival_processes = []
            for process in processes_queue:
                if tact >= process[0]:
                    wt = tact - process[0]
                    new_arrival_processes.append({"name": f"P{name}", "sys_info": process, "wt": wt})
                    name += 1
                    taken_processes.append(process)
            processes_queue = [elem for elem in processes_queue if elem not in taken_processes]
            waiting_queue = new_arrival_processes + waiting_queue
            
            
            if waiting_queue:
                current_process = waiting_queue.pop(0)
                is_process_were_executed = True
                execution_time = 0

                if current_process["sys_info"][1] - 3 < 0:
                    execution_time = current_process.get("sys_info")[1]
                    current_process["sys_info"][1] = 0
                else:
                    execution_time = 3
                    current_process["sys_info"][1] -= 3

                for waiting_process in waiting_queue:
                    waiting_process["wt"] += execution_time

                for i in range(execution_time):
                    execution_history.append([current_process["name"], tact + i])

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
    # TODO FIX RR
    class_ = RR3([[1, 10], [2, 2], [2, 3], [4, 1]])
    # class_ = RR3([[1, 6], [1, 4], [1, 3]])
    order = class_.get_execution_order()
    awt = class_.get_awt()
    print(order)
    print(awt)
