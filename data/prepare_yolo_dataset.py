# prepare_yolo_dataset.py
import shutil
from pathlib import Path
import os
import sys
import json

# Run this script from: D:\Projects\SchematicReader\data
BASE = Path.cwd()  # expects to be run from data/ folder
print("Base folder:", BASE)

# Source folders (adjust if your folders are elsewhere)
sources = [
    # Augmented (train/valid/test) -> each has images/ and labels/
    (BASE / "Augmented" / "train" / "images", BASE / "Augmented" / "train" / "labels"),
    (BASE / "Augmented" / "valid" / "images", BASE / "Augmented" / "valid" / "labels"),
    (BASE / "Augmented" / "test" / "images",  BASE / "Augmented" / "test" / "labels"),
    # Generated (train/val/test) -> generated folders likely contain png + txt
    (BASE / "generated" / "train", BASE / "generated" / "train"),
    (BASE / "generated" / "val",   BASE / "generated" / "val"),
    (BASE / "generated" / "test",  BASE / "generated" / "test"),
]

# Destination YOLO structure
YOLO_ROOT = BASE / "yolo_data"
IMG_TRAIN = YOLO_ROOT / "images" / "train"
IMG_VAL   = YOLO_ROOT / "images" / "val"
LBL_TRAIN = YOLO_ROOT / "labels" / "train"
LBL_VAL   = YOLO_ROOT / "labels" / "val"

for p in [IMG_TRAIN, IMG_VAL, LBL_TRAIN, LBL_VAL]:
    p.mkdir(parents=True, exist_ok=True)

# Class names (must match your datasets). Edit if different.
CLASSES = ["AND", "OR", "NOT", "NAND", "NOR", "XOR"]

# Helper to copy from source pair -> destination pair
def copy_pairs(img_src: Path, lbl_src: Path, dest_img: Path, dest_lbl: Path, default_label_exts=(".txt", ".xml")):
    if not img_src.exists():
        print(f"  ⚠️ image source {img_src} does not exist, skipping")
        return 0,0
    img_files = [p for p in img_src.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
    copied = 0
    skipped = 0
    for img in img_files:
        stem = img.stem
        # find label file
        lbl_candidates = []
        if lbl_src.exists():
            # common txt label
            txt = lbl_src / f"{stem}.txt"
            if txt.exists(): lbl_candidates.append(txt)
            # sometimes Roboflow uses same images folder with labels in separate structure; check .xml
            xml = lbl_src / f"{stem}.xml"
            if xml.exists(): lbl_candidates.append(xml)
            # if generated dataset put txt in same folder as images (source==lbl_src)
            txt2 = lbl_src / f"{stem}.txt"
            if txt2.exists() and txt2 not in lbl_candidates: lbl_candidates.append(txt2)

        # if no label found, we will skip (you can change to allow unlabeled)
        if not lbl_candidates:
            print(f"    - no label found for {img.name}; skipping (place label or accept unlabeled)")
            skipped += 1
            continue

        # choose first label candidate
        lbl = lbl_candidates[0]

        # avoid name collisions in destination
        dest_img_path = dest_img / img.name
        dest_lbl_path = dest_lbl / lbl.name

        counter = 1
        while dest_img_path.exists() or dest_lbl_path.exists():
            dest_img_path = dest_img.with_name(dest_img.name) / f"{img.stem}_{counter}{img.suffix}"
            dest_lbl_path = dest_lbl.with_name(dest_lbl.name) / f"{lbl.stem}_{counter}{lbl.suffix}"
            # simpler approach: create new paths with counter
            dest_img_path = dest_img / f"{img.stem}_{counter}{img.suffix}"
            dest_lbl_path = dest_lbl / f"{lbl.stem}_{counter}{lbl.suffix}"
            counter += 1

        shutil.copy2(img, dest_img_path)
        shutil.copy2(lbl, dest_lbl_path)
        copied += 1

    return copied, skipped

# Do copying:
total_copied = 0
total_skipped = 0

# Heuristic: treat Augmented's 'valid' as val, 'train' as train.
for img_src, lbl_src in sources:
    # determine mapping
    if "Augmented" in str(img_src):
        if "train" in str(img_src):
            dest_img, dest_lbl = IMG_TRAIN, LBL_TRAIN
        elif "valid" in str(img_src) or "val" in str(img_src):
            dest_img, dest_lbl = IMG_VAL, LBL_VAL
        elif "test" in str(img_src):
            dest_img, dest_lbl = IMG_VAL, LBL_VAL  # map test -> val (or adjust)
        else:
            dest_img, dest_lbl = IMG_TRAIN, LBL_TRAIN
    elif "generated" in str(img_src):
        # simple heuristic: generated/train -> train, val-> val, test->val
        if "train" in str(img_src):
            dest_img, dest_lbl = IMG_TRAIN, LBL_TRAIN
        elif "val" in str(img_src):
            dest_img, dest_lbl = IMG_VAL, LBL_VAL
        else:
            dest_img, dest_lbl = IMG_VAL, LBL_VAL

    print(f"\nCopying from {img_src}  ->  {dest_img}")
    copied, skipped = copy_pairs(img_src, lbl_src, dest_img, dest_lbl)
    total_copied += copied
    total_skipped += skipped
    print(f"  copied: {copied}, skipped(no-label): {skipped}")

# Summary
print("\n=== SUMMARY ===")
print(f"Total copied images: {total_copied}")
print(f"Total skipped (no label): {total_skipped}")
print(f"YOLO root created at: {YOLO_ROOT}")

# Create classes.txt
classes_file = YOLO_ROOT / "classes.txt"
with open(classes_file, "w") as f:
    for c in CLASSES:
        f.write(c + "\n")
print("classes.txt written:", classes_file)

# Create data.yaml
data_yaml = BASE / "data.yaml"
yaml_text = f"""train: {YOLO_ROOT.as_posix()}/images/train
val:   {YOLO_ROOT.as_posix()}/images/val

nc: {len(CLASSES)}
names: {CLASSES}
"""
with open(data_yaml, "w") as f:
    f.write(yaml_text)
print("data.yaml written:", data_yaml)

# Final counts
train_imgs = len(list((IMG_TRAIN).glob("*.png"))) + len(list((IMG_TRAIN).glob("*.jpg")))
val_imgs = len(list((IMG_VAL).glob("*.png"))) + len(list((IMG_VAL).glob("*.jpg")))
print(f"Train images: {train_imgs}, Val images: {val_imgs}")
print("\nDone. Inspect the folders and data.yaml before training.")
