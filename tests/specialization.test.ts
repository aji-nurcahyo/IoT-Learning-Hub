import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
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

test('Specialization Track C (Smart Agriculture): seluruh 6 modul terverifikasi 100% PASS', () => {
  const modSlugs = ['mod-c01', 'mod-c02', 'mod-c03', 'mod-c04', 'mod-c05', 'mod-c06'];
  const scripts = [
    'soil_moisture_topp_sim.py',
    'sensor_calibration_drift_sim.py',
    'lorawan_canopy_propagation_sim.py',
    'solar_energy_harvesting_sim.py',
    'fao56_evapotranspiration_sim.py',
    'agricultural_capstone_network_sim.py'
  ];

  for (let i = 0; i < modSlugs.length; i++) {
    const slug = modSlugs[i];
    const script = scripts[i];
    const modDir = resolve(root, 'public/content/specialization/track-c', slug);

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

test('Specialization Track A (Smart Home & Building Automation): seluruh 6 modul terverifikasi 100% PASS', () => {
  const modSlugs = ['mod-a01', 'mod-a02', 'mod-a03', 'mod-a04', 'mod-a05', 'mod-a06'];
  const scripts = [
    'building_coexistence_cir_sim.py',
    'occupancy_iaq_dcv_sim.py',
    'matter_thread_commissioning_sim.py',
    'building_energy_peakshaving_sim.py',
    'lifesafety_interlock_evacuation_sim.py',
    'building_capstone_controller_sim.py'
  ];

  for (let i = 0; i < modSlugs.length; i++) {
    const slug = modSlugs[i];
    const script = scripts[i];
    const modDir = resolve(root, 'public/content/specialization/track-a', slug);

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

test('Specialization Track E (Smart Cities & Telecommunications): seluruh 6 modul terverifikasi 100% PASS', () => {
  const modSlugs = ['mod-e01', 'mod-e02', 'mod-e03', 'mod-e04', 'mod-e05', 'mod-e06'];
  const scripts = [
    'smart_city_ngsild_multitenant_sim.py',
    'urban_rf_propagation_sim.py',
    'cellular_iot_energy_sim.py',
    'municipal_contention_queue_sim.py',
    'geospatial_telemetry_h3_sim.py',
    'city_scale_capstone_platform.py'
  ];

  for (let i = 0; i < modSlugs.length; i++) {
    const slug = modSlugs[i];
    const script = scripts[i];
    const modDir = resolve(root, 'public/content/specialization/track-e', slug);

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
