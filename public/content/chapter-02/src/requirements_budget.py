"""Kalkulator System Requirements & Trade-off Edge vs Cloud (Chapter 02).

Membandingkan dua arsitektur untuk studi kasus Sistem Monitoring Suhu Terdistribusi:
1) Raw Cloud Streaming (setiap node mengirim sampel mentah setiap 5 detik)
2) Edge Aggregation (gateway lokal merata-ratakan sampel 5 detik menjadi ringkasan 60 detik)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureScenario:
    name: str
    num_nodes: int
    sample_interval_s: int
    uplink_interval_s: int
    payload_bytes: int
    protocol_overhead_bytes: int
    local_control_latency_ms: float
    cloud_rtt_ms: float
    outage_buffer_hours: int

    def packets_per_day(self) -> float:
        return self.num_nodes * (86400.0 / self.uplink_interval_s)

    def daily_wire_mib(self) -> float:
        total_bytes = self.packets_per_day() * (self.payload_bytes + self.protocol_overhead_bytes)
        return total_bytes / (1024.0 * 1024.0)

    def avg_uplink_kbps(self) -> float:
        bits_per_day = self.packets_per_day() * (self.payload_bytes + self.protocol_overhead_bytes) * 8.0
        return (bits_per_day / 86400.0) / 1000.0

    def outage_buffer_kib(self) -> float:
        packets_during_outage = self.num_nodes * (self.outage_buffer_hours * 3600.0 / self.uplink_interval_s)
        return (packets_during_outage * self.payload_bytes) / 1024.0


def main() -> None:
    scenarios = [
        ArchitectureScenario(
            name="A: Direct-to-Cloud Raw (dt=5s)",
            num_nodes=40,
            sample_interval_s=5,
            uplink_interval_s=5,
            payload_bytes=140,
            protocol_overhead_bytes=64,
            local_control_latency_ms=850.0,
            cloud_rtt_ms=320.0,
            outage_buffer_hours=6,
        ),
        ArchitectureScenario(
            name="B: Edge Gateway Aggregation (dt=60s)",
            num_nodes=40,
            sample_interval_s=5,
            uplink_interval_s=60,
            payload_bytes=220,
            protocol_overhead_bytes=64,
            local_control_latency_ms=25.0,
            cloud_rtt_ms=320.0,
            outage_buffer_hours=6,
        ),
    ]

    print("=== ANALISIS KEBUTUHAN SISTEM: MONITORING SUHU TERDISTRIBUSI (40 NODE) ===")
    for sc in scenarios:
        print(f"\nSkenario: {sc.name}")
        print(f"  Paket uplink / hari      : {sc.packets_per_day():,.0f} paket")
        print(f"  Volume wire / hari       : {sc.daily_wire_mib():.2f} MiB/hari")
        print(f"  Rata-rata bandwidth      : {sc.avg_uplink_kbps():.3f} kbps")
        print(f"  Latensi kendali darurat  : {sc.local_control_latency_ms:.1f} ms")
        print(f"  Kebutuhan buffer {sc.outage_buffer_hours} jam   : {sc.outage_buffer_kib():.1f} KiB")

    raw, edge = scenarios[0], scenarios[1]
    reduction = (1.0 - edge.daily_wire_mib() / raw.daily_wire_mib()) * 100.0
    print("\n--- Perbandingan Trade-off ---")
    print(f"Penghematan volume uplink oleh Edge Aggregation : {reduction:.1f}%")
    print(f"Percepatan respons kendali lokal vs Cloud-loop  : {raw.local_control_latency_ms / edge.local_control_latency_ms:.1f}x")


if __name__ == "__main__":
    main()

