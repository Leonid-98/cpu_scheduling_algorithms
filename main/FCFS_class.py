from operator import itemgetter


class FCFS:
    """
    Iga protsessi täidatakse järjest saabumise kaudu.
    Kõik muutujad klassis on list'id, kus indeks vastab protsessi nimile (ja täitmise järjekorrale)
    Kasutatakse 1 muutja -- self.execution_order:
        list, mis sisaldab iga protsess kujul
        [{"name": f"P{index+1}", "start": start_time, "completion": completion_time, "wt": waiting_time}]
    """

    def __init__(self, processes_queue: list):
        # processes_queue = sorted(self.get_processes_from_string(processes), key=itemgetter(0))  # sorteerin saabumise aja kaudus
        arrival_time = [time[0] for time in processes_queue]
        burst_time = [time[1] for time in processes_queue]
        completion_time = self.set_completion_time(arrival_time, burst_time)
        start_time = self.set_start_time(completion_time, burst_time)
        average_waiting_time = self.set_waiting_time(completion_time, arrival_time, burst_time)

        self.execution_order = self.set_execution_order(start_time, completion_time, average_waiting_time)

    def set_completion_time(self, arrival_time, burst_time):
        completion_time = [_ for _ in range(len(arrival_time))]
        for i in range(len(arrival_time)):
            if i == 0:
                completion_time[i] = arrival_time[i] + burst_time[i]
            else:
                completion_time[i] = completion_time[i - 1] + burst_time[i]
        return completion_time

    def set_start_time(self, completion_time, burst_time):
        start_time = [(completion_time[i] - burst_time[i]) for i in range(len(burst_time))]
        return start_time

    def set_waiting_time(self, completion_time, arrival_time, burst_time):
        waiting_time = [(completion_time[i] - arrival_time[i] - burst_time[i]) for i in range(len(arrival_time))]
        return waiting_time

    def set_execution_order(self, start_time, completion_time, waiting_time):
        order = []
        for index, (start, completion, wt) in enumerate(zip(start_time, completion_time, waiting_time)):
            process = {"name": f"P{index+1}", "start": start, "completion": completion, "wt": wt}
            order.append(process)
        return order


