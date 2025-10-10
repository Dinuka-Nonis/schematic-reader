import schemdraw
import schemdraw.logic as logic
import random
import os
import json
import shutil

# -----------------------------
# CONFIG
# -----------------------------
TOTAL_IMAGES = 50
OUTPUT_DIR = 'data/generated'
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
GATE_TYPES = [
    ("AND", logic.And),
    ("OR", logic.Or),
    ("NOT", logic.Not),
    ("NAND", logic.Nand),
    ("NOR", logic.Nor),
    ("XOR", logic.Xor)
]

random.seed(42)

# Clean output folder
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
for folder in ['train', 'val', 'test']:
    os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

# -----------------------------
# HELPER: Determine folder
# -----------------------------
def split_folder(index):
    if index <= TOTAL_IMAGES * TRAIN_SPLIT:
        return "train"
    elif index <= TOTAL_IMAGES * (TRAIN_SPLIT + VAL_SPLIT):
        return "val"
    else:
        return "test"

# -----------------------------
# GENERATE CIRCUIT IMAGE
# -----------------------------
def generate_circuit(index):
    d = schemdraw.Drawing()
    d.config(fontsize=14)

    num_gates = random.randint(5, 12)
    gate_metadata = []

    # Layout: place gates in a row
    x_pos = 0
    y_pos = 0
    spacing = 2  # spacing between gates

    for i in range(num_gates):
        name, gate_type = random.choice(GATE_TYPES)
        inputs = 1 if name == "NOT" else 2
        gate = gate_type(inputs=inputs)
        gate.at((x_pos, y_pos))
        d += gate

        # Record metadata
        gate_metadata.append({
            "id": f"g{i}",
            "type": name,
            "x": x_pos,
            "y": y_pos,
            "inputs": inputs
        })

        x_pos += spacing  # move right for next gate

    # Save image
    folder = split_folder(index)
    filename = f"circuit_{index:03d}.png"
    img_path = os.path.join(OUTPUT_DIR, folder, filename)
    d.save(img_path)

    # Save JSON label
    label_path = img_path.replace(".png", ".json")
    label_data = {
        "filename": filename,
        "folder": folder,
        "num_gates": num_gates,
        "gates": gate_metadata
    }
    with open(label_path, "w") as f:
        json.dump(label_data, f, indent=2)

    print(f"✅ Generated {filename} ({num_gates} gates)")

# -----------------------------
# GENERATE ALL IMAGES
# -----------------------------
for i in range(1, TOTAL_IMAGES + 1):
    generate_circuit(i)

print(f"\n🎉 Synthetic dataset created at {os.path.abspath(OUTPUT_DIR)}")
