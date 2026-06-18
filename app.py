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
# ✅ LOGOUT BUTTON (FIXED TOP RIGHT)
# ======================================================

logout_col1, logout_col2, logout_col3 = st.columns([8,1,1])

with logout_col3:
    if st.button("🚪", help="Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

st.markdown("""
<style>
div[data-testid="column"]:nth-of-type(3) {
    position: fixed;
    top: 4px;
    right: 45px;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)


# ======================================================
# ✅ LOGIN SYSTEM (FINAL INLINE LOGO WORKING)
# ======================================================
def check_login():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:

        # ✅ background
        set_bg("background_login.png")

        # ✅ HEADER В 1 РЕД (чрез columns, но правилно оразмерени)
        col1, col2 = st.columns([4,1])

        with col1:
            st.markdown("""
            <div style="
                text-align:right;
                font-size:32px;
                font-weight:900;
                color:white;
                white-space:nowrap;
            ">
                CustomsFlow
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.image("Screenshot 2026-06-18 093459.png", width=60)

        # ✅ леко spacing
        st.markdown("<br>", unsafe_allow_html=True)

        # ✅ Login title
        st.markdown(
            "<h1 style='text-align:center; color:white;'>🔐 Вход</h1>",
            unsafe_allow_html=True
        )

        # ✅ Inputs
        username = st.text_input("Потребител")
        password = st.text_input("Парола", type="password")

        # ✅ Button
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

# ✅ main background
set_bg("background.png")
# ======================================================
# ✅ ULTRA GLASS SIDEBAR (PRO VERSION)
# ======================================================

st.markdown("""
<style>

/* ✅ Sidebar container */
section[data-testid="stSidebar"] {
    background: transparent !important;
}

/* ✅ GLASS EFFECT */
section[data-testid="stSidebar"] > div {
    background: rgba(0,0,0,0.01) !important;  /* почти прозрачно */

    backdrop-filter: blur(18px) saturate(140%);
    -webkit-backdrop-filter: blur(18px) saturate(140%);

    border-right: 4px solid rgba(255,255,255,0.7);  /* силен метален борд */

    /* ✅ вътрешен glow */
    box-shadow:
        inset 0 0 10px rgba(255,255,255,0.05),
        0 0 20px rgba(255,255,255,0.1);
}


/* ✅ текст */
section[data-testid="stSidebar"] * {
    color: white !important;
}


/* ✅ SELECT BOX */
div[data-baseweb="select"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(8px);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.25);

    cursor: pointer !important;
}


/* ✅ hover ефект (много фин) */
div[data-baseweb="select"]:hover {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 0 8px rgba(255,255,255,0.2);
}


/* ✅ pointer fix */
div[data-baseweb="select"] * {
    cursor: inherit !important;
}

</style>
""", unsafe_allow_html=True)

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

    current_qty = 0
    current_weight = 0
    liters_per_unit = 0
    units_in_box = 1

    for line in lines:

        # ✅ количество
        match = re.search(r"\d+\s+\d+\s+(\d+)\s+[\d,\.]+\s+[\d,\.]+", line)
        if match:
            try:
                current_qty = int(match.group(1))
            except:
                pass

        # ✅ тегло
        weights = re.findall(r"\d+,\d+", line)
        if weights:
            try:
                current_weight = float(weights[0].replace(",", "."))
            except:
                pass

        # ✅ multipack
        multi = re.findall(r"(\d+)X([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)
        single = re.search(r"([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)

        if multi:
            units_in_box = int(multi[-1][0])
            liters_per_unit = float(multi[-1][1].replace(",", "."))
        elif single:
            units_in_box = 1
            liters_per_unit = float(single.group(1).replace(",", "."))

        # ✅ код
        if "HS code" in line:
            code = re.search(r"HS code\s*:\s*(\d+)", line)

            if code:
                code_value = code.group(1)[:8]

                # ✅ логика от вчера (КЛЮЧОВА)
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
    df.columns = df.columns.str.strip()

    # ✅ COLUMN MAP (FIX)
    column_map = {}

    for col in df.columns:
        c = col.lower()

        if "comm" in c or "code" in c:
            column_map[col] = "Commodity code"

        elif "pack" in c:
            column_map[col] = "Type of packaging"

        elif "delivery quantity" in c or "qty" in c or "quantity" in c:
            column_map[col] = "Delivery quantity"

        elif "volume" in c:
            column_map[col] = "Volume"

        elif "net weight" in c or "weight" in c:
            column_map[col] = "Net Weight"

    df = df.rename(columns=column_map)

    # ✅ DEBUG
    st.write("DEBUG columns after rename:", df.columns.tolist())

    # ✅ защита
    required_cols = [
        "Commodity code",
        "Type of packaging",
        "Delivery quantity",
        "Volume",
        "Net Weight"
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(f"❌ Липсват колони: {missing}")
        st.stop()

    # ✅ правим структура като PDF
    df = df.groupby(
        ["Commodity code", "Type of packaging"],
        as_index=False
    ).agg({
        "Delivery quantity": "sum",
        "Volume": "sum",
        "Net Weight": "sum"
    })

    df = df.rename(columns={
        "Commodity code": "Тарифен код",
        "Type of packaging": "wid",
        "Delivery quantity": "Количество",
        "Volume": "kolichestvo",
        "Net Weight": "тегло"
    })

