# CPU Scheduling Algorithms
## Simple graphical implementation of four processor scheduling algorithms using `Python` and `Tkinter` module.

**1. First Come First Serve** </br>
Processes are executed in order of arrival without interruption. </br>
Waiting queue checked when executed process is done. </br>
<img src="/images/fcfs.png" width=85% height="auto"/> </br>
</br>
**2. First Come First Serve with two-level priority** </br>
If burst time <= 3, process goes into high priority queue. Else into low priority queue. </br>
If there's no high priority processes, execute low priority processes. </br>
if process coming to the high priority queue, low priority process is interputed. </br>
Waiting queues checked every tact. </br>
<img src="/images/fcfs2x.png" width=85% height="auto"/></br>
</br>
**3. Round-Robin Scheduling with time quantum 3** </br>
Always execute new incoming processes at any time before the old processes have accumulated in the queue.</br>
Time slices (time quantum) are assigned to each process in equal portions and in circular order, handling all processes without priority. </br>
Waiting queue checked every time quantum or if executed process is done. </br>
<img src="/images/rr3.png" width=85% height="auto"/></br>
</br>
**4. Shortest Remaining Time First** </br>
If a process with a lower burst time arrives (or in waiting queue), the current one is interputed.</br>
If a process with a same burst time arrives (or in waiting queue), the current one is prefered.</br>
Priorities check every tact. </br>
<img src="/images/srtf.png" width=85% height="auto"/></br>
</br>
