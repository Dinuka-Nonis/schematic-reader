# Vision-based Schematic Reader MVP

## Scope
- Focus: Combinational circuits (AND, OR, NOT, NAND, NOR, XOR) + basic sequential (flip-flops for simple state).
- Inputs: Clean Logisim-exported PNGs (limited to 5-20 gates for MVP; robust to minor rotations/noise via aug).
- Features: Image upload → detection (YOLO) → wire tracing → graph build (NetworkX) → simulation queries (robust parsing with regex/spaCy for "chatbot-like" feel).
- Exclusions: No analog, full sequential logic, or real-time hardware sim—post-MVP.

## Success Metrics
- Simulation Accuracy: 90%+ on test circuits vs. Logisim truths.
- Detection Robustness: 80%+ mAP on varied images (synthetics + augmented real).
- End-to-End: <10s processing on GPU; 85%+ connectivity F1.
- User Value: Demo feedback >70% "saves time vs. manual."