"""Simulasi Offline Ring Buffer, Full-Jitter Exponential Backoff, SNTP, dan Idempotent Replay."""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass


@dataclass
class TelemetrySample:
    device_id: str
    seq_id: int
    utc_epoch: int
    time_synced: bool
    temp_c: float


class FixedRingBuffer:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._buf: deque[TelemetrySample] = deque()
        self.dropped_oldest = 0

    def push(self, item: TelemetrySample) -> None:
        if len(self._buf) >= self.capacity:
            self._buf.popleft()
            self.dropped_oldest += 1
        self._buf.append(item)

    def peek(self) -> TelemetrySample | None:
        return self._buf[0] if self._buf else None

    def pop_acked(self) -> None:
        if self._buf:
            self._buf.popleft()

    def __len__(self) -> int:
        return len(self._buf)


class IdempotentIngestServer:
    def __init__(self) -> None:
        self.seen_keys: set[tuple[str, int]] = set()
        self.stored: list[TelemetrySample] = []
        self.duplicates_ignored = 0

    def ingest(self, sample: TelemetrySample) -> str:
        key = (sample.device_id, sample.seq_id)
        if key in self.seen_keys:
            self.duplicates_ignored += 1
            return "DUPLICATE_ACK"
        self.seen_keys.add(key)
        self.stored.append(sample)
        return "STORED_ACK"


def full_jitter_backoff_s(attempt: int, base_s: float = 2.0, cap_s: float = 60.0, rng: random.Random | None = None) -> float:
    r = rng or random.Random(42)
    upper = min(cap_s, base_s * (2**attempt))
    return round(r.uniform(0.0, upper), 3)


def main() -> None:
    print("=== CHAPTER 19: RELIABILITY, TIME SYNC & OFFLINE BUFFERING ===")
    rng = random.Random(2026)

    # 1. Perbandingan No-Jitter vs Full-Jitter pada 50 node yang putus bersamaan
    no_jitter = [min(60.0, 2.0 * (2**3)) for _ in range(50)]
    with_jitter = [full_jitter_backoff_s(attempt=3, rng=rng) for _ in range(50)]
    print(f"[JITTER] attempt=3, 50 nodes without jitter -> unique_delays={len(set(no_jitter))} (all at {no_jitter[0]:.1f} s!)")
    print(
        f"[JITTER] attempt=3, 50 nodes full-jitter    -> unique_delays={len(set(with_jitter))}, "
        f"min={min(with_jitter):.2f} s, max={max(with_jitter):.2f} s"
    )

    # 2. Simulasi Ring Buffer kapasitas kecil (4 slot) selama outage 6 sampel (menguji Drop-Oldest)
    ring = FixedRingBuffer(capacity=4)
    server = IdempotentIngestServer()
    base_epoch = 1762819200
    sntp_valid = True

    samples = [
        TelemetrySample("node-01", seq, base_epoch + seq * 10, sntp_valid, round(27.0 + 0.1 * seq, 2))
        for seq in range(1, 10)
    ]

    # T=1..2 online
    for s in samples[:2]:
        ack = server.ingest(s)
        print(f"[LIVE] seq={s.seq_id} epoch={s.utc_epoch} -> {ack}")

    # T=3..8 offline (6 sampel masuk ke ring kapasitas 4 -> 2 paling lama tergeser)
    for s in samples[2:8]:
        ring.push(s)
    print(f"[OFFLINE] pushed 6 items into capacity=4 ring -> buffered={len(ring)}, dropped_oldest={ring.dropped_oldest}")

    # Simulasi replay dengan 1 kasus duplikat (misal PUBACK sempat hilang di percobaan awal)
    ring_head = ring.peek()
    if ring_head is not None:
        first_try = server.ingest(ring_head)
        dup_try = server.ingest(ring_head)
        print(f"[IDEMPOTENCY] replay seq={ring_head.seq_id} try1={first_try}, retry_after_lost_ack={dup_try}")
        ring.pop_acked()

    # Kuras sisa antrean + data T=9
    while len(ring) > 0:
        item = ring.peek()
        assert item is not None
        res = server.ingest(item)
        print(f"[DRAIN] seq={item.seq_id} -> {res}")
        ring.pop_acked()

    res_last = server.ingest(samples[8])
    print(f"[LIVE] seq={samples[8].seq_id} -> {res_last}")
    print(
        f"[SUMMARY] server_stored={len(server.stored)}, duplicates_ignored={server.duplicates_ignored}, "
        f"ring_dropped_oldest={ring.dropped_oldest}"
    )


if __name__ == "__main__":
    main()

