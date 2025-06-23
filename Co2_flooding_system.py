import streamlit as st
from fpdf import FPDF
import base64
import tempfile

st.set_page_config(page_title="CO₂ Flooding System Calculator", layout="centered")
st.title("💨 CO₂ Flooding System Calculator (NFPA 12 Based)")

# --- Input Section ---
st.header("Room Details")
length = st.number_input("Length of the room (m):", min_value=0.0, format="%.2f")
width = st.number_input("Width of the room (m):", min_value=0.0, format="%.2f")
height = st.number_input("Height of the room (m):", min_value=0.0, format="%.2f")

st.header("Calculation Factors")
material_conversion_factor = st.number_input("Material Conversion Factor (default = 1.6):", value=1.6, format="%.2f")
flooding_factor = st.number_input("Flooding Factor (default = 0.93):", value=0.93, format="%.2f")

st.sidebar.markdown(
    """
    <style>
    .bottom-footer {
        position: fixed;
        bottom: 15px;
        left: 0;
        width: 18rem;
        text-align: center;
        font-size: 13px;
        color: #888;
    }
    </style>
    <div class="bottom-footer">Made by <b>MANMOHAN SINGH RAWAT</b></div>
    """,
    unsafe_allow_html=True
)


# --- Calculation ---
if st.button("Calculate CO₂ Required"):
    volume = length * width * height
    co2_required = volume * flooding_factor * material_conversion_factor

    st.success(f"✅ CO₂ required: **{co2_required:.2f} kg**")
    st.info(f"📐 Volume: {volume:.2f} m³")

    # --- PDF Report Creation ---
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(200, 10, "CO2 Flooding System Report", ln=True, align="C")


        def chapter_title(self, title):
            self.set_font("Arial", "B", 12)
            self.ln(10)
            self.cell(0, 10, title, ln=True)

        def chapter_body(self, text):
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, text)

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Input Parameters")
    pdf.chapter_body(f"""
    Length: {length} m
    Width: {width} m
    Height: {height} m
    Volume: {volume:.2f} m³

    Material Conversion Factor: {material_conversion_factor}
    Flooding Factor: {flooding_factor}
    """)

    pdf.chapter_title("Calculation Result")
    pdf.chapter_body(f"CO2 Required: {co2_required:.2f} kg")  # <-- plain "CO2"

 
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf_output = tmpfile.name
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as f:
            b64_pdf = base64.b64encode(f.read()).decode("utf-8")
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="co2_flooding_report.pdf">📄 Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)
            

# --- NFPA 12 Reference Chart ---
with st.sidebar:
    st.markdown("### 📘 NFPA 12 Reference")
    st.markdown("""
**Typical CO₂ Flooding Factors (kg/m³):**

| Hazard Type                        | Factor |
|-----------------------------------|--------|
| Surface Fire (Total Flooding)     | 0.93   |
| Deep-Seated Fire (Total Flooding) | 1.10   |
| Local Application (Surface Only)  | 0.67   |
| Very High Hazard Areas            | 1.20   |

> 🔹 *Refer to the latest NFPA 12 standard for final values.*
""")

