"""Kalkulator Subnetting IPv4 CIDR, Efisiensi Goodput TCP vs UDP & Analisis Probe (Chapter 11).

Menjalankan:
1. Perhitungan alamat jaringan, broadcast, dan jumlah host usable menggunakan `ipaddress`.
2. Perbandingan efisiensi header TCP+IPv4 (40 B) vs UDP+IPv4 (28 B) untuk payload IoT kecil.
3. Statistik RTT, jitter, dan packet loss dari log probe sintetis `telemetry.csv`.
"""

from __future__ import annotations

import csv
import ipaddress
import statistics
from pathlib import Path


def analyze_cidr(cidr: str) -> None:
    net = ipaddress.IPv4Network(cidr, strict=False)
    hosts = list(net.hosts())
    print(f"Subnet {net.with_prefixlen}:")
    print(f"  Network / Broadcast : {net.network_address} / {net.broadcast_address}")
    print(f"  Netmask             : {net.netmask}")
    print(f"  Rentang Host Usable : {hosts[0]} .. {hosts[-1]} ({len(hosts)} host)")


def compare_goodput(payload_bytes: int, link_overhead_bytes: int = 18) -> None:
    tcp_wire = payload_bytes + 20 + 20 + link_overhead_bytes
    udp_wire = payload_bytes + 8 + 20 + link_overhead_bytes
    print(f"\nEfisiensi Goodput untuk Payload IoT = {payload_bytes} B (Ethernet/MAC overhead={link_overhead_bytes} B):")
    print(f"  TCP/IPv4 (hdr 40 B) : total={tcp_wire} B -> goodput={payload_bytes / tcp_wire * 100:.1f}%")
    print(f"  UDP/IPv4 (hdr 28 B) : total={udp_wire} B -> goodput={payload_bytes / udp_wire * 100:.1f}%")


def analyze_probes() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    total = len(rows)
    lost = sum(1 for r in rows if r["lost"].lower() == "true")
    rtts = [float(r["rtt_ms"]) for r in rows if r["lost"].lower() == "false"]
    mean_rtt = statistics.mean(rtts)
    jitter = statistics.stdev(rtts)

    print(f"\nAnalisis Probe Sintetis ({csv_path.name}, n={total}):")
    print(f"  Paket hilang        : {lost}/{total} ({lost / total * 100:.1f}% packet loss)")
    print(f"  RTT min/avg/max     : {min(rtts):.1f} / {mean_rtt:.2f} / {max(rtts):.1f} ms")
    print(f"  Jitter (std dev)    : {jitter:.2f} ms")


def main() -> None:
    print("=== ANALISIS JARINGAN IoT: CIDR, GOODPUT & PROBE TELEMETRY (CHAPTER 11) ===")
    analyze_cidr("192.168.50.37/26")
    compare_goodput(payload_bytes=48)
    analyze_probes()


if __name__ == "__main__":
    main()

