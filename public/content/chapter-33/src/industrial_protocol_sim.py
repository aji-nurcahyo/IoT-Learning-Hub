"""
Chapter 33: Industrial IoT, Modbus & OPC UA Simulator
Simulasi frame Modbus RTU/TCP (Holding Registers) dan OPC UA Information Model node tree.
"""

from typing import Dict, List, Any, Optional
import struct


def calculate_modbus_crc16(data: bytes) -> int:
    """Menghitung CRC-16 Modbus standar (Polinom 0xA001, Init 0xFFFF)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


class ModbusSlaveSimulator:
    """Simulasi Modbus Slave dengan holding registers 16-bit."""
    def __init__(self, unit_id: int = 1):
        self.unit_id = unit_id
        # Holding registers: alamat 40001-40010 dipetakan ke indeks 0-9
        self.holding_registers: Dict[int, int] = {
            0: 255,   # Suhu x10 (25.5 C)
            1: 652,   # Kelembaban x10 (65.2 %)
            2: 1013,  # Tekanan Barometrik (1013 hPa)
            3: 1,     # Status Pompa (1 = ON, 0 = OFF)
        }

    def process_read_holding_registers_rtu(self, request_frame: bytes) -> bytes:
        """Memproses Function Code 03 (Read Holding Registers) format RTU."""
        if len(request_frame) != 8:
            raise ValueError("Panjang frame Modbus RTU tidak valid!")

        slave_id = request_frame[0]
        func_code = request_frame[1]
        start_addr = struct.unpack(">H", request_frame[2:4])[0]
        reg_count = struct.unpack(">H", request_frame[4:6])[0]
        rx_crc = struct.unpack("<H", request_frame[6:8])[0]

        calc_crc = calculate_modbus_crc16(request_frame[0:6])
        if rx_crc != calc_crc:
            raise ValueError(f"CRC Mismatch! Diterima: {rx_crc:04X}, Dihitung: {calc_crc:04X}")

        if slave_id != self.unit_id or func_code != 3:
            raise ValueError("Unit ID atau Function Code tidak cocok!")

        byte_count = reg_count * 2
        payload = bytearray([slave_id, func_code, byte_count])
        for i in range(start_addr, start_addr + reg_count):
            val = self.holding_registers.get(i, 0)
            payload.extend(struct.pack(">H", val))

        tx_crc = calculate_modbus_crc16(payload)
        payload.extend(struct.pack("<H", tx_crc))
        return bytes(payload)


class OpcUaNodeTreeSimulator:
    """Simulasi struktur Information Model hierarkis OPC UA (Nodes & Variables)."""
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {
            "ns=2;s=Root.Sensors": {
                "node_id": "ns=2;s=Root.Sensors",
                "node_class": "Object",
                "browse_name": "SensorsFolder",
                "children": ["ns=2;s=Root.Sensors.Temperature", "ns=2;s=Root.Sensors.Pressure"]
            },
            "ns=2;s=Root.Sensors.Temperature": {
                "node_id": "ns=2;s=Root.Sensors.Temperature",
                "node_class": "Variable",
                "browse_name": "Temperature",
                "data_type": "Float",
                "value": 25.5,
                "engineering_units": "degC"
            },
            "ns=2;s=Root.Sensors.Pressure": {
                "node_id": "ns=2;s=Root.Sensors.Pressure",
                "node_class": "Variable",
                "browse_name": "Pressure",
                "data_type": "Float",
                "value": 101.3,
                "engineering_units": "kPa"
            }
        }

    def read_variable(self, node_id: str) -> Dict[str, Any]:
        node = self.nodes.get(node_id)
        if not node:
            raise KeyError(f"NodeId {node_id} tidak ditemukan!")
        if node["node_class"] != "Variable":
            raise ValueError(f"NodeId {node_id} bukan variabel data!")
        return {
            "node_id": node["node_id"],
            "value": node["value"],
            "units": node["engineering_units"],
            "quality": "Good"
        }


def run_industrial_simulation() -> None:
    print("=== CHAPTER 33: INDUSTRIAL IOT & PROTOCOLS SIMULATION ===")
    
    # 1. Verifikasi Modbus RTU Frame & CRC
    slave = ModbusSlaveSimulator(unit_id=1)
    
    # Request: Slave 1, Func 3, Start 0x0000, Count 0x0002
    req_payload = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x02])
    crc = calculate_modbus_crc16(req_payload)
    req_frame = req_payload + struct.pack("<H", crc)
    
    print(f"Modbus RTU Request Frame: {req_frame.hex().upper()} (CRC: {crc:04X})")
    resp_frame = slave.process_read_holding_registers_rtu(req_frame)
    print(f"Modbus RTU Response Frame: {resp_frame.hex().upper()}")
    
    # Parse Response: Byte 0=Slave, Byte 1=Func, Byte 2=Bytes(4), Bytes 3-4=Reg0, Bytes 5-6=Reg1
    reg0_val = struct.unpack(">H", resp_frame[3:5])[0]
    reg1_val = struct.unpack(">H", resp_frame[5:7])[0]
    print(f"Nilai Register 0 (Suhu x10): {reg0_val} -> {reg0_val / 10.0} C")
    print(f"Nilai Register 1 (Kelembaban x10): {reg1_val} -> {reg1_val / 10.0} %")
    
    assert reg0_val == 255
    assert reg1_val == 652

    # 2. Verifikasi OPC UA Information Model
    opcua = OpcUaNodeTreeSimulator()
    temp_var = opcua.read_variable("ns=2;s=Root.Sensors.Temperature")
    press_var = opcua.read_variable("ns=2;s=Root.Sensors.Pressure")
    print(f"OPC UA Read Temp: {temp_var['value']} {temp_var['units']} (Quality: {temp_var['quality']})")
    print(f"OPC UA Read Pressure: {press_var['value']} {press_var['units']} (Quality: {press_var['quality']})")
    
    assert temp_var["value"] == 25.5
    assert press_var["value"] == 101.3
    print("STATUS: VERIFIED (Semua pengujian Modbus frame dan OPC UA Information Tree lulus 100%)")


if __name__ == "__main__":
    run_industrial_simulation()
