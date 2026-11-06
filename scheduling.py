import matplotlib.pyplot as plt
import heapq

def fcfs(processes, context_switch):
    processes.sort(key=lambda x: x['arrival_time'])
    time = 0
    gantt_chart = []
    stats = []
    
    for process in processes:
        if time < process['arrival_time']:
            time = process['arrival_time']
        start_time = time
        time += process['burst_time'] + context_switch
        end_time = time - context_switch
        turnaround_time = end_time - process['arrival_time']
        waiting_time = turnaround_time - process['burst_time']
        response_time = start_time - process['arrival_time']
        gantt_chart.append((process['id'], start_time, end_time))
        stats.append({
            'id': process['id'],
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time,
            'response_time': response_time
        })

    return gantt_chart, stats

def sjf(processes, context_switch):
    processes.sort(key=lambda x: x['arrival_time'])
    time = 0
    ready_queue = []
    completed = 0
    n = len(processes)
    gantt_chart = []
    stats = []
    visited = [False] * n

    while completed < n:
        for i in range(n):
            if not visited[i] and processes[i]['arrival_time'] <= time:
                heapq.heappush(ready_queue, (processes[i]['burst_time'], i))
                visited[i] = True
        
        if ready_queue:
            burst_time, i = heapq.heappop(ready_queue)
            start_time = max(time, processes[i]['arrival_time'])
            time = start_time + processes[i]['burst_time'] + context_switch
            end_time = time - context_switch
            turnaround_time = end_time - processes[i]['arrival_time']
            waiting_time = turnaround_time - processes[i]['burst_time']
            response_time = start_time - processes[i]['arrival_time']
            gantt_chart.append((processes[i]['id'], start_time, end_time))
            stats.append({
                'id': processes[i]['id'],
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time,
                'response_time': response_time
            })
            completed += 1
        else:
            time += 1

    return gantt_chart, stats

def round_robin(processes, time_quantum, context_switch):
    processes.sort(key=lambda x: x['arrival_time'])
    queue = []
    time = 0
    gantt_chart = []
    stats = {p['id']: {'turnaround_time': 0, 'waiting_time': 0, 'response_time': -1} for p in processes}
    remaining_burst = {p['id']: p['burst_time'] for p in processes}
    completed = 0
    n = len(processes)
    idx = 0

    while completed < n:
        while idx < n and processes[idx]['arrival_time'] <= time:
            queue.append(processes[idx])
            idx += 1

        if queue:
            current_process = queue.pop(0)
            pid = current_process['id']
            if stats[pid]['response_time'] == -1:
                stats[pid]['response_time'] = time - current_process['arrival_time']

            execution_time = min(time_quantum, remaining_burst[pid])
            start_time = time
            time += execution_time
            remaining_burst[pid] -= execution_time
            gantt_chart.append((pid, start_time, time))

            if remaining_burst[pid] == 0:
                completed += 1
                stats[pid]['turnaround_time'] = time - current_process['arrival_time']
                stats[pid]['waiting_time'] = stats[pid]['turnaround_time'] - current_process['burst_time']
            else:
                while idx < n and processes[idx]['arrival_time'] <= time:
                    queue.append(processes[idx])
                    idx += 1
                queue.append(current_process)
            time += context_switch
        else:
            time += 1

    return gantt_chart, list(stats.values())

def priority_scheduling(processes, context_switch):
    processes.sort(key=lambda x: (x['arrival_time'], x['priority']))
    time = 0
    ready_queue = []
    completed = 0
    n = len(processes)
    gantt_chart = []
    stats = []
    visited = [False] * n

    while completed < n:
        for i in range(n):
            if not visited[i] and processes[i]['arrival_time'] <= time:
                heapq.heappush(ready_queue, (processes[i]['priority'], i))
                visited[i] = True

        if ready_queue:
            _, i = heapq.heappop(ready_queue)
            start_time = max(time, processes[i]['arrival_time'])
            time = start_time + processes[i]['burst_time'] + context_switch
            end_time = time - context_switch
            turnaround_time = end_time - processes[i]['arrival_time']
            waiting_time = turnaround_time - processes[i]['burst_time']
            response_time = start_time - processes[i]['arrival_time']
            gantt_chart.append((processes[i]['id'], start_time, end_time))
            stats.append({
                'id': processes[i]['id'],
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time,
                'response_time': response_time
            })
            completed += 1
        else:
            time += 1

    return gantt_chart, stats

def srtf(processes, context_switch):
    processes.sort(key=lambda x: x['arrival_time'])
    time = 0
    ready_queue = []
    remaining_time = {p['id']: p['burst_time'] for p in processes}
    gantt_chart = []
    stats = {p['id']: {'turnaround_time': 0, 'waiting_time': 0, 'response_time': -1} for p in processes}
    completed = 0
    n = len(processes)
    idx = 0

    while completed < n:
        while idx < n and processes[idx]['arrival_time'] <= time:
            heapq.heappush(ready_queue, (remaining_time[processes[idx]['id']], processes[idx]['id'], idx))
            idx += 1

        if ready_queue:
            remaining, pid, i = heapq.heappop(ready_queue)

            if stats[pid]['response_time'] == -1:
                stats[pid]['response_time'] = time - processes[i]['arrival_time']

            start_time = time
            execution_time = 1
            time += execution_time
            remaining_time[pid] -= execution_time

            if remaining_time[pid] > 0:
                heapq.heappush(ready_queue, (remaining_time[pid], pid, i))
            else:
                completed += 1
                stats[pid]['turnaround_time'] = time - processes[i]['arrival_time']
                stats[pid]['waiting_time'] = stats[pid]['turnaround_time'] - processes[i]['burst_time']

            gantt_chart.append((pid, start_time, time))
        else:
            time += 1

    return gantt_chart, list(stats.values())

def plot_gantt_chart(gantt_chart):
    fig, ax = plt.subplots()
    for process_id, start, end in gantt_chart:
        ax.barh(1, end - start, left=start, edgecolor='black', label=f'P{process_id}')
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart')
    plt.show()

if __name__ == "__main__":
    processes = [
        {'id': 1, 'arrival_time': 0, 'burst_time': 5, 'priority': 2},
        {'id': 2, 'arrival_time': 1, 'burst_time': 3, 'priority': 1},
        {'id': 3, 'arrival_time': 2, 'burst_time': 8, 'priority': 4},
        {'id': 4, 'arrival_time': 3, 'burst_time': 6, 'priority': 3}
    ]
    context_switch = 1

    print("FCFS Scheduling")
    gantt_fcfs, stats_fcfs = fcfs(processes, context_switch)
    for stat in stats_fcfs:
        print(stat)
    plot_gantt_chart(gantt_fcfs)

    print("\nSJF Scheduling")
    gantt_sjf, stats_sjf = sjf(processes, context_switch)
    for stat in stats_sjf:
        print(stat)
    plot_gantt_chart(gantt_sjf)

    print("\nRound Robin Scheduling")
    time_quantum = 4
    gantt_rr, stats_rr = round_robin(processes, time_quantum, context_switch)
    for stat in stats_rr:
        print(stat)
    plot_gantt_chart(gantt_rr)

    print("\nPriority Scheduling")
    gantt_priority, stats_priority = priority_scheduling(processes, context_switch)
    for stat in stats_priority:
        print(stat)
    plot_gantt_chart(gantt_priority)

    print("\nSRTF Scheduling")
    gantt_srtf, stats_srtf = srtf(processes, context_switch)
    for stat in stats_srtf:
        print(stat)
    plot_gantt_chart(gantt_srtf)
