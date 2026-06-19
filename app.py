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

# ======================================================
# ✅ LOGIN
# ======================================================
def check_login():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:

        set_bg("background_login.png")

        col1, col2 = st.columns([4,1])

        with col1:
            st.markdown("<h2 style='text-align:right;color:white;'>CustomsFlow</h2>", unsafe_allow_html=True)

        with col2:
            st.image("Screenshot 2026-06-18 093459.png", width=60)

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
# ✅ SIDEBAR
# ======================================================
menu = st.sidebar.selectbox("Suppliers", ["CASTROL", "MOTUL","NESTE"])

# ======================================================
# ✅ FILE UPLOAD
# ======================================================
st.markdown("### 👇 Choose Source")

col1, col2 = st.columns(2)

if "source_type" not in st.session_state:
    st.session_state["source_type"] = ""

with col1:
    if st.button("PDF"):
        st.session_state["source_type"] = "PDF"

with col2:
    if st.button("Excel"):
        st.session_state["source_type"] = "Excel"

source_type = st.session_state["source_type"]

uploaded_files = st.file_uploader(
    "",
    type=["pdf"] if source_type == "PDF" else ["xlsx", "xls"],
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
# ✅ PARSERS
# ======================================================
def parse_castrol(text):
    rows = []
    for line in text.split("\n"):
        if "Cod Vamal" in line:
            try:
                code = re.search(r"(\d+)", line).group(1)
                rows.append({
                    "Тарифен код": code,
                    "Количество": 1,
                    "wid": 1,
                    "kolichestvo": 1,
                    "тегло": 0
                })
            except:
                pass
    return pd.DataFrame(rows)

def parse_motul(text):
    return pd.DataFrame([])  # остава както е за момента

def parse_neste_excel(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Commodity code": "Тарифен код",
        "Type of packaging": "wid",
        "Delivery quantity": "Количество",
        "Volume": "kolichestvo",
        "Net Weight": "тегло"
    })

    df = df.dropna(subset=["Тарифен код"])

    return df

# ======================================================
# ✅ REPORT
# ======================================================
def build_final_report(df):
    return df.groupby("Тарифен код").sum(numeric_only=True).reset_index()

# ======================================================
# ✅ PROCESS
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        df = None

        if menu == "NESTE":
            df = parse_neste_excel(file)

        elif source_type == "PDF":

            reader = PdfReader(file)
            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            if menu == "CASTROL":
                df = parse_castrol(text)
            else:
                df = parse_motul(text)

        else:
            df = pd.read_excel(file)

        # ✅ SAFE APPEND
        if isinstance(df, pd.DataFrame) and not df.empty:
            all_data.append(df)

    if not all_data:
        st.warning("⚠️ Няма данни")
        st.stop()

    final_df = pd.concat(all_data, ignore_index=True)

    final_df["Тарифен код"] = final_df["Тарифен код"].astype(str)
    final_df = final_df[final_df["Тарифен код"].isin(ALLOWED_CODES)]

    report = build_final_report(final_df)

    st.dataframe(report)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report.to_excel(writer, index=False)

    st.download_button(
        "📥 Изтегли Excel",
        data=output.getvalue(),
        file_name="report.xlsx"
    )

    # ======================================================
# ✅ NESTE (EXCEL ONLY ✅)
# ======================================================
def parse_neste_excel(file):

    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    # ✅ rename
    df = df.rename(columns={
        "Commodity code": "Тарифен код",
        "Type of packaging": "wid",
        "Delivery quantity": "Количество",
        "Volume": "kolichestvo",
        "Net Weight": "тегло"
    })

    # ✅ махаме празни / грешни редове
    df = df.dropna(subset=["Тарифен код"])

    # ✅ group
    df = df.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df
