"""
Modul Simulasi Arsitektur Purdue Model & OT/IT DMZ Gateway Policy Engine.
Mendemonstrasikan penegakan kebijakan keamanan zona, inspeksi paket industri,
dan isolasi komunikasi Level 0-2 dari Level 4 Enterprise.

Author: Aji Pamungkas Tri Nurcahyo (ITERA)
Track: Track B - Industrial IoT & Predictive Maintenance (B01)
"""

from typing import Dict, Any, List, Tuple
import json

class PurdueZone:
    LEVEL_0_FIELD = 0       # Sensor & Actuator fisik
    LEVEL_1_CONTROL = 1     # PLC, RTU, I/O Controller
    LEVEL_2_SUPERVISORY = 2 # HMI, SCADA Local Operator
    LEVEL_3_OPERATIONS = 3  # Manufacturing Execution System (MES), Plant Historian
    IDMZ = 3.5              # Industrial Demilitarized Zone (Proxies, Replicated Historian)
    LEVEL_4_ENTERPRISE = 4  # ERP, Corporate Network, Business Analytics

class IndustrialSecurityGateway:
    def __init__(self):
        # Tabel aturan aliran data yang diizinkan (Zone & Conduit Model IEC 62443)
        self.allowed_conduits = {
            # Dari zona asal -> daftar zona tujuan yang legal
            PurdueZone.LEVEL_0_FIELD: [PurdueZone.LEVEL_1_CONTROL],
            PurdueZone.LEVEL_1_CONTROL: [PurdueZone.LEVEL_0_FIELD, PurdueZone.LEVEL_2_SUPERVISORY],
            PurdueZone.LEVEL_2_SUPERVISORY: [PurdueZone.LEVEL_1_CONTROL, PurdueZone.LEVEL_3_OPERATIONS],
            PurdueZone.LEVEL_3_OPERATIONS: [PurdueZone.LEVEL_2_SUPERVISORY, PurdueZone.IDMZ],
            PurdueZone.IDMZ: [PurdueZone.LEVEL_3_OPERATIONS, PurdueZone.LEVEL_4_ENTERPRISE],
            PurdueZone.LEVEL_4_ENTERPRISE: [PurdueZone.IDMZ]  # Tidak boleh menembus langsung ke Level 0-3!
        }
        
        # Protokol legal per conduit
        self.protocol_rules = {
            (PurdueZone.LEVEL_1_CONTROL, PurdueZone.LEVEL_2_SUPERVISORY): ["MODBUS_TCP", "OPC_UA", "ETHERNET_IP"],
            (PurdueZone.LEVEL_2_SUPERVISORY, PurdueZone.LEVEL_3_OPERATIONS): ["OPC_UA", "PROFINET"],
            (PurdueZone.LEVEL_3_OPERATIONS, PurdueZone.IDMZ): ["OPC_UA_REPLICATION", "HTTPS", "MQTT_TLS"],
            (PurdueZone.IDMZ, PurdueZone.LEVEL_4_ENTERPRISE): ["HTTPS", "SQL_EXPORT", "REST_API"],
            (PurdueZone.LEVEL_4_ENTERPRISE, PurdueZone.IDMZ): ["HTTPS_READONLY", "REST_API"]
        }

    def inspect_packet(self, packet: Dict[str, Any]) -> Tuple[bool, str]:
        src_zone = packet.get("src_zone")
        dst_zone = packet.get("dst_zone")
        protocol = packet.get("protocol")
        payload = packet.get("payload", {})

        # Aturan 1: Cek apakah conduit traversal legal
        allowed_destinations = self.allowed_conduits.get(src_zone, [])
        if dst_zone not in allowed_destinations:
            return False, f"POLICY_VIOLATION: Traversal ilegal dari Level {src_zone} langsung ke Level {dst_zone}. Melanggar isolasi Purdue Model!"

        # Aturan 2: Verifikasi protokol yang diizinkan pada conduit tersebut
        conduit_key = (src_zone, dst_zone)
        valid_protocols = self.protocol_rules.get(conduit_key, [])
        if protocol not in valid_protocols:
            return False, f"PROTOCOL_VIOLATION: Protokol {protocol} tidak diizinkan pada conduit ({src_zone} -> {dst_zone})."

        # Aturan 3: Blokir perintah kendali langsung (write command) dari Enterprise ke plant
        if src_zone == PurdueZone.LEVEL_4_ENTERPRISE and payload.get("action") == "WRITE_COIL":
            return False, "SAFETY_VIOLATION: Perintah penulisan aktuator/coil langsung dari Enterprise dilarang keras oleh IDMZ Policy!"

        return True, "PACKET_PERMITTED: Sesuai spesifikasi conduit dan zonasi ISA-95/IEC 62443."

def run_simulation() -> Dict[str, Any]:
    gateway = IndustrialSecurityGateway()
    test_packets = [
        {
            "id": "PKT-01",
            "src_zone": PurdueZone.LEVEL_1_CONTROL,
            "dst_zone": PurdueZone.LEVEL_2_SUPERVISORY,
            "protocol": "MODBUS_TCP",
            "payload": {"fc": 3, "register": 40001, "count": 2}
        },
        {
            "id": "PKT-02",
            "src_zone": PurdueZone.LEVEL_3_OPERATIONS,
            "dst_zone": PurdueZone.IDMZ,
            "protocol": "MQTT_TLS",
            "payload": {"topic": "factory/line1/telemetry", "kurtosis": 3.8}
        },
        {
            "id": "PKT-03", # Ilegal: Traversal langsung Level 4 Enterprise ke Level 1 PLC
            "src_zone": PurdueZone.LEVEL_4_ENTERPRISE,
            "dst_zone": PurdueZone.LEVEL_1_CONTROL,
            "protocol": "MODBUS_TCP",
            "payload": {"fc": 5, "action": "WRITE_COIL", "val": 1}
        },
        {
            "id": "PKT-04", # Ilegal: Penulisan coil dari Enterprise ke IDMZ
            "src_zone": PurdueZone.LEVEL_4_ENTERPRISE,
            "dst_zone": PurdueZone.IDMZ,
            "protocol": "REST_API",
            "payload": {"action": "WRITE_COIL", "valve_id": 4}
        },
        {
            "id": "PKT-05", # Legal: Enterprise query read-only data agregat di IDMZ
            "src_zone": PurdueZone.LEVEL_4_ENTERPRISE,
            "dst_zone": PurdueZone.IDMZ,
            "protocol": "HTTPS_READONLY",
            "payload": {"query": "SELECT oee FROM plant_summary"}
        }
    ]

    results = []
    for pkt in test_packets:
        permitted, reason = gateway.inspect_packet(pkt)
        results.append({
            "packet_id": pkt["id"],
            "permitted": permitted,
            "reason": reason
        })

    # Verifikasi assert
    assert results[0]["permitted"] == True
    assert results[1]["permitted"] == True
    assert results[2]["permitted"] == False # Harus ditolak
    assert results[3]["permitted"] == False # Harus ditolak
    assert results[4]["permitted"] == True

    return {
        "status": "PASS",
        "total_packets": len(test_packets),
        "permitted_count": sum(1 for r in results if r["permitted"]),
        "blocked_count": sum(1 for r in results if not r["permitted"]),
        "details": results
    }

if __name__ == "__main__":
    report = run_simulation()
    print("=== INDUSTRIAL OT/IT SECURITY GATEWAY SIMULATION ===")
    print(json.dumps(report, indent=2))
    print("\nSTATUS VERIFIKASI: 100% PASS (Kebijakan Zonasi Purdue & IDMZ Terbukti Kuat)")

