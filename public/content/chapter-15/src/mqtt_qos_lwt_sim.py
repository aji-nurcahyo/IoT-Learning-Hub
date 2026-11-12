"""Simulasi MQTT QoS 0/1/2, Deduplikasi, Retained Message, Session & Last Will (Chapter 15).

Memodelkan perilaku protokol MQTT secara deterministik:
1. Perbandingan jumlah paket per-hop: QoS 0 (1 pkt), QoS 1 (2 pkt), QoS 2 (4 pkt).
2. Simulasi hilangnya PUBACK pada QoS 1 -> pengiriman ulang (DUP=1) -> ditangani
   oleh mekanisme deduplikasi `seq` di sisi Subscriber.
3. Simulasi Retained Message -> subscriber yang baru bergabung belakangan tetap
   langsung menerima status terakhir (`{"state": "online"}`).
4. Simulasi putus mendadak -> keepalive 1.5x habis -> Broker memicu LWT (`"offline"`).
"""

from __future__ import annotations


def main() -> None:
    print("=== SIMULASI MQTT QoS, SESSIONS, RETAINED & LWT (CHAPTER 15) ===")

    # 1. Overhead paket per pesan
    for qos, pkts in [(0, ["PUBLISH"]), (1, ["PUBLISH", "PUBACK"]), (2, ["PUBLISH", "PUBREC", "PUBREL", "PUBCOMP"])]:
        print(f"QoS {qos}: {len(pkts)} paket/pesan -> {' -> '.join(pkts)}")

    # 2. QoS 1 duplicate delivery & idempotent receiver
    print("\n--- Uji Duplikasi QoS 1 (PUBACK hilang di jaringan) ---")
    seen_seqs: set[int] = set()
    incoming_stream = [
        {"seq": 10, "dup": False, "temp_c": 29.1},
        {"seq": 11, "dup": False, "temp_c": 29.3},
        {"seq": 11, "dup": True, "temp_c": 29.3},   # Broker/client retry karena PUBACK hilang
        {"seq": 12, "dup": False, "temp_c": 29.4},
    ]
    accepted = 0
    deduped = 0
    for pkt in incoming_stream:
        if pkt["seq"] in seen_seqs:
            deduped += 1
            print(f"  [DEDUP DROP] seq={pkt['seq']} dup={pkt['dup']} sudah pernah diproses!")
        else:
            seen_seqs.add(pkt["seq"])
            accepted += 1
            print(f"  [DB INSERT ] seq={pkt['seq']} dup={pkt['dup']} temp_c={pkt['temp_c']} C")
    assert accepted == 3 and deduped == 1

    # 3. Retained & LWT lifecycle
    print("\n--- Uji Retained Message, Keepalive & LWT ---")
    retained_store: dict[str, str] = {}
    lwt_registry: dict[str, tuple[str, str, bool]] = {}

    # Device connect membawa LWT + publish online retained
    lwt_registry["node-01"] = ("lab/gh01/node-01/status", '{"state":"offline","reason":"lwt"}', True)
    retained_store["lab/gh01/node-01/status"] = '{"state":"online"}'
    print(f"1) Node konek -> retained['status'] = {retained_store['lab/gh01/node-01/status']}")

    # Dashboard bergabung 2 menit kemudian
    print(f"2) Dashboard baru subscribe -> langsung terima retained: {retained_store['lab/gh01/node-01/status']}")

    # Node mati mendadak (kabel USB dicabut tanpa DISCONNECT) -> 1.5 * 30s = 45s lewat
    keepalive_s = 30
    silent_s = 46
    if silent_s > 1.5 * keepalive_s:
        topic, lwt_msg, retain = lwt_registry.pop("node-01")
        if retain:
            retained_store[topic] = lwt_msg
        print(f"3) Diam {silent_s}s (> {1.5 * keepalive_s:.0f}s) -> Broker picu LWT: {topic} = {lwt_msg}")


if __name__ == "__main__":
    main()

