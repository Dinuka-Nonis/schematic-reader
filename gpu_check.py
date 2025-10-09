# gpu_check.py - Verify GPU for Schematic Reader MVP (Final Version)
# Confirms PyTorch + CUDA setup and compares CPU vs GPU performance correctly.

import torch
import sys
import time

print("=" * 60)
print("🔍 Schematic Reader - GPU Verification & Benchmark")
print("=" * 60)

try:
    print(f"PyTorch Version: {torch.__version__}")
    is_cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {is_cuda_available}")

    if is_cuda_available:
        device_name = torch.cuda.get_device_name(0)
        print(f"CUDA Device Name: {device_name}")
    else:
        print("⚠️ GPU not available — falling back to CPU.")
        print("YOLO will still run, but slower (use device='cpu').")
        sys.exit(0)

except ImportError as e:
    print("❌ Error importing Torch:", e)
    print("Fix: Re-run Sub-task 2 (dependencies installation).")
    sys.exit(1)

# =====================
# Benchmark Comparison
# =====================
print("\n🧮 Running performance comparison... (this may take a few seconds)")

# Matrix size — increase for more accurate GPU performance
size = 20000  # can try 10,000 if VRAM allows
a_cpu = torch.rand(size, size)
b_cpu = torch.rand(size, size)

# CPU benchmark
cpu_start = time.time()
cpu_c = torch.mm(a_cpu, b_cpu)
cpu_end = time.time()
cpu_time = cpu_end - cpu_start
print(f"🖥️  CPU Matrix multiply time: {cpu_time:.4f} seconds")

# GPU benchmark
a_gpu = a_cpu.to("cuda")
b_gpu = b_cpu.to("cuda")
torch.cuda.synchronize()

gpu_start = time.time()
gpu_c = torch.mm(a_gpu, b_gpu)
torch.cuda.synchronize()  # ✅ wait for GPU to finish
gpu_end = time.time()
gpu_time = gpu_end - gpu_start
print(f"⚙️  GPU Matrix multiply time: {gpu_time:.4f} seconds")

# Comparison
speedup = cpu_time / gpu_time if gpu_time > 0 else float("inf")
print(f"\n🚀 GPU Speedup: {speedup:.2f}x faster than CPU")

print("=" * 60)
print("✅ GPU setup verified successfully — ready for YOLO training.")
print("=" * 60)
