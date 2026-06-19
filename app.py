import streamlit as st
import re
import pandas as pd
from PyPDF2 import PdfReader
import io
import base64

# ======================================================
# ✅ BACKGROUND
# ======================================================
def set_bg(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

# ✅ LOGIN
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        set_bg("background_login.png")

        st.markdown("<h1 style='text-align:center;color:white;'>🔐 Вход</h1>", unsafe_allow_html=True)

        username = st.text_input("Потребител")
        password = st.text_input("Парола", type="password")

        if st.button("Вход"):
            if username == "mitnica" and password == "Intercars2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("❌ Грешно име или парола")

        return False
    return True

if not check_login():
    st.stop()

set_bg("background.png")

# ======================================================
# ✅ MENU
# ======================================================
menu = st.sidebar.selectbox("Suppliers", ["CASTROL", "MOTUL", "NESTE", "GASOLINE"])

source_type = st.selectbox("Source", ["PDF", "Excel"])

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf"] if source_type == "PDF" else ["xlsx"],
    accept_multiple_files=True
)

# ======================================================
# ✅ CODES
# ======================================================
ALLOWED_CODES = [
    "27101991","27101981","27101983","27101987",
    "27101993","27101999","34031910","34039900",
    "34031980","38119000","38112100","38249992",
    "27101225","38140090"
]

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
# ✅ MOTUL
# ======================================================
def parse_motul(text):
    rows = []
    lines = text.split("\n")

    current_qty = 0
    current_weight = 0
    liters_per_unit = 0
    units_in_box = 1

    for line in lines:

        match = re.search(r"\d+\s+\d+\s+(\d+)", line)
        if match:
            current_qty = int(match.group(1))

        multi = re.findall(r"(\d+)X([\d\.,]+)", line)
        if multi:
            units_in_box = int(multi[-1][0])
            liters_per_unit = float(multi[-1][1].replace(",", "."))

        weight_match = re.search(r"([\d\s,]+)\s+([\d\s,]+)", line)
        if weight_match:
            try:
                current_weight = float(weight_match.group(1).replace(",", "."))
            except:
                pass

        if "HS code" in line:
            code = re.search(r"(\d+)", line)

            if code:
                code_value = code.group(1)[:8]

                rows.append({
                    "Тарифен код": code_value,
                    "Количество": current_qty,
                    "wid": liters_per_unit,
                    "kolichestvo": current_qty * liters_per_unit,
                    "тегло": current_weight
                })

                current_qty = 0
                current_weight = 0

    return pd.DataFrame(rows)

# ======================================================
# ✅ GASOLINE
# ======================================================
def parse_gasoline(text):

    rows = []
    lines = text.split("\n")

    current_liters = 0
    current_weight = 0
    current_wid = 1

    for line in lines:

        liters_match = re.search(r"([\d\.,]+)\s+Liter", line, re.IGNORECASE)
        if liters_match:
            current_liters = float(liters_match.group(1).replace(",", ".").replace(".", ""))

        weight_match = re.search(r"([\d\.,]+)\s*kg", line, re.IGNORECASE)
        if weight_match:
            current_weight = float(weight_match.group(1).replace(",", ".").replace(".", ""))

        multi = re.search(r"(\d+)x(\d+)", line, re.IGNORECASE)
        if multi:
            current_wid = float(multi.group(2))

        if "Zolltarifnummer" in line:
            code_match = re.search(r"(\d+)", line)

            if code_match and current_liters > 0:
                code_value = code_match.group(1)[:8]

                weight_for_row = current_weight
                if weight_for_row == 0:
                    weight_for_row = current_liters * 0.85

                rows.append({
                    "Тарифен код": code_value,
                    "Количество": current_liters / current_wid,
                    "wid": current_wid,
                    "kolichestvo": current_liters,
                    "тегло": weight_for_row
                })

                current_liters = 0
                current_weight = 0
                current_wid = 1

    return pd.DataFrame(rows)

# ======================================================
# ✅ NESTE
# ======================================================
def parse_neste_excel(file):
    df = pd.read_excel(file)
    df = df.rename(columns={
        "Commodity code": "Тарифен код",
        "Volume": "kolichestvo",
        "Net Weight": "тегло"
    })
    return df

# ======================================================
# ✅ REPORT
# ======================================================
def build_final_report(df):
    return df.groupby(["Тарифен код"], as_index=False).sum()

# ======================================================
# ✅ PROCESS
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        if source_type == "PDF":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            if menu == "CASTROL":
                df = parse_castrol(text)
            elif menu == "MOTUL":
                df = parse_motul(text)
            elif menu == "GASOLINE":
                df = parse_gasoline(text)

        else:
            df = parse_neste_excel(file)

        if isinstance(df, pd.DataFrame) and not df.empty:
            all_data.append(df)

    if not all_data:
        st.warning("⚠️ Няма данни")
        st.stop()

    final_df = pd.concat(all_data, ignore_index=True)

    final_df["Тарифен код"] = final_df["Тарифен код"].astype(str).str[:8]
    final_df = final_df[final_df["Тарифен код"].isin(ALLOWED_CODES)]

    if menu in ["MOTUL", "NESTE"]:
        final_df = final_df[final_df["тегло"] > 0]

    report = build_final_report(final_df)

    st.subheader("📊 Финален отчет")
    st.dataframe(report)

    output = io.BytesIO()
    report.to_excel(output, index=False)

    st.download_button("📥 Изтегли Excel", data=output.getvalue(), file_name="report.xlsx")
