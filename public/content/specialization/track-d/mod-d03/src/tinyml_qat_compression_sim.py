import math
import json

def fake_quantize(val, scale=0.02, zero_point=0):
    # Simulasi kuantisasi integer INT8 [-128, 127]
    q = round(val / scale) + zero_point
    q_clamped = max(-128, min(127, q))
    # Dequantize kembali ke float (simulasi forward pass QAT)
    return (q_clamped - zero_point) * scale

def simulate_qat_step(weight, grad_loss, lr=0.01, scale=0.02):
    # Straight-Through Estimator (STE):
    # Gradien dilewatkan langsung d(q)/d(w) = 1 jika |w/scale| <= 128, else 0
    if abs(weight / scale) <= 128:
        grad_ste = grad_loss
    else:
        grad_ste = 0.0 # Gradien terpotong pada batas saturasi
        
    updated_weight = weight - (lr * grad_ste)
    quantized_weight = fake_quantize(updated_weight, scale)
    return updated_weight, quantized_weight

def run_simulation():
    # Model baseline FP32: 10 bobot layer filter
    fp32_weights = [0.15, -0.42, 0.88, -0.05, 1.25, -0.95, 0.33, -0.12, 0.64, -0.55]
    
    # 1. Post-Training Quantization (PTQ) naive
    scale = 0.01
    ptq_weights = [fake_quantize(w, scale) for w in fp32_weights]
    ptq_error = sum((w - qw) ** 2 for w, qw in zip(fp32_weights, ptq_weights)) / len(fp32_weights)
    
    # 2. Satu siklus iterasi QAT dengan penyesuaian gradien
    qat_weights = []
    for w in fp32_weights:
        grad_dummy = (w - 0.5) * 0.2 # Gradien optimasi loss
        w_real, w_q = simulate_qat_step(w, grad_dummy, lr=0.05, scale=scale)
        qat_weights.append(w_q)
        
    # 3. Structured Pruning: pangkas bobot beramplitudo kecil (< 0.2) menjadi 0
    pruned_weights = [w if abs(w) >= 0.2 else 0.0 for w in qat_weights]
    sparsity = sum(1 for w in pruned_weights if w == 0.0) / len(pruned_weights)
    
    assert ptq_error < 0.001
    assert sparsity >= 0.20 # Minimal 20% bobot terpangkas!
    
    return {
        "status": "PASS",
        "baseline_fp32_count": len(fp32_weights),
        "ptq_mean_squared_error": round(ptq_error, 6),
        "pruned_sparsity_ratio": round(sparsity * 100, 1),
        "sample_qat_pruned_weights": [round(w, 4) for w in pruned_weights[:5]]
    }

if __name__ == "__main__":
    out = run_simulation()
    print("=== TINYML QAT & STRUCTURED PRUNING SIMULATION ===")
    print(json.dumps(out, indent=2))
    print("\nSTATUS VERIFIKASI: 100% PASS (Model QAT & Pruning Tervalidasi)")
