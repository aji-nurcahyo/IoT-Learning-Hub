"""
Chapter 37: Scalable IoT Architecture & Deployment Simulator
Simulasi load balancing partisi MQTT (Consistent Hashing / Sharding), penanganan backpressure antrean, dan skalabilitas horizontal worker.
"""

from typing import List, Dict, Any, Optional
import hashlib


class PartitionedBrokerCluster:
    """Simulasi cluster broker/ingestion dengan pembagian partisi berbasis hash kunci perangkat."""
    def __init__(self, num_partitions: int = 4):
        self.num_partitions = num_partitions
        self.partitions: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(num_partitions)}
        self.partition_queue_limit = 50
        self.dropped_messages = 0

    def get_partition(self, device_id: str) -> int:
        """Menghitung indeks partisi deterministik via MD5 hash."""
        digest = hashlib.md5(device_id.encode("utf-8")).hexdigest()
        return int(digest, 16) % self.num_partitions

    def publish_telemetry(self, device_id: str, payload: Dict[str, Any]) -> bool:
        """Mengirim pesan ke partisi tujuan dengan proteksi backpressure queue."""
        p_id = self.get_partition(device_id)
        queue = self.partitions[p_id]

        if len(queue) >= self.partition_queue_limit:
            self.dropped_messages += 1
            return False  # Backpressure aktif (Drop / Pushback)

        queue.append({"device_id": device_id, "payload": payload})
        return True

    def consume_batch(self, partition_id: int, max_batch_size: int = 10) -> List[Dict[str, Any]]:
        """Konsumsi batch data oleh worker pemroses."""
        queue = self.partitions[partition_id]
        batch = queue[:max_batch_size]
        self.partitions[partition_id] = queue[max_batch_size:]
        return batch


def run_scalability_simulation() -> None:
    print("=== CHAPTER 37: SCALABLE IOT ARCHITECTURE SIMULATION ===")
    
    # 1. Inisialisasi Cluster 4 Partisi
    cluster = PartitionedBrokerCluster(num_partitions=4)

    # 2. Distribusi Beban 100 Perangkat Acak
    print("Mendistribusikan telemetri dari 100 perangkat IoT...")
    for i in range(100):
        dev_id = f"dev-edge-{i:03d}"
        success = cluster.publish_telemetry(device_id=dev_id, payload={"val": 20.0 + i})
        assert success is True, f"Publikasi gagal untuk {dev_id}!"

    # 3. Audit Distribusi Beban Lintas Partisi
    counts = [len(cluster.partitions[p]) for p in range(4)]
    print(f"Distribusi Pesan pada Partisi [0, 1, 2, 3]: {counts}")
    assert sum(counts) == 100
    for p, c in enumerate(counts):
        assert c > 0, f"Partisi {p} tidak menerima beban sama sekali (Hashing cacat)!"

    # 4. Uji Proteksi Backpressure
    print("Menguji batas antrean partisi (Backpressure test)...")
    target_p = 0
    test_dev = "fixed-hash-device-for-p0"
    while cluster.get_partition(test_dev) != target_p:
        test_dev += "x"

    # Penuhi partisi 0 hingga batas maksimum 50
    current_in_p0 = len(cluster.partitions[target_p])
    for _ in range(55 - current_in_p0):
        cluster.publish_telemetry(device_id=test_dev, payload={"burst": True})

    print(f"Partisi 0 Size: {len(cluster.partitions[target_p])} | Total Dropped (Backpressure): {cluster.dropped_messages}")
    assert len(cluster.partitions[target_p]) == 50
    assert cluster.dropped_messages == 5

    # 5. Konsumsi Paralel oleh Worker
    drained = cluster.consume_batch(partition_id=target_p, max_batch_size=20)
    print(f"Worker menguras {len(drained)} pesan dari Partisi 0. Sisa antrean: {len(cluster.partitions[target_p])}")
    assert len(drained) == 20
    assert len(cluster.partitions[target_p]) == 30

    print("STATUS: VERIFIED (Semua pengujian sharding partisi, hash deterministik, dan backpressure lulus 100%)")


if __name__ == "__main__":
    run_scalability_simulation()
