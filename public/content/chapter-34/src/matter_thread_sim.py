"""
Chapter 34: Interoperability, Matter & Thread Fundamentals Simulator
Simulasi topologi Thread mesh (Leader, Router, End Device) dan alur Matter commissioning (PASE/CASE).
"""

from typing import Dict, List, Any, Optional
import hashlib
import secrets


class ThreadNode:
    def __init__(self, node_id: str, role: str, rloc16: str):
        self.node_id = node_id
        self.role = role  # "Leader", "Router", "Child/EndDevice", "BorderRouter"
        self.rloc16 = rloc16
        self.neighbors: List[str] = []

    def add_neighbor(self, neighbor_id: str) -> None:
        if neighbor_id not in self.neighbors:
            self.neighbors.append(neighbor_id)


class ThreadMeshSimulator:
    """Simulasi topologi jaringan Thread berbasis IEEE 802.15.4 dan 6LoWPAN."""
    def __init__(self, pan_id: str = "0x1234"):
        self.pan_id = pan_id
        self.nodes: Dict[str, ThreadNode] = {}
        self.leader_id: Optional[str] = None

    def add_node(self, node_id: str, role: str, rloc16: str) -> ThreadNode:
        node = ThreadNode(node_id, role, rloc16)
        self.nodes[node_id] = node
        if role == "Leader":
            self.leader_id = node_id
        return node

    def link_nodes(self, id1: str, id2: str) -> None:
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].add_neighbor(id2)
            self.nodes[id2].add_neighbor(id1)

    def route_packet(self, src_id: str, dst_id: str) -> List[str]:
        """Menemukan rute paket multihop melintasi jaringan mesh."""
        if src_id not in self.nodes or dst_id not in self.nodes:
            raise ValueError("Node sumber atau tujuan tidak valid!")

        # BFS shortest path
        queue = [[src_id]]
        visited = set([src_id])

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == dst_id:
                return path
            for neighbor in self.nodes[node].neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return []


class MatterCommissioningSimulator:
    """Simulasi protokol commissioning Matter (PASE berbasis SPAKE2+ & CASE)."""
    def __init__(self, setup_pin_code: int = 20202021, discriminator: int = 3840):
        self.setup_pin_code = setup_pin_code
        self.discriminator = discriminator
        self.is_commissioned = False
        self.fabric_id: Optional[str] = None
        self.node_id: Optional[str] = None

    def execute_pase(self, provided_pin: int) -> bool:
        """Password-Authenticated Session Establishment (PASE)."""
        if provided_pin == self.setup_pin_code:
            # Simulasi handshake kriptografi SPAKE2+
            return True
        return False

    def complete_commissioning(self, fabric_id: str, assigned_node_id: str, noc_cert: str) -> Dict[str, Any]:
        """Konfigurasi Node Operational Certificate (NOC) dan Fabric ID."""
        self.fabric_id = fabric_id
        self.node_id = assigned_node_id
        self.is_commissioned = True
        return {
            "status": "SUCCESS",
            "fabric_id": self.fabric_id,
            "node_id": self.node_id,
            "session": "CASE_READY"
        }


def run_matter_thread_simulation() -> None:
    print("=== CHAPTER 34: MATTER & THREAD SIMULATION ===")
    
    # 1. Verifikasi Topologi Thread Mesh
    mesh = ThreadMeshSimulator(pan_id="0x7E3A")
    mesh.add_node("Leader", "Leader", "0x0001")
    mesh.add_node("BorderRouter", "BorderRouter", "0x0400")
    mesh.add_node("Router1", "Router", "0x0800")
    mesh.add_node("DoorLock", "Child/EndDevice", "0x0801")
    mesh.add_node("LightSensor", "Child/EndDevice", "0x0401")

    # Tautkan hubungan topologi
    mesh.link_nodes("BorderRouter", "Leader")
    mesh.link_nodes("Leader", "Router1")
    mesh.link_nodes("Router1", "DoorLock")
    mesh.link_nodes("BorderRouter", "LightSensor")

    route = mesh.route_packet("DoorLock", "LightSensor")
    print(f"Thread Multihop Route (DoorLock -> LightSensor): {' -> '.join(route)}")
    assert route == ["DoorLock", "Router1", "Leader", "BorderRouter", "LightSensor"]

    # 2. Verifikasi Matter Commissioning
    comm = MatterCommissioningSimulator(setup_pin_code=20202021, discriminator=3840)
    
    # Uji verifikasi PIN salah
    assert comm.execute_pase(11112222) is False
    # Uji verifikasi PIN benar
    assert comm.execute_pase(20202021) is True
    
    cert_dummy = hashlib.sha256(b"NOC_DUMMY_CERT").hexdigest()
    res = comm.complete_commissioning(fabric_id="FABRIC_01", assigned_node_id="NODE_42", noc_cert=cert_dummy)
    print(f"Matter Commissioning Complete: Fabric={res['fabric_id']}, NodeId={res['node_id']}, Session={res['session']}")
    
    assert comm.is_commissioned is True
    print("STATUS: VERIFIED (Semua pengujian Thread Mesh routing dan Matter Commissioning lulus 100%)")


if __name__ == "__main__":
    run_matter_thread_simulation()
