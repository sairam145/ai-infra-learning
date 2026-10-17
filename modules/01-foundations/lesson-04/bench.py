import os, time, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

NAME = "distilbert-base-uncased-finetuned-sst-2-english"   # small sentiment model
device = "cuda" if torch.cuda.is_available() else "cpu"

# --- 1. LOAD: download weights from Hugging Face, put on device, exam mode ---
tok = AutoTokenizer.from_pretrained(NAME)
model = AutoModelForSequenceClassification.from_pretrained(NAME).to(device)
model.eval()
params = sum(p.numel() for p in model.parameters())
print(f"Device: {device} | Parameters: {params/1e6:.1f}M | Expected FP32 size: {params*4/1e6:.0f} MB")

def run(m, texts, dev):
    inputs = tok(texts, return_tensors="pt", padding=True, truncation=True).to(dev)
    with torch.no_grad():                       # exam mode: no learning, less memory
        return m(**inputs).logits

# --- 2. WARM-UP: first call vs. later calls ---
t = time.perf_counter(); run(model, ["hello"], device); cold = (time.perf_counter() - t) * 1000
for _ in range(5): run(model, ["hello"], device)
t = time.perf_counter(); run(model, ["hello"], device); warm = (time.perf_counter() - t) * 1000
print(f"\nWARM-UP  first call: {cold:.1f} ms | after warm-up: {warm:.1f} ms")

# --- 3. BATCHING: same text, different batch sizes ---
text = "The deployment finished and everything works great"
print("\nBATCHING")
for bs in [1, 8, 32]:
    batch = [text] * bs
    run(model, batch, device)                    # warm this batch size
    n = 5
    t = time.perf_counter()
    for _ in range(n): run(model, batch, device)
    per_batch = (time.perf_counter() - t) / n
    print(f"  batch {bs:>2}: {per_batch*1000:7.1f} ms per batch | {bs/per_batch:7.1f} texts/sec")

# --- 4. IT WORKS: real predictions ---
labels = model.config.id2label
print("\nPREDICTIONS")
for s in ["I love this product", "This is the worst service ever"]:
    p = run(model, [s], device).softmax(-1)[0]
    print(f"  {s!r} -> {labels[int(p.argmax())]} ({p.max():.2f})")

# --- 5. SAVE weights only (state_dict) ---
torch.save(model.state_dict(), "weights_fp32.pth")
fp32_mb = os.path.getsize("weights_fp32.pth") / 1e6
print(f"\nSAVED  FP32 weights: {fp32_mb:.0f} MB")

# --- 6. QUANTIZE: FP32 -> INT8 (CPU) and compare size + speed ---
try:
    from torch.ao.quantization import quantize_dynamic
    cpu_model = model.to("cpu")
    q = quantize_dynamic(cpu_model, {torch.nn.Linear}, dtype=torch.qint8)
    torch.save(q.state_dict(), "weights_int8.pth")
    int8_mb = os.path.getsize("weights_int8.pth") / 1e6
    batch = [text] * 8
    for m in (cpu_model, q): run(m, batch, "cpu")
    def speed(m):
        t = time.perf_counter()
        for _ in range(5): run(m, batch, "cpu")
        return (time.perf_counter() - t) / 5 * 1000
    print(f"QUANTIZE  INT8 weights: {int8_mb:.0f} MB ({fp32_mb/int8_mb:.1f}x smaller)")
    print(f"          batch 8 on CPU: FP32 {speed(cpu_model):.1f} ms vs INT8 {speed(q):.1f} ms")
    p = run(q, ["I love this product"], "cpu").softmax(-1)[0]
    print(f"          INT8 still says: {labels[int(p.argmax())]} ({p.max():.2f})")
except Exception as e:
    print(f"QUANTIZE skipped on this PyTorch version: {e}")
