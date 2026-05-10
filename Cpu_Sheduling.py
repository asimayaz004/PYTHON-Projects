# CPU Scheduling Simulator in Python

## Overview

This project simulates common CPU scheduling algorithms used in operating systems.

Implemented algorithms:

1. First Come First Serve (FCFS)
2. Shortest Job First (SJF - Non Preemptive)
3. Priority Scheduling (Non Preemptive)
4. Round Robin (RR)

The program calculates:

* Waiting Time
* Turnaround Time
* Completion Time
* Average Waiting Time
* Average Turnaround Time

It also prints a simple Gantt Chart.

---

# Full Python Code

Save this file as:

```text
cpu_scheduler.py
```

```python
from collections import deque


class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

        self.remaining = burst
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def calculate_metrics(processes):
    for p in processes:
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst


def print_results(processes, gantt):
    print("\nGantt Chart:")
    print(" -> ".join(gantt))

    print("\nProcess Table:")
    print(
        f"{'PID':<8}{'Arrival':<10}{'Burst':<10}{'Priority':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}"
    )

    total_wait = 0
    total_turn = 0

    for p in sorted(processes, key=lambda x: x.pid):
        total_wait += p.waiting
        total_turn += p.turnaround

        print(
            f"{p.pid:<8}{p.arrival:<10}{p.burst:<10}{p.priority:<10}{p.completion:<12}{p.turnaround:<12}{p.waiting:<10}"
        )

    n = len(processes)

    print("\nAverage Waiting Time:", round(total_wait / n, 2))
    print("Average Turnaround Time:", round(total_turn / n, 2))


# -------------------------------------------------
# FCFS Scheduling
# -------------------------------------------------

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival)

    current_time = 0
    gantt = []

    for p in processes:
        if current_time < p.arrival:
            current_time = p.arrival

        gantt.append(p.pid)

        current_time += p.burst
        p.completion = current_time

    calculate_metrics(processes)
    print_results(processes, gantt)


# -------------------------------------------------
# SJF Non-Preemptive
# -------------------------------------------------

def sjf(processes):
    n = len(processes)
    completed = 0
    current_time = 0

    visited = [False] * n
    gantt = []

    while completed < n:
        idx = -1
        minimum = float('inf')

        for i in range(n):
            p = processes[i]

            if (
                p.arrival <= current_time
                and not visited[i]
                and p.burst < minimum
            ):
                minimum = p.burst
                idx = i

        if idx != -1:
            p = processes[idx]

            gantt.append(p.pid)
            current_time += p.burst
            p.completion = current_time

            visited[idx] = True
            completed += 1
        else:
            current_time += 1

    calculate_metrics(processes)
    print_results(processes, gantt)


# -------------------------------------------------
# Priority Scheduling Non-Preemptive
# Lower number = higher priority
# -------------------------------------------------

def priority_scheduling(processes):
    n = len(processes)
    completed = 0
    current_time = 0

    visited = [False] * n
    gantt = []

    while completed < n:
        idx = -1
        best_priority = float('inf')

        for i in range(n):
            p = processes[i]

            if (
                p.arrival <= current_time
                and not visited[i]
                and p.priority < best_priority
            ):
                best_priority = p.priority
                idx = i

        if idx != -1:
            p = processes[idx]

            gantt.append(p.pid)
            current_time += p.burst
            p.completion = current_time

            visited[idx] = True
            completed += 1
        else:
            current_time += 1

    calculate_metrics(processes)
    print_results(processes, gantt)


# -------------------------------------------------
# Round Robin Scheduling
# -------------------------------------------------

def round_robin(processes, quantum):
    processes.sort(key=lambda x: x.arrival)

    n = len(processes)
    current_time = 0
    completed = 0
    queue = deque()

    gantt = []
    visited = [False] * n

    while completed < n:

        for i in range(n):
            if (
                processes[i].arrival <= current_time
                and not visited[i]
            ):
                queue.append(processes[i])
                visited[i] = True

        if queue:
            p = queue.popleft()

            gantt.append(p.pid)

            execute = min(quantum, p.remaining)

            current_time += execute
            p.remaining -= execute

            for i in range(n):
                if (
                    processes[i].arrival <= current_time
                    and not visited[i]
                ):
                    queue.append(processes[i])
                    visited[i] = True

            if p.remaining > 0:
                queue.append(p)
            else:
                p.completion = current_time
                completed += 1

        else:
            current_time += 1

    calculate_metrics(processes)
    print_results(processes, gantt)


# -------------------------------------------------
# Input Section
# -------------------------------------------------

def get_processes():
    processes = []

    n = int(input("Enter number of processes: "))

    for i in range(n):
        print(f"\nProcess P{i+1}")

        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))
        priority = int(input("Priority (smaller = higher): "))

        processes.append(Process(f"P{i+1}", arrival, burst, priority))

    return processes


# -------------------------------------------------
# Main Program
# -------------------------------------------------

def main():
    while True:
        print("\n===== CPU Scheduling Simulator =====")
        print("1. FCFS")
        print("2. SJF")
        print("3. Priority Scheduling")
        print("4. Round Robin")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '5':
            print("Exiting...")
            break

        processes = get_processes()

        if choice == '1':
            print("\n--- FCFS Scheduling ---")
            fcfs(processes)

        elif choice == '2':
            print("\n--- SJF Scheduling ---")
            sjf(processes)

        elif choice == '3':
            print("\n--- Priority Scheduling ---")
            priority_scheduling(processes)

        elif choice == '4':
            quantum = int(input("Enter Time Quantum: "))
            print("\n--- Round Robin Scheduling ---")
            round_robin(processes, quantum)

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()
```

---

# Example Input

```text
Enter number of processes: 3

Process P1
Arrival Time: 0
Burst Time: 5
Priority: 2

Process P2
Arrival Time: 1
Burst Time: 3
Priority: 1

Process P3
Arrival Time: 2
Burst Time: 8
Priority: 3
```

---

# How to Run

Install Python 3.

Run:

```bash
python cpu_scheduler.py
```

---

# Features

* Menu-driven interface
* Multiple scheduling algorithms
* Accurate process metrics
* Gantt chart simulation
* Object-oriented design
* Easy to extend

---

# Suggested Future Improvements

* Preemptive SJF
* GUI using Tkinter
* Real-time process visualization
* Export results to CSV
* Multilevel Queue Scheduling
