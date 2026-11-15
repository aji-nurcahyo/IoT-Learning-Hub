#!/usr/bin/env python3
"""
Edge Processing & Local Automation Rule Engine
Chapter 23 — Internet of Things Learning Hub

Menyediakan pemfilteran outlier (IQR/Deadband), agregasi jendela waktu (Sliding Window),
mesin aturan aktuasi lokal dengan histeresis, serta sinkronisasi spool buffer ke cloud.
"""

import time
import math
from typing import List, Dict, Any, Optional


# 1. Pemfilteran Outlier Berbasis Rentang Interkuartil (IQR)
def filter_outliers_iqr(values: List[float], multiplier: float = 1.5) -> List[float]:
    """Menyaring nilai ekstrem yang menyimpang di luar Q1 - k*IQR dan Q3 + k*IQR."""
    if len(values) < 4:
        return values
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    q1 = sorted_vals[n // 4]
    q3 = sorted_vals[(3 * n) // 4]
    iqr = q3 - q1
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    return [v for v in values if lower_bound <= v <= upper_bound]


# 2. Pemfilteran Deadband (Meredam fluktuasi derau kecil)
class DeadbandFilter:
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.last_value: Optional[float] = None

    def should_publish(self, current_value: float) -> bool:
        if self.last_value is None:
            self.last_value = current_value
            return True
        if abs(current_value - self.last_value) >= self.threshold:
            self.last_value = current_value
            return True
        return False


# 3. Agregator Jendela Waktu Geser (Sliding Window)
class SlidingWindowAggregator:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.buffer: List[float] = []

    def add_sample(self, val: float) -> Optional[Dict[str, float]]:
        self.buffer.append(val)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)

        if len(self.buffer) == self.window_size:
            clean = filter_outliers_iqr(self.buffer)
            mean_val = sum(clean) / len(clean)
            variance = sum((x - mean_val) ** 2 for x in clean) / len(clean)
            return {
                "count": len(clean),
                "mean": round(mean_val, 2),
                "min": round(min(clean), 2),
                "max": round(max(clean), 2),
                "std_dev": round(math.sqrt(variance), 2)
            }
        return None


# 4. Mesin Aturan Otomasi Lokal dengan Kontrol Histeresis
class LocalAutomationEngine:
    def __init__(self, high_threshold: float = 30.0, hysteresis: float = 1.5):
        self.high_threshold = high_threshold
        self.hysteresis = hysteresis
        self.relay_state = False  # False = OFF, True = ON (Cooling fan)
        self.transitions = 0

    def evaluate(self, current_temp: float) -> Dict[str, Any]:
        """
        Logika histeresis:
        - Hidupkan pendingin jika temp >= high_threshold (misal: 30.0 C)
        - Matikan pendingin HANYA jika temp < high_threshold - hysteresis (misal: 28.5 C)
        """
        initial_state = self.relay_state
        if not self.relay_state and current_temp >= self.high_threshold:
            self.relay_state = True
            self.transitions += 1
            action = "RELAY_TURNED_ON"
        elif self.relay_state and current_temp < (self.high_threshold - self.hysteresis):
            self.relay_state = False
            self.transitions += 1
            action = "RELAY_TURNED_OFF"
        else:
            action = "NO_CHANGE"

        return {
            "current_temp": current_temp,
            "relay_active": self.relay_state,
            "action": action,
            "state_changed": (initial_state != self.relay_state)
        }


# 5. Buffer Spooling Sinkronisasi Edge-Cloud
class EdgeSpoolBuffer:
    def __init__(self, max_capacity: int = 50):
        self.max_capacity = max_capacity
        self.queue: List[Dict[str, Any]] = []

    def push(self, record: Dict[str, Any]):
        if len(self.queue) >= self.max_capacity:
            self.queue.pop(0)  # Drop-oldest saat buffer penuh
        self.queue.append(record)

    def drain(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        batch = self.queue[:batch_size]
        self.queue = self.queue[batch_size:]
        return batch

    def pending_count(self) -> int:
        return len(self.queue)


def main():
    print("=== Edge Processing & Local Automation Verification Suite ===")

    # Test 1: Pemfilteran Outlier IQR
    raw_readings = [26.1, 26.3, 26.2, 99.9, 26.4, 26.2, -45.0, 26.5]
    filtered = filter_outliers_iqr(raw_readings)
    print(f"Test 1 - IQR Filter: Dari {len(raw_readings)} sampel mentah -> {len(filtered)} sampel bersih.")
    print(f"   Raw: {raw_readings}")
    print(f"   Cleaned: {filtered}")
    assert 99.9 not in filtered and -45.0 not in filtered, "Outlier harus dieliminasi!"

    # Test 2: Deadband Filtering
    deadband = DeadbandFilter(threshold=0.5)
    sequence = [25.0, 25.1, 25.2, 25.6, 25.7, 26.3]
    published = [val for val in sequence if deadband.should_publish(val)]
    print(f"\nTest 2 - Deadband Filter (threshold 0.5 C):")
    print(f"   Input stream : {sequence}")
    print(f"   Published    : {published} (Meredam {len(sequence) - len(published)} fluktuasi kecil)")

    # Test 3: Sliding Window Aggregator
    aggregator = SlidingWindowAggregator(window_size=5)
    stats_result = None
    stream_samples = [25.0, 25.5, 26.0, 25.8, 26.2, 26.5]
    for s in stream_samples:
        stats_result = aggregator.add_sample(s)
    print(f"\nTest 3 - Sliding Window Aggregation (5 samples):")
    print(f"   Metrik agregat: {stats_result}")

    # Test 4: Local Automation Rule Engine dengan Histeresis
    print(f"\nTest 4 - Hysteresis Control (High: 30.0 C, Hysteresis: 1.5 C):")
    engine = LocalAutomationEngine(high_threshold=30.0, hysteresis=1.5)
    temp_profile = [28.0, 29.8, 30.2, 29.9, 29.0, 28.6, 28.4, 28.0]
    for temp in temp_profile:
        res = engine.evaluate(temp)
        print(f"   Temp: {temp:4.1f} C | Relay: {'ON ' if res['relay_active'] else 'OFF'} | Action: {res['action']}")

    assert engine.transitions == 2, f"Harus tepat 2 transisi on/off, tercatat {engine.transitions}"

    # Test 5: Edge Spooling Buffer
    print(f"\nTest 5 - Edge Spooling & Cloud Sync:")
    spool = EdgeSpoolBuffer(max_capacity=10)
    for i in range(12):
        spool.push({"id": i, "temp": 25.0 + i, "ts": 1762822800 + i})
    print(f"   Total buffer setelah 12 push (kapasitas 10): {spool.pending_count()} entri")
    batch_drained = spool.drain(batch_size=5)
    print(f"   Drain batch 1 (5 entri): id {batch_drained[0]['id']} hingga {batch_drained[-1]['id']}")
    print(f"   Sisa buffer dalam antrean: {spool.pending_count()} entri")

    print("\nAll edge processing test cases passed successfully.")


if __name__ == "__main__":
    main()
