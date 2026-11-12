"""Verifikasi Logika Timing Unsigned 32-bit Rollover & Transisi FSM (Chapter 05).

Menguji dua sifat kritis firmware embedded C/C++:
1) Aritmatika pengurangan unsigned 32-bit ((now - prev) & 0xFFFFFFFF) tetap akurat
   saat millis() melampaui 2^32 - 1 (~49,7 hari).
2) Alur transisi IDLE -> SAMPLE -> ALERT pada ex02_nonblocking_fsm.ino berjalan
   deterministik tanpa pemblokiran.
"""

from __future__ import annotations

MASK_U32 = 0xFFFFFFFF


def u32_elapsed(now_ms: int, prev_ms: int) -> int:
    return (now_ms - prev_ms) & MASK_U32


def main() -> None:
    print("=== SIMULASI ROLLOVER millis() & TRANSISI FSM (CHAPTER 05) ===")

    # 1. Uji rollover batas 32-bit
    prev_ms = 0xFFFFFFF0  # 16 ms sebelum overflow
    now_ms = 0x000003D8   # 984 ms setelah overflow -> total selisih harus 1000 ms
    elapsed = u32_elapsed(now_ms, prev_ms)
    assert elapsed == 1000, f"Gagal rollover: {elapsed}"
    print(f"[PASS] Rollover u32: prev=0x{prev_ms:08X}, now=0x{now_ms:08X} -> elapsed={elapsed} ms")

    # 2. Simulasi transisi FSM 8 detik (step 200 ms)
    state = "IDLE"
    last_sample_ms = 0
    sim_temp = 27.5
    threshold = 30.0
    seq = 0

    for now in range(0, 8200, 200):
        if state == "IDLE":
            if u32_elapsed(now, last_sample_ms) >= 1000:
                last_sample_ms = now
                state = "SAMPLE"
        elif state == "ALERT":
            if u32_elapsed(now, last_sample_ms) >= 1000:
                last_sample_ms = now
                state = "SAMPLE"

        if state == "SAMPLE":
            seq += 1
            sim_temp += 0.9
            if sim_temp > 32.5:
                sim_temp = 27.0
            next_state = "ALERT" if sim_temp >= threshold else "IDLE"
            print(f"t={now:4d} ms | seq={seq} | sim_temp={sim_temp:.1f} C -> next_state={next_state}")
            state = next_state


if __name__ == "__main__":
    main()

