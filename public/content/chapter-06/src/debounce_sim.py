"""Simulasi Software Debouncing & Edge Detection pada Aliran Bounce Sintetis (Chapter 06).

Membandingkan dua algoritma pada dataset telemetry.csv (dua penekanan tombol nyata
yang disertai pantulan mekanik selama 15-20 ms):
1) Naive falling-edge detection (tanpa debounce) -> menghasilkan pemicuan ganda palsu!
2) Time-based software debouncing (DEBOUNCE_MS = 50) + FSM 3-mode (OFF -> ON -> BLINK -> OFF).
"""

from __future__ import annotations

import csv
from pathlib import Path

DEBOUNCE_MS = 50
MODES = ("OFF", "ON", "BLINK")


def main() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        samples = [(int(r["time_ms"]), int(r["raw_gpio"])) for r in csv.DictReader(handle)]

    # 1. Naive falling edge tanpa debounce
    naive_presses = 0
    prev_naive = 1
    for _, raw in samples:
        if prev_naive == 1 and raw == 0:
            naive_presses += 1
        prev_naive = raw

    # 2. Software debounce (stability window 50 ms) + FSM
    last_raw = 1
    stable_state = 1
    last_bounce_ms = 0
    mode_idx = 0
    debounced_events: list[tuple[int, str]] = []

    for now_ms, raw in samples:
        if raw != last_raw:
            last_bounce_ms = now_ms
            last_raw = raw

        if (now_ms - last_bounce_ms) >= DEBOUNCE_MS and raw != stable_state:
            stable_state = raw
            if stable_state == 0:  # Falling edge valid
                mode_idx = (mode_idx + 1) % len(MODES)
                debounced_events.append((now_ms, MODES[mode_idx]))

    print("=== SIMULASI SWITCH BOUNCE & DEBOUNCE FSM (CHAPTER 06) ===")
    print(f"Dataset sintetis: {csv_path.name} ({len(samples)} sampel, 2 tekan fisik ber-bounce)")
    print(f"1) Naive falling-edge (tanpa debounce) : {naive_presses} kali terpicu (SALAH - bounce terhitung!)")
    print(f"2) Software debounce (T_db={DEBOUNCE_MS} ms)      : {len(debounced_events)} kali terpicu (BENAR)")
    for idx, (t_ms, mode) in enumerate(debounced_events, start=1):
        print(f"   [PRESS #{idx}] t={t_ms} ms -> LED Mode = {mode}")


if __name__ == "__main__":
    main()

