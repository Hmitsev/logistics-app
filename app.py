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
# ✅ FINAL UI (RESET + PERFECT ORDER)
# ======================================================

st.markdown("""
<style>
.source-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

/* ✅ Add file малък */
.add-file {
    display:inline-block;
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 4px 10px;
    color: white;
    font-size: 16px;
    margin-bottom: 6px;
}

/* ✅ маха текста от default button */
button[data-testid="baseButton-secondary"] p {
    opacity: 0;
}
</style>
""", unsafe_allow_html=True)


# ✅ SIDEBAR
menu = st.sidebar.selectbox("Suppliers", ["CASTROL", "MOTUL","NESTE","VALVOLINE"])

# ✅ RESET при смяна на supplier
if "prev_supplier" not in st.session_state:
    st.session_state["prev_supplier"] = menu

if st.session_state["prev_supplier"] != menu:
    st.session_state["source_type"] = ""
    st.session_state["prev_supplier"] = menu


# ✅ заглавие
st.markdown('<div class="source-title">👇 Choose Source</div>', unsafe_allow_html=True)


# ✅ STATE
if "source_type" not in st.session_state:
    st.session_state["source_type"] = ""


# ✅ бутони
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


# ✅ цветове + overlay
if source_type == "PDF":
    pdf_color = "#ff3b3b"
    excel_color = "#444"
    pdf_overlay = "<span style='color:#ff3b3b;'>You chose: PDF</span>"
    excel_overlay = "<span style='color:white;'>Excel</span>"

elif source_type == "Excel":
    pdf_color = "#444"
    excel_color = "#36c165"
    pdf_overlay = "<span style='color:white;'>PDF</span>"
    excel_overlay = "<span style='color:#36c165;'>You chose: Excel</span>"

else:
    pdf_color = "#444"
    excel_color = "#444"
    pdf_overlay = "<span style='color:white;'>PDF</span>"
    excel_overlay = "<span style='color:white;'>Excel</span>"


# ✅ стил на бутоните
st.markdown(f"""
<style>
div[data-testid="column"]:nth-of-type(1) button {{
    background-color: {pdf_color};
    height: 60px;
    border-radius: 12px;
}}

div[data-testid="column"]:nth-of-type(2) button {{
    background-color: {excel_color};
    height: 60px;
    border-radius: 12px;
}}
</style>
""", unsafe_allow_html=True)


# ✅ overlay текст
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="
        margin-top:-65px;
        display:flex;
        justify-content:flex-end;
        padding-right:20px;
        pointer-events:none;
    ">
        {pdf_overlay}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        margin-top:-65px;
        display:flex;
        justify-content:flex-end;
        padding-right:20px;
        pointer-events:none;
    ">
        {excel_overlay}
    </div>
    """, unsafe_allow_html=True)


# ✅ ✅ ПРАВИЛЕН РЕД (FIX)
st.markdown("<div class='add-file'>Add file</div>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "",
    type=["pdf"] if source_type == "PDF" else ["xlsx", "xls"],
    accept_multiple_files=True
)
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
# ✅ MOTUL (FINAL REAL WORKING)
# ======================================================
def parse_motul(text):

    rows = []
    lines = text.split("\n")

    current_qty = 0
    current_weight = 0
    liters_per_unit = 0
    units_in_box = 1

    for line in lines:

        # ✅ КОЛИЧЕСТВО
        match = re.search(r"\d+\s+\d+\s+(\d+)\s+[\d,\.]+\s+[\d,\.]+", line)
        if match:
            try:
                current_qty = int(match.group(1))
            except:
                pass

        # ✅ РАЗФАСОВКА
        multi = re.findall(r"(\d+)X([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)
        single = re.search(r"([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)

        if multi:
            units_in_box = int(multi[-1][0])
            liters_per_unit = float(multi[-1][1].replace(",", "."))
        elif single:
            units_in_box = 1
            liters_per_unit = float(single.group(1).replace(",", "."))

        # ✅ ТЕГЛО
        weights = re.findall(r"\d{1,3}(?:\s\d{3})*,\d+", line)

        qty_match = re.search(r"\d+\s+\d+\s+(\d+)\s+[\d,\.]+\s+[\d,\.]+", line)

        if weights and qty_match:
            try:
                values = [
                    float(w.replace(" ", "").replace(",", "."))
                    for w in weights
                ]

                if len(values) >= 2:
                    current_weight = min(values[-2:])

            except:
                pass

        # ✅ HS CODE (само веднъж!)
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

                # ✅ RESET
                current_qty = 0
                current_weight = 0
                liters_per_unit = 0
                units_in_box = 1

    return pd.DataFrame(rows)


# ======================================================
# ✅ NESTE (EXCEL ONLY ✅)  ✅ ТУК Е ФИКСЪТ
# ======================================================
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

    df = df.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df

# ======================================================
# ✅ VALVOLINE (EXCEL ONLY ✅)
# ======================================================
def parse_valvoline_excel(file):

    import pandas as pd
    import re

    xls = pd.ExcelFile(file)

    # ✅ намираме PL sheet
    sheet_name = None
    for s in xls.sheet_names:
        if "PL" in s.upper():
            sheet_name = s
            break

    if not sheet_name:
        st.error("❌ Не е намерен PL sheet")
        st.stop()

    # ======================================================
    # ✅ НАМИРАМЕ HEADER ROW АВТОМАТИЧНО
    # ======================================================
    raw = xls.parse(sheet_name, header=None)

    header_row = None

    for i, row in raw.iterrows():
        row_text = " ".join([str(x) for x in row])

        if "Tariff" in row_text and "Qty" in row_text:
            header_row = i
            break

    if header_row is None:
        st.error("❌ Не е намерен header ред")
        st.stop()

    # ✅ четем пак със правилния header
    df = xls.parse(sheet_name, header=header_row)

    # ✅ чистим колоните
    df.columns = df.columns.astype(str).str.strip().str.replace("\n", " ")

    # ======================================================
    # ✅ COLUMN MAP
    # ======================================================
    column_map = {}

    for col in df.columns:
        c = col.lower()

        if "tariff" in c:
            column_map[col] = "code"

        elif "pack" in c:
            column_map[col] = "pack"

        elif "qty" in c:
            column_map[col] = "qty"

        elif "net" in c:
            column_map[col] = "weight"

    df = df.rename(columns=column_map)

    required = ["code", "pack", "qty", "weight"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"❌ Липсват колони VALVOLINE: {missing}")
        st.write(df.columns)
        st.stop()

    df = df.dropna(subset=["code"])

    rows = []

    for _, r in df.iterrows():

        code = str(r["code"])[:8]
        qty = float(r["qty"])
        weight = float(r["weight"])
        pack = str(r["pack"])

        wid = 1

        # ✅ regex
        multi = re.search(r"(\d+)\s*x\s*(\d+)\s*L", pack, re.I)
        single = re.search(r"(\d+)\s*L", pack, re.I)
        grams = re.search(r"(\d+)\s*g", pack, re.I)

        # ======================================================
        # ✅ MULTI PACK (пример: 4x5L)
        # ======================================================
        if multi:
            units = int(multi.group(1))
            liters = int(multi.group(2))

            wid = liters

            # ✅ това винаги са кутии
            kolichestvo = qty * liters
            real_qty = qty


        # ======================================================
        # ✅ SINGLE L (пример: 20L, 208L)
        # ======================================================
        elif single:
            wid = int(single.group(1))

            # ✅ това при VALVOLINE са вече литри
            kolichestvo = qty
            real_qty = qty / wid


        # ======================================================
        # ✅ GRAMS (грес)
        # ======================================================
        elif grams:
            wid = 1
            kolichestvo = qty
            real_qty = qty


        # ======================================================
        # ✅ fallback
        # ======================================================
        else:
            wid = 1
            kolichestvo = qty
            real_qty = qty


        rows.append({
            "Тарифен код": code,
            "Количество": real_qty,
            "wid": wid,
            "kolichestvo": kolichestvo,
            "тегло": weight
        })

    df = pd.DataFrame(rows)

    df = df.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df
