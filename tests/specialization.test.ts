import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { execSync } from 'node:child_process';

const root = resolve(process.cwd());

test('Specialization Track B (Industrial IoT): seluruh 6 modul terverifikasi 100% PASS', () => {
  const modSlugs = ['mod-b01', 'mod-b02', 'mod-b03', 'mod-b04', 'mod-b05', 'mod-b06'];
  const scripts = [
    'purdue_security_sim.py',
    'vibration_mounting_sim.py',
    'modbus_polling_cycle_sim.py',
    'vibration_feature_envelope_sim.py',
    'sil_voting_reliability_sim.py',
    'industrial_pdm_capstone_platform.py'
  ];

  for (let i = 0; i < modSlugs.length; i++) {
    const slug = modSlugs[i];
    const script = scripts[i];
    const modDir = resolve(root, 'public/content/specialization/track-b', slug);

    // Pastikan 11 file esensial ada
    const expectedFiles = [
      'reading.md',
      'slides.json',
      'code.md',
      'diagram.svg',
      'exercises.md',
      'assignment.md',
      'review.md',
      'outputs.md',
      `src/${script}`
    ];

    for (const f of expectedFiles) {
      assert.ok(existsSync(resolve(modDir, f)), `File ${f} harus ada di ${slug}`);
    }

    // Jalankan eksekusi skrip python mandiri
    const scriptPath = resolve(modDir, 'src', script);
    const stdout = execSync(`python "${scriptPath}"`, { encoding: 'utf8' });
    assert.match(stdout, /STATUS VERIFIKASI: 100% PASS/);
    assert.match(stdout, /"status":\s*"PASS"/);
  }
});

test('Specialization Track D (AIoT & Edge Intelligence): seluruh 6 modul terverifikasi 100% PASS', () => {
  const modSlugs = ['mod-d01', 'mod-d02', 'mod-d03', 'mod-d04', 'mod-d05', 'mod-d06'];
  const scripts = [
    'hardware_roofline_model_sim.py',
    'fixed_point_mfcc_extractor_sim.py',
    'tinyml_qat_compression_sim.py',
    'ekf_sensor_fusion_sim.py',
    'edge_model_drift_sim.py',
    'multimodal_edge_capstone_platform.py'
  ];

  for (let i = 0; i < modSlugs.length; i++) {
    const slug = modSlugs[i];
    const script = scripts[i];
    const modDir = resolve(root, 'public/content/specialization/track-d', slug);

    const expectedFiles = [
      'reading.md',
      'slides.json',
      'code.md',
      'diagram.svg',
      'exercises.md',
      'assignment.md',
      'review.md',
      'outputs.md',
      `src/${script}`
    ];

    for (const f of expectedFiles) {
      assert.ok(existsSync(resolve(modDir, f)), `File ${f} harus ada di ${slug}`);
    }

    const scriptPath = resolve(modDir, 'src', script);
    const stdout = execSync(`python "${scriptPath}"`, { encoding: 'utf8' });
    assert.match(stdout, /STATUS VERIFIKASI: 100% PASS/);
    assert.match(stdout, /"status":\s*"PASS"/);
  }
});

