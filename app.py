import streamlit as st
import re
import pandas as pd
from PyPDF2 import PdfReader
import io
import base64

# ======================================================
# ✅ BACKGROUND FUNCTION
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
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

set_bg("background.png")

# ======================================================
# ✅ КОДОВЕ
# ======================================================
ALLOWED_CODES = [
    "27101991","27101981","27101983","27101987",
    "27101993","27101999","34031910","34039900",
    "34031980","38119000","38112100","38249992",
    "27101225","38140090"
]

# ======================================================
# ✅ UI FIXED
# ======================================================
st.title("📦 Logistics App")

menu = st.sidebar.selectbox("Suppliers", ["Castrol", "MOTUL"])

if "source_type" not in st.session_state:
    st.session_state["source_type"] = ""

col1, col2 = st.columns(2)

with col1:
    if st.button("PDF", use_container_width=True):
        st.session_state["source_type"] = "PDF"
        st.rerun()

with col2:
    if st.button("Excel", use_container_width=True):
        st.session_state["source_type"] = "Excel"
        st.rerun()

source_type = st.session_state["source_type"]

uploaded_files = None

if source_type:
    uploaded_files = st.file_uploader(
        "📂 Upload files",
        type=["pdf"] if source_type == "PDF" else ["xlsx", "xls"],
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
# ✅ MOTUL (РАБОТЕЩ)
# ======================================================
def parse_motul(text):

    rows = []
    lines = text.split("\n")

    for i, line in enumerate(lines):

        match = re.findall(r'(\d{1,4})\s+(\d{1,3}(?:\s\d{3})*,\d+)', line)

        if match:
            try:
                qty = float(match[0][0])
                weight = float(match[0][1].replace(" ", "").replace(",", "."))

                code = None
                for j in range(i, min(i + 6, len(lines))):
                    c = re.search(r'\b\d{8}\b', lines[j])
                    if c:
                        code = c.group(0)
                        break

                wid = 1
                for j in range(max(0, i - 8), i + 1):
                    l = lines[j].upper()

                    pack = re.search(r'(\d+)X(\d+)L', l)
                    single = re.search(r'(\d+)L', l)

                    if pack:
                        wid = float(pack.group(2))
                    elif single:
                        wid = float(single.group(1))

                    if "0.500L" in l:
                        wid = 0.5
                    elif "0.250L" in l:
                        wid = 0.25

                if code:
                    rows.append({
                        "Тарифен код": code,
                        "Количество": qty,
                        "wid": wid,
                        "kolichestvo": qty * wid,
                        "тегло": weight
                    })

            except:
                pass

    return pd.DataFrame(rows)

# ======================================================
# ✅ FINAL REPORT
# ======================================================
def build_final_report(df):

    df["wid"] = df["wid"].astype(float).round(3)

    df["ratio"] = df["тегло"] / df["kolichestvo"]
    df["correct_weight"] = df["kolichestvo"] * df["ratio"]

    grouped = df.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "correct_weight": "sum"
    })

    grouped = grouped.rename(columns={"correct_weight": "тегло"})

    rows = []

    for code, group in grouped.groupby("Тарифен код"):

        for _, r in group.iterrows():
            rows.append(r.to_dict())

        rows.append({
            "Тарифен код": str(code) + " -",
            "wid": "",
            "Количество": "",
            "kolichestvo": group["kolichestvo"].sum(),
            "тегло": group["тегло"].sum()
        })

        rows.append({
            "Тарифен код": "",
            "wid": "",
            "Количество": "",
            "kolichestvo": "",
            "тегло": ""
        })

    rows.append({
        "Тарифен код": "GRAND TOTAL",
        "wid": "",
        "Количество": "",
        "kolichestvo": grouped["kolichestvo"].sum(),
        "тегло": grouped["тегло"].sum()
    })

    return pd.DataFrame(rows)

# ======================================================
# ✅ PROCESS
# ======================================================
if uploaded_files and len(uploaded_files) > 0:

    all_data = []

    for file in uploaded_files:

        if source_type == "PDF":
            reader = PdfReader(file)
            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            if menu == "Castrol":
                df = parse_castrol(text)
            else:
                df = parse_motul(text)
        else:
            df = pd.read_excel(file)

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    final_df["Тарифен код"] = final_df["Тарифен код"].astype(str)
    final_df = final_df[final_df["Тарифен код"].isin(ALLOWED_CODES)]
    final_df = final_df[final_df["тегло"] > 0]

    report = build_final_report(final_df)

    st.subheader("📊 Финален отчет")
    st.dataframe(report)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report.to_excel(writer, index=False)

    st.download_button(
        "📥 Изтегли Excel",
        data=output.getvalue(),
        file_name="final_report.xlsx"
    )
