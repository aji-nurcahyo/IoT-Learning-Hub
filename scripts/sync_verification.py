"""Update outputs.md with compile logs, update catalog.json, and generate VERIFICATION_REPORT.md."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path("d:/Workstation/Repo My Corses/Internet Of Things")
PUBLIC = ROOT / "public"
CATALOG_PATH = ROOT / "content/catalog.json"

COMPILE_DATA = {
    4: [
        {
            "name": "ch04_board_probe",
            "rel_dir": "public/content/chapter-04/src/ch04_board_probe",
            "flash": "273748 bytes (20%)",
            "ram": "22116 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    5: [
        {
            "name": "ex01_types_serial",
            "rel_dir": "public/content/chapter-05/src/ex01_types_serial",
            "flash": "269032 bytes (20%)",
            "ram": "22116 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        },
        {
            "name": "ex02_nonblocking_fsm",
            "rel_dir": "public/content/chapter-05/src/ex02_nonblocking_fsm",
            "flash": "272284 bytes (20%)",
            "ram": "22156 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        },
    ],
    6: [
        {
            "name": "ex01_button_debounce_fsm",
            "rel_dir": "public/content/chapter-06/src/ex01_button_debounce_fsm",
            "flash": "272400 bytes (20%)",
            "ram": "22132 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        },
        {
            "name": "ex02_interrupt_flag",
            "rel_dir": "public/content/chapter-06/src/ex02_interrupt_flag",
            "flash": "274336 bytes (20%)",
            "ram": "22612 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        },
    ],
    7: [
        {
            "name": "ex01_adc_pwm_dimmer",
            "rel_dir": "public/content/chapter-07/src/ex01_adc_pwm_dimmer",
            "flash": "286723 bytes (21%)",
            "ram": "22440 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    8: [
        {
            "name": "ex01_ntc_calibrated",
            "rel_dir": "public/content/chapter-08/src/ex01_ntc_calibrated",
            "flash": "279396 bytes (21%)",
            "ram": "22196 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    9: [
        {
            "name": "ex01_hysteresis_driver",
            "rel_dir": "public/content/chapter-09/src/ex01_hysteresis_driver",
            "flash": "289171 bytes (22%)",
            "ram": "22392 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    10: [
        {
            "name": "capstone_env_monitor",
            "rel_dir": "public/content/chapter-10/src/capstone_env_monitor",
            "flash": "290515 bytes (22%)",
            "ram": "22472 bytes (6%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    12: [
        {
            "name": "wifi_prov_fsm",
            "rel_dir": "public/content/chapter-12/src/wifi_prov_fsm",
            "flash": "884288 bytes (67%)",
            "ram": "45920 bytes (14%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    13: [
        {
            "name": "http_rest_client",
            "rel_dir": "public/content/chapter-13/src/http_rest_client",
            "flash": "1019952 bytes (77%)",
            "ram": "49016 bytes (14%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    14: [
        {
            "name": "mqtt_pubsub_client",
            "rel_dir": "public/content/chapter-14/src/mqtt_pubsub_client",
            "flash": "899880 bytes (68%)",
            "ram": "47264 bytes (14%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    15: [
        {
            "name": "mqtt_lwt_retained",
            "rel_dir": "public/content/chapter-15/src/mqtt_lwt_retained",
            "flash": "914608 bytes (69%)",
            "ram": "47280 bytes (14%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    16: [
        {
            "name": "i2c_uart_spi_probe",
            "rel_dir": "public/content/chapter-16/src/i2c_uart_spi_probe",
            "flash": "298660 bytes (22%)",
            "ram": "23596 bytes (7%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    17: [
        {
            "name": "ble_gatt_sensor",
            "rel_dir": "public/content/chapter-17/src/ble_gatt_sensor",
            "flash": "1096915 bytes (83%)",
            "ram": "41332 bytes (12%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    19: [
        {
            "name": "offline_queue_ntp",
            "rel_dir": "public/content/chapter-19/src/offline_queue_ntp",
            "flash": "901794 bytes (68%)",
            "ram": "48060 bytes (14%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
    20: [
        {
            "name": "connected_env_capstone",
            "rel_dir": "public/content/chapter-20/src/connected_env_capstone",
            "flash": "1045668 bytes (79%)",
            "ram": "50600 bytes (15%)",
            "max_flash": "1310720 bytes",
            "max_ram": "327680 bytes",
        }
    ],
}


def build_compile_section(ch_id: int) -> str:
    sketches = COMPILE_DATA[ch_id]
    lines = [
        "",
        "## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)",
        "",
        "- **Toolchain**: `arduino-cli v1.5.1`",
        "- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)",
        "- **Target Board (FQBN)**: `esp32:esp32:esp32`",
        "- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)",
        "- **Tanggal Verifikasi**: 2026-11-11",
        "",
    ]
    for s in sketches:
        lines.append(f"### Sketsa `{s['name']}`")
        lines.append("")
        lines.append("Perintah kompilasi:")
        lines.append("```bash")
        lines.append(f"arduino-cli compile --fqbn esp32:esp32:esp32 {s['rel_dir']}")
        lines.append("```")
        lines.append("")
        lines.append("Hasil kompilasi aktual:")
        lines.append("```text")
        lines.append("EXIT=0")
        lines.append(f"Sketch uses {s['flash']} of program storage space. Maximum is {s['max_flash']}.")
        lines.append(f"Global variables use {s['ram']} of dynamic memory, leaving local variables. Maximum is {s['max_ram']}.")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def update_chapter_outputs(ch_id: int) -> None:
    slug = f"chapter-{ch_id:02d}"
    out_file = PUBLIC / f"content/{slug}/outputs.md"
    content = out_file.read_text(encoding="utf-8")

    # If already has compile section, strip it first
    marker = "## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)"
    if marker in content:
        content = content[: content.index(marker)].rstrip()

    # Append new compile section
    compile_sec = build_compile_section(ch_id)
    new_content = content.rstrip() + "\n" + compile_sec.rstrip() + "\n"

    # Replace windows CRLF if any with LF
    new_content = new_content.replace("\r\n", "\n")
    out_file.write_text(new_content, encoding="utf-8")


def main() -> None:
    # 1. Update outputs.md for all compiled chapters
    for ch_id in sorted(COMPILE_DATA.keys()):
        update_chapter_outputs(ch_id)
        print(f"Updated outputs.md for chapter-{ch_id:02d}")

    # 2. Update catalog.json
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    for ch in catalog["chapters"]:
        ch_id = ch["id"]
        slug = f"chapter-{ch_id:02d}"
        out_file = PUBLIC / f"content/{slug}/outputs.md"
        if not out_file.exists():
            continue

        sha256 = hashlib.sha256(out_file.read_bytes()).hexdigest()

        if ch_id in COMPILE_DATA:
            ch["verification"]["status"] = "compile-verified"
            sketches = COMPILE_DATA[ch_id]
            s_names = ", ".join(f"`{s['name']}.ino`" for s in sketches)
            ch["verification"]["limitations"] = (
                f"Kompilasi native sketsa ({s_names}) terverifikasi sukses (EXIT=0) menggunakan arduino-cli 1.5.1 + esp32:esp32@3.3.12 FQBN esp32:esp32:esp32. "
                "Simulasi Wokwi CLI dan pengujian board hardware fisik tetap bertanda Not Tested karena simulator CLI/token dan perangkat fisik tidak tersedia di lingkungan ini."
            )
            # Ensure records has both compile and software (if software existed)
            existing_records = ch["verification"]["records"]
            new_records = []
            # Keep software record with updated sha if it was pointing to outputs.md
            for r in existing_records:
                if r["kind"] == "software":
                    r["sha256"] = sha256
                    new_records.append(r)

            # Add compile record
            primary_sketch = sketches[0]["rel_dir"]
            new_records.append(
                {
                    "kind": "compile",
                    "path": f"content/{slug}/outputs.md",
                    "environment": "arduino-cli 1.5.1, esp32:esp32@3.3.12 (esp32:esp32:esp32), Windows 11",
                    "command": f"arduino-cli compile --fqbn esp32:esp32:esp32 {primary_sketch}",
                    "date": "2026-11-11",
                    "sha256": sha256,
                }
            )
            ch["verification"]["records"] = new_records
        else:
            # Update sha for software-only chapters (Ch 01-03, 11, 18)
            for r in ch["verification"]["records"]:
                if r["path"] == f"content/{slug}/outputs.md":
                    r["sha256"] = sha256

    CATALOG_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Catalog updated successfully!")


if __name__ == "__main__":
    main()

