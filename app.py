import streamlit as st
import re
import pandas as pd
from PyPDF2 import PdfReader

# ======================================================
# ✅ BASIC UI
# ======================================================
st.title("📦 CustomsFlow - Parser")

menu = st.selectbox("Supplier", ["Castrol", "MOTUL"])
uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf"],
    accept_multiple_files=True
)

# ======================================================
# ✅ CASTROL
# ======================================================
def parse_castrol(text):

    rows = []
    lines = text.split("\n")
    current_liters = 0

    for line in lines:

        multi = re.search(r"(\d+)X(\d+)L", line)
        single = re.search(r"(\d+)L", line)

        if multi:
            current_liters = int(multi.group(1)) * int(multi.group(2))
        elif single:
            current_liters = int(single.group(1))

        if "Cod Vamal" in line:
            try:
                code = re.search(r"Cod Vamal:(\d+)", line).group(1)
                qty = int(re.search(r"ST\s*(\d+)", line).group(1))

                rows.append({
                    "Тарифен код": code,
                    "Количество": qty,
                    "wid": current_liters,
                    "kolichestvo": qty * current_liters,
                    "тегло": 0
                })
            except:
                pass

    return pd.DataFrame(rows)

# ======================================================
# ✅ MOTUL (FINAL 100% WORKING)
# ======================================================
def parse_motul(text):

    rows = []
    lines = text.split("\n")

    current_qty = 0
    current_weight = 0
    liters_per_unit = 0
    units_in_box = 1

    for line in lines:

        # ✅ Quantity
        match = re.search(r"\d+\s+\d+\s+(\d+)\s+[\d,\.]+\s+[\d,\.]+", line)
        if match:
            try:
                current_qty = int(match.group(1))
            except:
                pass

        # ✅ Packaging
        multi = re.findall(r"(\d+)X([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)
        single = re.search(r"([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)

        if multi:
            units_in_box = int(multi[-1][0])
            liters_per_unit = float(multi[-1][1].replace(",", "."))
        elif single:
            units_in_box = 1
            liters_per_unit = float(single.group(1).replace(",", "."))

        # ✅ Weight (NET ONLY ✅)
        weights = re.findall(r"\d{1,3}(?:\s\d{3})*,\d+", line)

        if weights:
            try:
                values = [
                    float(w.replace(" ", "").replace(",", "."))
                    for w in weights
                ]

                if len(values) >= 2:
                    current_weight = min(values[-2:])

            except:
                pass

        # ✅ HS CODE
        if "HS code" in line:
            code = re.search(r"HS code\s*:\s*(\d+)", line)

            if code:
                code_value = code.group(1)[:8]

                if current_qty * units_in_box * liters_per_unit > 100000:
                    real_qty = current_qty
                else:
                    if units_in_box > 1 and liters_per_unit <= 5:
                        real_qty = current_qty * units_in_box
                    else:
                        real_qty = current_qty

                rows.append({
                    "Тарифен код": code_value,
                    "Количество": real_qty,
                    "wid": liters_per_unit,
                    "kolichestvo": real_qty * liters_per_unit,
                    "тегло": current_weight
                })

                # RESET
                current_qty = 0
                current_weight = 0
                liters_per_unit = 0
                units_in_box = 1

    return pd.DataFrame(rows)

# ======================================================
# ✅ PROCESS
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        if menu == "Castrol":
            df = parse_castrol(text)
        else:
            df = parse_motul(text)

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    st.subheader("📊 Result")
    st.dataframe(final_df)
