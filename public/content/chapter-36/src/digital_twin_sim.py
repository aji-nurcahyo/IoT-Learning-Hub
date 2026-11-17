"""
Chapter 36: Digital Twins & System Modeling Simulator
Simulasi sinkronisasi state fisik-digital, estimasi suhu ruang via model dinamika termal 1-orde (Newton Cooling), dan simulasi skenario 'What-If'.
"""

from typing import Dict, List, Any, Tuple


class ThermalSystemModel:
    """Model termal 1-orde berbasis Hukum Pendinginan Newton & Pemanasan Joule."""
    def __init__(self, c_th: float = 500.0, r_th: float = 0.05, ambient_temp: float = 25.0):
        self.c_th = c_th          # Kapasitas panas (Joule / Kelvin)
        self.r_th = r_th          # Resistansi termal konveksi (Kelvin / Watt)
        self.ambient_temp = ambient_temp
        self.current_temp = ambient_temp

    def step(self, heat_input_watts: float, dt_seconds: float) -> float:
        """Menghitung suhu langkah berikutnya: dT/dt = (Q_in - (T - T_amb)/R_th) / C_th."""
        heat_dissipated = (self.current_temp - self.ambient_temp) / self.r_th
        net_heat_flow = heat_input_watts - heat_dissipated
        dt_temp = (net_heat_flow / self.c_th) * dt_seconds
        self.current_temp += dt_temp
        return round(self.current_temp, 3)


class DigitalTwinSynchronizer:
    """Sinkronisasi Kembaran Digital antara telemetri fisik dan estimasi model virtual."""
    def __init__(self, model: ThermalSystemModel, error_threshold: float = 2.0):
        self.model = model
        self.error_threshold = error_threshold
        self.physical_state: Dict[str, Any] = {}
        self.digital_state: Dict[str, Any] = {}
        self.discrepancy_history: List[float] = []

    def update_physical_telemetry(self, temp: float, heater_power_watts: float) -> None:
        self.physical_state = {
            "measured_temp": temp,
            "heater_power_watts": heater_power_watts
        }

    def sync_and_estimate(self, dt: float) -> Dict[str, Any]:
        """Langkah sinkronisasi: update model digital dan hitung deviasi fisik-digital."""
        p_watts = self.physical_state.get("heater_power_watts", 0.0)
        p_temp = self.physical_state.get("measured_temp", self.model.ambient_temp)

        # Perbarui estimasi model digital
        estimated_temp = self.model.step(heat_input_watts=p_watts, dt_seconds=dt)
        residual = abs(p_temp - estimated_temp)
        self.discrepancy_history.append(residual)

        is_calibrated = residual <= self.error_threshold
        status = "SYNCHRONIZED" if is_calibrated else "DEVIATION_ALERT"

        self.digital_state = {
            "estimated_temp": estimated_temp,
            "residual": round(residual, 3),
            "status": status
        }
        return self.digital_state

    def simulate_what_if_scenario(self, future_power_watts: float, duration_seconds: float, dt: float = 1.0) -> float:
        """Simulasi skenario What-If: prediksi suhu akhir jika daya dinaikkan."""
        temp_sim = self.model.current_temp
        steps = int(duration_seconds / dt)
        for _ in range(steps):
            heat_diss = (temp_sim - self.model.ambient_temp) / self.model.r_th
            temp_sim += ((future_power_watts - heat_diss) / self.model.c_th) * dt
        return round(temp_sim, 2)


def run_digital_twin_simulation() -> None:
    print("=== CHAPTER 36: DIGITAL TWIN & SYSTEM MODELING SIMULATION ===")
    
    # 1. Inisialisasi Model Termal Fisik-Digital
    model = ThermalSystemModel(c_th=300.0, r_th=0.1, ambient_temp=25.0)
    twin = DigitalTwinSynchronizer(model=model, error_threshold=1.5)

    # 2. Siklus Telemetri Fisik (Pemanas 100 Watt selama 5 langkah)
    print("Siklus Sinkronisasi Real-Time (Daya = 100W, dt = 2s):")
    simulated_physical_readings = [25.5, 26.1, 26.8, 27.4, 28.0]
    for i, p_temp in enumerate(simulated_physical_readings):
        twin.update_physical_telemetry(temp=p_temp, heater_power_watts=100.0)
        state = twin.sync_and_estimate(dt=2.0)
        print(f"Step {i+1} | Fisik: {p_temp} C | Digital: {state['estimated_temp']} C | Residual: {state['residual']} C | Status: {state['status']}")
        assert state["status"] == "SYNCHRONIZED", f"Deviasi melebihi batas pada step {i+1}!"

    # 3. Simulasi What-If Scenario: Prediksi Suhu Jika Heater Dinaikkan ke 250 Watt selama 60 Detik
    predicted_t = twin.simulate_what_if_scenario(future_power_watts=250.0, duration_seconds=60.0)
    print(f"\nSimulasi What-If: Prediksi Suhu 60s ke Depan pada 250W -> {predicted_t} C")
    assert predicted_t > simulated_physical_readings[-1], "Prediksi pemanasan What-If gagal!"
    print("STATUS: VERIFIED (Semua pengujian sinkronisasi Digital Twin dan skenario What-If lulus 100%)")


if __name__ == "__main__":
    run_digital_twin_simulation()
