import schemdraw
import schemdraw.logic as logic
import random
import os
import json
import shutil

# -----------------------------
# CONFIGURATION
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

# YOLO class mapping
CLASS_MAP = {name: idx for idx, (name, _) in enumerate(GATE_TYPES)}

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
# GENERATE CIRCUIT IMAGE & YOLO LABEL
# -----------------------------
def generate_circuit(index):
    d = schemdraw.Drawing()
    d.config(fontsize=14)
    
    num_gates = random.randint(5, 8)  # keep manageable for image
    gate_metadata = []

    # Layout: grid-style with rotation
    x_pos = 0
    y_pos = 0
    spacing_x = 2
    spacing_y = 1.5

    img_width = num_gates * spacing_x + 2
    img_height = 4  # fixed height

    yolo_lines = []

    for i in range(num_gates):
        name, gate_type = random.choice(GATE_TYPES)
        inputs = 1 if name == "NOT" else 2

        gate = gate_type(inputs=inputs)

        # Random rotation (multiples of 90)
        angle = random.choice([0, 90, 180, 270])
        try:
            gate.angle = angle
        except AttributeError:
            pass  # fallback if not supported

        # Small random offset to avoid perfect alignment
        offset_x = random.uniform(-0.3, 0.3)
        offset_y = random.uniform(-0.3, 0.3)

        gate.at((x_pos + offset_x, y_pos + offset_y))
        d += gate

        # Approx bounding box for YOLO (schemdraw has no direct bbox; assume 1x1 units)
        bbox_w, bbox_h = 1.0, 1.0
        x_center = x_pos + offset_x + bbox_w / 2
        y_center = y_pos + offset_y + bbox_h / 2

        # Normalize for YOLO
        x_norm = x_center / img_width
        y_norm = (y_center + img_height / 2) / img_height  # center adjustment
        w_norm = bbox_w / img_width
        h_norm = bbox_h / img_height

        class_id = CLASS_MAP[name]
        yolo_lines.append(f"{class_id} {x_norm:.6f} {y_norm:.6f} {w_norm:.6f} {h_norm:.6f}")

        # Metadata
        gate_metadata.append({
            "id": f"g{i}",
            "type": name,
            "x": round(x_pos + offset_x, 2),
            "y": round(y_pos + offset_y, 2),
            "rotation": angle,
            "inputs": inputs
        })

        # Update positions
        x_pos += spacing_x
        if x_pos > 8:  # max width before new row
            x_pos = 0
            y_pos -= spacing_y

    # Save image
    folder = split_folder(index)
    filename = f"circuit_{index:03d}.png"
    img_path = os.path.join(OUTPUT_DIR, folder, filename)
    d.save(img_path)

    # Save JSON metadata
    label_path_json = img_path.replace(".png", ".json")
    label_data = {
        "filename": filename,
        "folder": folder,
        "num_gates": num_gates,
        "gates": gate_metadata
    }
    with open(label_path_json, "w") as f:
        json.dump(label_data, f, indent=2)

    # Save YOLO .txt label
    label_path_txt = img_path.replace(".png", ".txt")
    with open(label_path_txt, "w") as f:
        f.write("\n".join(yolo_lines))

    print(f"✅ Generated {filename} ({num_gates} gates) -> YOLO label created")

# -----------------------------
# GENERATE ALL IMAGES
# -----------------------------
for i in range(1, TOTAL_IMAGES + 1):
    generate_circuit(i)

print(f"\n🎉 YOLO-ready synthetic dataset created at {os.path.abspath(OUTPUT_DIR)}")

# -----------------------------
# CREATE classes.txt
# -----------------------------
classes_txt = os.path.join(OUTPUT_DIR, "classes.txt")
with open(classes_txt, "w") as f:
    for name in CLASS_MAP.keys():
        f.write(f"{name}\n")
print(f"📄 Class list saved to {classes_txt}")
