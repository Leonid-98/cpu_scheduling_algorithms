from numpy import mean, right_shift


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

        waiting_queue = []
        for elem in processes_queue:
            waiting_queue.append({"name": f"P{name}", "sys_info": elem, "wt": 0})
            name += 1

        while len(done_processes) < expected_processes:

            if tact >= waiting_queue[0]["sys_info"][0]:
                current_process = waiting_queue.pop(0)
                print(tact, current_process)
                waiting_queue.append(current_process)


            tact += 1
            if tact > 20:
                break

        # awt = round(mean([i["wt"] for i in done_processes]), 2)
        awt = 0

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
