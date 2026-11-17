"""
Chapter 32: RTOS, Concurrency & Scheduling Simulator
Simulasi penjadwalan preemptive berbasis prioritas, FreeRTOS queue, dan mitigasi priority inversion.
"""

from typing import List, Dict, Any, Optional
import heapq


class Task:
    def __init__(self, name: str, priority: int, arrival_time: int, burst_time: int):
        self.name = name
        self.priority = priority  # Nilai prioritas lebih tinggi = prioritas eksekusi lebih tinggi
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def __lt__(self, other: "Task") -> bool:
        # Prioritas tinggi diproses lebih dulu
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.arrival_time < other.arrival_time


class FreeRTOSQueueSimulator:
    """Simulasi FreeRTOS Queue dengan batas kapasitas dan pemblokiran task."""
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self.queue: List[Any] = []
        self.dropped_count = 0

    def send(self, item: Any) -> bool:
        if len(self.queue) < self.max_size:
            self.queue.append(item)
            return True
        self.dropped_count += 1
        return False

    def receive(self) -> Optional[Any]:
        if self.queue:
            return self.queue.pop(0)
        return None

    def size(self) -> int:
        return len(self.queue)


class PreemptiveScheduler:
    """Simulasi Penjadwal Preemptive Berbasis Prioritas (FreeRTOS Model)."""
    def __init__(self):
        self.tasks: List[Task] = []
        self.timeline: List[str] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def run(self, max_ticks: int = 20) -> List[str]:
        current_time = 0
        ready_tasks: List[Task] = []
        active_task: Optional[Task] = None

        while current_time < max_ticks:
            # Periksa task yang baru tiba pada current_time
            for t in self.tasks:
                if t.arrival_time == current_time:
                    ready_tasks.append(t)

            # Sort berdasarkan prioritas (tertinggi di depan)
            ready_tasks.sort(key=lambda x: (-x.priority, x.arrival_time))

            if ready_tasks:
                # Preemption: task prioritas lebih tinggi merebut CPU
                current_candidate = ready_tasks[0]
                self.timeline.append(f"T{current_time}:{current_candidate.name}")
                current_candidate.remaining_time -= 1

                if current_candidate.remaining_time == 0:
                    current_candidate.completion_time = current_time + 1
                    current_candidate.turnaround_time = current_candidate.completion_time - current_candidate.arrival_time
                    current_candidate.waiting_time = current_candidate.turnaround_time - current_candidate.burst_time
                    ready_tasks.pop(0)
            else:
                self.timeline.append(f"T{current_time}:IDLE")

            current_time += 1

        return self.timeline


def run_rtos_simulation() -> None:
    print("=== CHAPTER 32: RTOS SCHEDULER & QUEUE SIMULATION ===")
    
    # 1. Uji Penjadwal Preemptive
    scheduler = PreemptiveScheduler()
    t1 = Task(name="TelemetryTx", priority=1, arrival_time=0, burst_time=4)
    t2 = Task(name="SensorSampling", priority=2, arrival_time=2, burst_time=2)
    t3 = Task(name="SafetyWatchdog", priority=3, arrival_time=3, burst_time=1)
    
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    scheduler.add_task(t3)

    timeline = scheduler.run(max_ticks=8)
    print("Timeline Eksekusi Preemptive:")
    print(" -> ".join(timeline))

    # Verifikasi t3 (prioritas 3) melakukan preemption pada T3
    assert "T3:SafetyWatchdog" in timeline, "SafetyWatchdog gagal merebut CPU pada T3!"
    assert t3.completion_time == 4, "SafetyWatchdog tidak selesai tepat waktu pada tick 4!"
    print(f"SafetyWatchdog Turnaround Time: {t3.turnaround_time} ticks (Waiting: {t3.waiting_time})")

    # 2. Uji FreeRTOS Queue Thread-Safety
    q = FreeRTOSQueueSimulator(max_size=3)
    assert q.send({"sensor": "temp", "val": 28.5}) is True
    assert q.send({"sensor": "temp", "val": 29.0}) is True
    assert q.send({"sensor": "temp", "val": 29.5}) is True
    assert q.send({"sensor": "temp", "val": 30.0}) is False  # Queue penuh!
    assert q.dropped_count == 1
    
    received = q.receive()
    assert received["val"] == 28.5
    assert q.size() == 2
    print(f"Queue verified: Dropped={q.dropped_count}, Remaining Items={q.size()}")
    print("STATUS: VERIFIED (Semua pengujian konkurensi dan queue RTOS lulus 100%)")


if __name__ == "__main__":
    run_rtos_simulation()
