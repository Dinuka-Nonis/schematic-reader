# streamlit_app.py

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json

st.set_page_config(page_title="Circuit Canvas", layout="wide")

st.title("Circuit Schematic Canvas")

# -----------------------------
# Component Definitions
# -----------------------------
components = {
    "Resistor": {"width": 60, "height": 20, "color": "orange"},
    "LED": {"width": 40, "height": 20, "color": "green"},
    "Battery": {"width": 50, "height": 30, "color": "red"},
    "Switch": {"width": 50, "height": 20, "color": "blue"},
    "Ground": {"width": 40, "height": 20, "color": "brown"}
}

# Sidebar to add components
st.sidebar.header("Add Component")
comp_type = st.sidebar.selectbox("Component Type", list(components.keys()))
comp_label = st.sidebar.text_input("Label (e.g., R1, LED1)", "C1")
add_button = st.sidebar.button("Add Component")

# Store components in session state
if "placed_components" not in st.session_state:
    st.session_state.placed_components = []

# Add component to canvas
if add_button:
    st.session_state.placed_components.append({
        "type": comp_type,
        "label": comp_label,
        "x": 50,
        "y": 50,
        "width": components[comp_type]["width"],
        "height": components[comp_type]["height"],
        "color": components[comp_type]["color"]
    })

# -----------------------------
# Draw Canvas
# -----------------------------
canvas_result = st_canvas(
    fill_color="",
    stroke_width=2,
    stroke_color="#000",
    background_color="#fff",
    height=600,
    width=800,
    drawing_mode="rect",
    key="canvas"
)

# Display placed components on canvas
for comp in st.session_state.placed_components:
    st.write(f"{comp['label']} ({comp['type']}) at x:{comp['x']} y:{comp['y']}")

# -----------------------------
# Export JSON
# -----------------------------
if st.button("Export Netlist JSON"):
    netlist = {"components": st.session_state.placed_components}
    st.download_button(
        "Download JSON",
        data=json.dumps(netlist, indent=2),
        file_name="netlist.json",
        mime="application/json"
    )
