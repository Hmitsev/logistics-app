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
    font-size: 23px;
    font-weight: 800;
    color: #ff8c00;
    text-shadow: 0 0 8px rgba(255,140,0,0.5);

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
menu = st.sidebar.selectbox("Suppliers", ["CASTROL & NESTE", "MOTUL", "FLUKAR", "GASOLIN", "VALVOLINE", "ORLEN", "Chempioil (FANFARO)", "FUCHS", "FEBI", "ELROMI RONAX","NISTA", "AMTRA" , "AUTO MEGA" ,"EMINIA" ,"Brehman"])
# ✅ статичен списък (като таблица в sidebar)
st.sidebar.markdown("### 📋 Suppliers & File type")

suppliers_table = [
    ("FLUKAR", "Excel"),
    ("ELROMI RONAX", "Excel"),
    ("VALVOLINE", "Excel"),
    ("ORLEN", "Excel"),
    ("Chempioil (FANFARO)", "Excel"),
    ("AMTRA", "Excel"),
    ("FUCHS", "PDF"),
    ("CASTROL", "Excel"),
    ("MOTUL", "PDF"),
    ("NESTE", "Excel"),
    ("Gasoline", "PDF"),
    ("FEBI", "PDF"),
    ("NISTA", "Excel+NewSheet"),
    ("AUTO MEGA", "Excel"),
    ("EMINIA", "Excel"),
    ("Brehman", "Excel"),
]

# ✅ обръщаме реда (както искаш)
suppliers_table = suppliers_table[::-1]

# ✅ правим DataFrame за визуализация
df_suppliers = pd.DataFrame(suppliers_table, columns=["Supplier", "File"])

st.sidebar.dataframe(df_suppliers, use_container_width=True, height=650)
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
    "27101225","38140090","38249996"
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
# ✅ CASTROL EXCEL
# ======================================================
def parse_castrol_excel(file):

    df = pd.read_excel(file)

    rows = []

    for _, row in df.iterrows():

        try:

            code = str(
                row["Commodity code"]
            )

            code = re.sub(
                r"\D",
                "",
                code
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            qty = pd.to_numeric(
                row["Delivery quantity"],
                errors="coerce"
            )

            volume = pd.to_numeric(
                row["Volume"],
                errors="coerce"
            )

            net_weight = pd.to_numeric(
                row["Net Weight"],
                errors="coerce"
            )

            wid = pd.to_numeric(
                row["Type of packaging"],
                errors="coerce"
            )

            if pd.isna(qty):
                continue

            if pd.isna(volume):
                continue

            if pd.isna(net_weight):
                continue

            if pd.isna(wid):
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,
                "kolichestvo": volume,
                "тегло": net_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ CASTROL Excel parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
    
# ======================================================
# ✅ NISTA (ROW PARSER ✅ за Lieferschein)
# ======================================================
def parse_nista_excel(file):

    df = pd.read_excel(file, header=None)

    rows = []
    VALID_WID = [1, 4, 5,4.5, 2, 0.300, 0.250, 0.200, 0.500, 30, 40, 80, 20, 60, 200, 210, 208, ]

    for i in range(len(df)):

        row = df.iloc[i]

        try:
            row_text = " ".join([str(x) for x in row if pd.notna(x)])

            # ✅ търсим код
            code_match = re.search(r"27[\d\s]{6,}", row_text)
            if not code_match:
                continue

            digits = re.sub(r"\D", "", code_match.group(0))
            if len(digits) < 8:
                continue

            code = digits[:8]

            if code not in ALLOWED_CODES:
                continue

            # ✅ търсим количество (liter)
            menge_match = re.search(r"(\d+)\s*liter", row_text.lower())
            if not menge_match:
                continue

            menge = float(menge_match.group(1))

            # ✅ wid (12x1l, 3x5l...)
            wid_match = re.search(r"(\d+)x(\d+)l", row_text.lower())

            if wid_match:
                wid = float(wid_match.group(2))
            else:
                single = re.search(r"(\d+)l", row_text.lower())
                if not single:
                    continue
                wid = float(single.group(1))

            if wid not in VALID_WID:
                continue

            # ✅ тегло (последното число)
            weight = None
            for cell in reversed(row):
                try:
                    val = float(str(cell).replace(",", "."))
                    if val > 10:
                        weight = val
                        break
                except:
                    continue

            if not weight:
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": int(round(menge / wid)),
                "wid": wid,
                "kolichestvo": menge,
                "тегло": weight
            })

        except:
            continue

    if not rows:
        st.error("❌ NISTA parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
# ======================================================
# ✅ ORLEN (EXCEL)
# ======================================================
def parse_orlen_excel(file):

    df = pd.read_excel(file)

    df.columns = df.columns.astype(str).str.strip()

    rename_map = {}

    for col in df.columns:
        c = col.lower()

        if "code cn" in c:
            rename_map[col] = "Тарифен код"

        elif c == "qty":
            rename_map[col] = "Количество"

        elif "net weight" in c:
            rename_map[col] = "тегло"

        elif "material" in c:
            rename_map[col] = "material"

    df = df.rename(columns=rename_map)

    required = [
        "Тарифен код",
        "Количество",
        "тегло",
        "material"
    ]

    for col in required:
        if col not in df.columns:
            st.error(f"❌ ORLEN: липсва колона {col}")
            return pd.DataFrame()

    # ✅ само позволените кодове
    df["Тарифен код"] = (
        df["Тарифен код"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
        .str[:8]
    )

    df = df[df["Тарифен код"].isin(ALLOWED_CODES)]

    # ==================================================
    # ✅ извличане на разфасовка от Material
    # ==================================================
    def extract_wid(material):

        txt = str(material).upper().replace(",", ".")

        # 20L, 205L, 4.5L, 0.6L и т.н.
        m = re.search(r'(\d+(?:\.\d+)?)\s*L\b', txt)
        if m:
            return float(m.group(1))

        # 17KG, 9KG, 4.5KG...
        m = re.search(r'(\d+(?:\.\d+)?)\s*KG\b', txt)
        if m:
            return float(m.group(1))

        # 800G, 400G...
        m = re.search(r'(\d+(?:\.\d+)?)\s*G\b', txt)
        if m:
            return float(m.group(1)) / 1000

        return None

    df["wid"] = df["material"].apply(extract_wid)

    df = df[df["wid"].notna()]

    # ✅ числа
    df["Количество"] = pd.to_numeric(
        df["Количество"],
        errors="coerce"
    )

    df["тегло"] = pd.to_numeric(
        df["тегло"],
        errors="coerce"
    )

    # ✅ Qty × wid
    df["kolichestvo"] = (
        df["Количество"] * df["wid"]
    )

    df = df.dropna(
        subset=[
            "Тарифен код",
            "Количество",
            "wid",
            "тегло"
        ]
    )

    # ✅ групиране
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
# ✅ MOTUL (FINAL REAL WORKING + FILTER ✅)
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
        weight_match = re.search(
            r"\d+\s+\d+\s+(\d+)\s+([\d\s,]+)\s+([\d\s,]+)",
            line
        )

        if weight_match:
            try:
                net_weight = float(
                    weight_match.group(2).replace(" ", "").replace(",", ".")
                )

                if net_weight < 100000:
                    current_weight = net_weight
            except:
                pass

        # ✅ HS CODE (само веднъж!)
        if "HS code" in line:
            code = re.search(r"HS code\s*:\s*(\d+)", line)

            if code:
                code_value = code.group(1)[:8]

                # ✅ ✅ ✅ ФИЛТЪР ПО ALLOWED_CODES
                if code_value not in ALLOWED_CODES:
                    continue

                # ✅ ЛОГИКА ЗА КОЛИЧЕСТВО
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
                    "kolichestvo": round(real_qty * liters_per_unit, 3),
                    "тегло": round(current_weight, 3)
                })

                # ✅ RESET
                current_qty = 0
                current_weight = 0
                liters_per_unit = 0
                units_in_box = 1

    return pd.DataFrame(rows)
# ======================================================
# ✅ AUTO MEGA FINAL
# ======================================================
def parse_auto_mega_excel(file):

    raw = pd.read_excel(file, header=None)

    header_row = None

    for i in range(len(raw)):

        row_text = " ".join(
            str(x)
            for x in raw.iloc[i]
            if pd.notna(x)
        ).upper()

        if (
            "TARIFF" in row_text
            and "DESCRIPTION" in row_text
        ):
            header_row = i
            break

    if header_row is None:
        st.error("❌ AUTO MEGA header не е намерен")
        return pd.DataFrame()

    df = pd.read_excel(
        file,
        header=header_row
    )

    df.columns = (
        df.columns.astype(str)
        .str.strip()
    )

    rows = []

    for _, row in df.iterrows():

        try:

            code = str(
                row["Tariff Code"]
            ).strip()

            code = re.sub(
                r"\D",
                "",
                code
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            description = str(
                row["Description"]
            ).upper()

            qty = pd.to_numeric(
                row["Delivery"],
                errors="coerce"
            )

            net_weight = pd.to_numeric(
                row["wt./net"],
                errors="coerce"
            )

            item_weight = pd.to_numeric(
                row["wt./item"],
                errors="coerce"
            )

            if pd.isna(qty):
                continue

            if pd.isna(net_weight):
                continue

            wid = None

            # ✅ търси литраж в описанието
            match = re.search(
                r"(\d+(?:[.,]\d+)?)\s*L",
                description
            )

            if match:
                wid = float(
                    match.group(1).replace(",", ".")
                )

            # ✅ специални случаи

            if wid is None:

                # 🔥 FIX
                if "TOYOTA SAE 5W40" in description:
                    wid = 5

                elif "AUTOMATIC TRANSMISSION OIL" in description:
                    wid = 1

                elif "TRANSMISSION OIL" in description:
                    wid = 1

            # ✅ fallback по тегло

            if wid is None and pd.notna(item_weight):

                if 0.75 <= item_weight <= 1.30:
                    wid = 1

                elif 1.70 <= item_weight <= 2.30:
                    wid = 2

                elif 3.50 <= item_weight <= 4.40:
                    wid = 4

                elif 4.40 <= item_weight <= 5.80:
                    wid = 5

            if wid is None:
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,
                "kolichestvo": qty * wid,
                "тегло": net_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ AUTO MEGA parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
    # ======================================================
# ✅ FUCHS PDF
# ======================================================
def parse_fuchs(text):

    rows = []

    current_code = None
    current_wid = None

    current_qty = 0
    current_net = 0

    lines = text.split("\n")

    def flush_article():

        nonlocal current_code
        nonlocal current_wid
        nonlocal current_qty
        nonlocal current_net

        if (
            current_code
            and current_wid is not None
            and current_qty > 0
        ):

            if current_wid < 1:
                kolichestvo = current_net
            else:
                kolichestvo = current_qty * current_wid

            rows.append({
                "Тарифен код": current_code,
                "Количество": current_qty,
                "wid": current_wid,
                "kolichestvo": round(kolichestvo, 3),
                "тегло": round(current_net, 3)
            })

        current_code = None
        current_wid = None
        current_qty = 0
        current_net = 0

    for line in lines:

        line = " ".join(line.split())

        # ==============================================
        # ✅ нов артикул
        # ==============================================
        if "Material" in line:

            flush_article()

            wid = None

            upper_line = line.upper()

            # ✅ L
            m = re.search(
                r'(\d+(?:[\.,]\d+)?)\s*L\b',
                upper_line
            )

            if m:
                wid = float(
                    m.group(1).replace(",", ".")
                )

            # ✅ KG
            if wid is None:

                m = re.search(
                    r'(\d+(?:[\.,]\d+)?)\s*KG\b',
                    upper_line
                )

                if m:
                    wid = float(
                        m.group(1).replace(",", ".")
                    )

            # ✅ G
            if wid is None:

                m = re.search(
                    r'(\d+(?:[\.,]\d+)?)\s*G\b',
                    upper_line
                )

                if m:
                    wid = (
                        float(
                            m.group(1).replace(",", ".")
                        ) / 1000
                    )

            current_wid = wid

        # ==============================================
        # ✅ код
        # ==============================================
        if "Commodity Code" in line:

            m = re.search(
                r'Commodity Code\s+(\d+)',
                line,
                re.IGNORECASE
            )

            if m:

                code = m.group(1)[:8]

                if code in ALLOWED_CODES:
                    current_code = code
                else:
                    current_code = None

        # ==============================================
        # ✅ количества
        # ==============================================
        if "Quantity/net/gross" in line:

            m = re.search(
                r'([\d\.,]+)\s*EA\s*/\s*([\d\.,]+)\s*KG',
                line,
                re.IGNORECASE
            )

            if m:

                qty = float(
                    m.group(1)
                    .replace(",", "")
                )

                net = float(
                    m.group(2)
                    .replace(",", "")
                )

                current_qty += qty
                current_net += net

    flush_article()

    if not rows:
        return pd.DataFrame()

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
# ======================================================
# ✅ CHEMPIOIL PDF
# ======================================================
def parse_chempioil_pdf(text):

    rows = []

    lines = text.split("\n")

    for line in lines:

        line = " ".join(line.split())

        try:

            # ✅ HS CODE
            hs_match = re.search(
                r'(\d{4}\.\d{2}\.\d{2}\.\d{2})',
                line
            )

            if not hs_match:
                continue

            code = re.sub(
                r"\D",
                "",
                hs_match.group(1)
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            # ✅ Quantity + Net + Gross
            m = re.search(
                r'(\d+(?:\.\d+)?)\s+SZT\s+'
                r'(\d+(?:\.\d+)?)\s+'
                r'(\d+(?:\.\d+)?)\s+'
                r'\d{4}\.\d{2}\.\d{2}\.\d{2}',
                line
            )

            if not m:
                continue

            qty = float(m.group(1))
            net_weight = float(m.group(2))
            gross_weight = float(m.group(3))

            # ✅ WID
            wid = None

            upper_line = line.upper()

            m = re.search(
                r'(\d+(?:\.\d+)?)L\b',
                upper_line
            )

            if m:
                wid = float(m.group(1))

            if wid is None:

                m = re.search(
                    r'(\d+(?:\.\d+)?)KG\b',
                    upper_line
                )

                if m:
                    wid = float(m.group(1))

            if wid is None:

                m = re.search(
                    r'(\d+(?:\.\d+)?)\s*(?:GR|G)\b',
                    upper_line
                )

                if m:
                    wid = float(m.group(1)) / 1000

            if wid is None:
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,

                # ✅ литри
                "kolichestvo": qty * wid,

                # ✅ тегло
                "тегло": net_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ CHEMPIOIL PDF parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
# ======================================================
# ✅ CHEMPIOIL EXCEL (ALL FORMATS)
# ======================================================
def parse_chempioil_excel(file):

    raw = pd.read_excel(
        file,
        header=None
    )

    header_row = None

    for i in range(len(raw)):

        row_text = " ".join(
            str(x)
            for x in raw.iloc[i]
            if pd.notna(x)
        ).upper()

        if (
            ("HS CODE" in row_text and "NAME" in row_text)
            or
            ("PRODUCT NAME" in row_text and "CN" in row_text)
        ):
            header_row = i
            break

    if header_row is None:
        st.error("❌ CHEMPIOIL header не е намерен")
        return pd.DataFrame()

    df = pd.read_excel(
        file,
        header=header_row
    )

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # ==================================================
    # ✅ FORMAT 1
    # ==================================================

    if "HS Code" in df.columns:

        code_col = "HS Code"
        name_col = "Name"
        qty_col = "Quantity"
        net_col = "Net weight"

    # ==================================================
    # ✅ FORMAT 2
    # ==================================================

    elif "CN" in df.columns:

        code_col = "CN"
        name_col = "Product Name"
        qty_col = "Quantity"
        net_col = "Total Weight (NET):"

    else:

        st.error("❌ CHEMPIOIL: непознат Excel формат")
        return pd.DataFrame()

    rows = []

    for _, row in df.iterrows():

        try:

            description = str(
                row[name_col]
            ).upper()

            code = str(
                row[code_col]
            )

            code = re.sub(
                r"\D",
                "",
                code
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            qty = pd.to_numeric(
                row[qty_col],
                errors="coerce"
            )

            net_weight = pd.to_numeric(
                row[net_col],
                errors="coerce"
            )

            if pd.isna(qty):
                continue

            if pd.isna(net_weight):
                continue

            wid = None

            m = re.search(
                r'(\d+(?:[.,]\d+)?)\s*L\b',
                description
            )

            if m:
                wid = float(
                    m.group(1).replace(",", ".")
                )

            if wid is None:

                m = re.search(
                    r'(\d+(?:[.,]\d+)?)\s*KG\b',
                    description
                )

                if m:
                    wid = float(
                        m.group(1).replace(",", ".")
                    )

            if wid is None:

                m = re.search(
                    r'(\d+(?:[.,]\d+)?)\s*(?:GR|G)\b',
                    description
                )

                if m:
                    wid = float(
                        m.group(1).replace(",", ".")
                    ) / 1000

            if wid is None:
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": float(qty),
                "wid": wid,
                "kolichestvo": round(
                    float(qty) * wid,
                    3
                ),
                "тегло": round(
                    float(net_weight),
                    3
                )
            })

        except:
            continue

    if not rows:
        st.error("❌ CHEMPIOIL Excel parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
# ======================================================
# ✅ VALVOLINE EXCEL
# ======================================================
def parse_valvoline_excel(file):

    xl = pd.ExcelFile(file)

    sheet_name = None

    for s in xl.sheet_names:

        if "PL" in str(s).upper():
            sheet_name = s
            break

    if sheet_name is None:
        sheet_name = xl.sheet_names[0]

    raw = pd.read_excel(
        file,
        sheet_name=sheet_name,
        header=None
    )

    header_row = None

    for i in range(len(raw)):

        row_text = " ".join(
            str(x)
            for x in raw.iloc[i]
            if pd.notna(x)
        ).upper()

        if (
            "TARIFF NO." in row_text
            and
            "PACKAGING" in row_text
            and
            "NET KG" in row_text
        ):
            header_row = i
            break

    if header_row is None:
        st.error("❌ VALVOLINE header не е намерен")
        return pd.DataFrame()

    df = pd.read_excel(
        file,
        sheet_name=sheet_name,
        header=header_row
    )

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    rows = []

    for _, row in df.iterrows():

        try:

            tariff = str(
                row["Tariff No."]
            )

            code = re.sub(
                r"\D",
                "",
                tariff
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            packaging = str(
                row["Packaging"]
            ).upper()

            uom = str(
                row["UoM"]
            ).strip().lower()

            qty = pd.to_numeric(
                row["Qty"],
                errors="coerce"
            )

            net_weight = pd.to_numeric(
                row["Net Kg"],
                errors="coerce"
            )

            packages = pd.to_numeric(
                row["No. of packages"],
                errors="coerce"
            )

            if pd.isna(qty):
                continue

            if pd.isna(net_weight):
                continue

            if pd.isna(packages):
                continue

            wid = None

            # =====================================
            # ✅ CASE
            # =====================================

            if uom == "case":

                case_match = re.search(
                    r'(\d+)\s*[Xx/]\s*(\d+(?:[.,]\d+)?)\s*(?:L|KG|G)?',
                    packaging
                )

                if case_match:

                    units_per_case = float(
                        case_match.group(1)
                    )

                    wid = float(
                        case_match.group(2)
                        .replace(",", ".")
                    )

                    # ✅ G
                    if "G" in packaging and "KG" not in packaging:
                        wid = wid / 1000

                    broj = packages * units_per_case

                    colic = broj * wid

                else:

                    continue

            # =====================================
            # ✅ LIT / KG / G
            # =====================================

            else:

                m = re.search(
                    r'(\d+(?:[.,]\d+)?)\s*L',
                    packaging
                )

                if m:

                    wid = float(
                        m.group(1)
                        .replace(",", ".")
                    )

                else:

                    m = re.search(
                        r'(\d+(?:[.,]\d+)?)\s*KG',
                        packaging
                    )

                    if m:

                        wid = float(
                            m.group(1)
                            .replace(",", ".")
                        )

                    else:

                        m = re.search(
                            r'(\d+(?:[.,]\d+)?)\s*G',
                            packaging
                        )

                        if m:

                            wid = (
                                float(
                                    m.group(1)
                                    .replace(",", ".")
                                ) / 1000
                            )

                if wid is None:
                    continue

                broj = packages

                colic = qty

            rows.append({
                "Тарифен код": code,
                "Количество": broj,
                "wid": wid,
                "kolichestvo": colic,
                "тегло": net_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ VALVOLINE parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
# ======================================================
# ✅ EMINIA EXCEL
# ======================================================
def parse_eminia_excel(file):

    df = pd.read_excel(file)

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # ==========================================
    # ✅ намиране на колони
    # ==========================================

    desc_col = None
    code_col = None
    qty_col = None
    weight_col = None

    for col in df.columns:

        c = str(col).strip().lower()

        if "description" in c:
            desc_col = col

        elif "customs" in c and "code" in c:
            code_col = col

        elif c == "qty":
            qty_col = col

        elif (
            "total net weight" in c
            or "total weight" in c
        ):
            weight_col = col

    # ==========================================
    # ✅ fallback по позиция
    # D,E,H,L
    # ==========================================

    cols = list(df.columns)

    if desc_col is None and len(cols) > 3:
        desc_col = cols[3]

    if code_col is None and len(cols) > 4:
        code_col = cols[4]

    if qty_col is None and len(cols) > 6:
        qty_col = cols[6]

    if weight_col is None:

        # L колона
        if len(cols) > 11:
            weight_col = cols[11]

        # K колона
        elif len(cols) > 10:
            weight_col = cols[10]

    rows = []

    for _, row in df.iterrows():

        try:

            description = str(
                row[desc_col]
            )

            code = str(
                row[code_col]
            )

            code = re.sub(
                r"\D",
                "",
                code
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            # ==================================
            # ✅ WID
            # ==================================

            wid = None

            txt = description.upper().replace(",", ".")

            m = re.search(
                r'(\d+(?:\.\d+)?)\s*L\b',
                txt
            )

            if m:
                wid = float(m.group(1))

            if wid is None:

                m = re.search(
                    r'(\d+(?:\.\d+)?)\s*KG\b',
                    txt
                )

                if m:
                    wid = float(m.group(1))

            if wid is None:

                m = re.search(
                    r'(\d+(?:\.\d+)?)\s*(?:GR|G)\b',
                    txt
                )

                if m:
                    wid = float(m.group(1)) / 1000

            # не е масло
            if wid is None:
                continue

            qty = pd.to_numeric(
                row[qty_col],
                errors="coerce"
            )

            total_weight = pd.to_numeric(
                row[weight_col],
                errors="coerce"
            )

            if pd.isna(qty):
                continue

            if pd.isna(total_weight):
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,

                # както поиска
                "kolichestvo": total_weight,

                "тегло": total_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ EMINIA parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
  
# ======================================================
# ✅ FLUKAR (EXCEL ONLY ✅)
# ======================================================
def parse_flukar_excel(file):

    df_raw = pd.read_excel(file, header=None)

    header_row = None

    # ✅ намираме header ред
    for i in range(len(df_raw)):
        row = df_raw.iloc[i]

        if any("cn" in str(cell).lower() for cell in row if pd.notna(cell)):
            header_row = i
            break

    if header_row is None:
        st.error("❌ Не може да се намери header ред (CN code)")
        return pd.DataFrame()

    df = pd.read_excel(file, header=header_row)
    df.columns = df.columns.astype(str).str.strip()

    # ✅ извличаме само нужните колони
    result = pd.DataFrame()

    for col in df.columns:
        c = col.lower()

        if "cn" in c:
            result["Тарифен код"] = df[col]

        elif "quantity" in c or "pcs" in c or "колич" in c:
            result["Количество"] = df[col]

        elif "capacity" in c or "package" in c:
            if "wid" not in result.columns:
                result["wid"] = df[col]

        elif "liter" in c:
            result["kolichestvo"] = df[col]

        elif "nett" in c or "net" in c or "тегло" in c:
            result["тегло"] = df[col]

    # ✅ проверки
    required = ["Тарифен код", "Количество", "wid", "тегло"]

    for col in required:
        if col not in result.columns:
            st.error(f"❌ Липсва колона: {col}")
            return pd.DataFrame()

    # ✅ cleaning
    result = result.dropna(subset=["Тарифен код"])

    result["Количество"] = pd.to_numeric(result["Количество"], errors="coerce")
    result["wid"] = pd.to_numeric(result["wid"], errors="coerce")
    result["тегло"] = pd.to_numeric(result["тегло"], errors="coerce")

    if "kolichestvo" not in result.columns:
        result["kolichestvo"] = result["Количество"] * result["wid"]
    else:
        result["kolichestvo"] = pd.to_numeric(result["kolichestvo"], errors="coerce")

    # ✅ ✅ 🔥 ВАЖНО — ROUND САМО НА ТЕГЛО (като FLUKAR)

    result = result.dropna(subset=["Количество", "wid", "тегло"])

    # ✅ group
    result = result.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return result

from decimal import Decimal, ROUND_HALF_UP

# ======================================================
# ✅ FINAL REPORT (FIXED)
# ======================================================
from decimal import Decimal, ROUND_HALF_UP

def build_final_report(df, supplier):

    # ✅ FLUKAR логика
    if supplier == "FLUKAR":

        grouped = df.groupby(
            ["Тарифен код", "wid"],
            as_index=False
        ).agg({
            "Количество": "sum",
            "kolichestvo": "sum",
            "тегло": list
        })

        rows = []

        for code, group in grouped.groupby("Тарифен код"):

            for _, r in group.iterrows():

                precise_sum = sum(Decimal(str(x)) for x in r["тегло"])

                rounded = float(
                    precise_sum.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                )

                rows.append({
                    "Тарифен код": r["Тарифен код"],
                    "wid": r["wid"],
                    "Количество": r["Количество"],
                    "kolichestvo": r["kolichestvo"],
                    "тегло": rounded
                })

            code_sum = sum(
                Decimal(str(x))
                for sublist in group["тегло"]
                for x in sublist
            )

            code_rounded = float(
                code_sum.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            )

            rows.append({
                "Тарифен код": str(code) + " -",
                "wid": "",
                "Количество": "",
                "kolichestvo": sum(group["kolichestvo"]),
                "тегло": code_rounded
            })

            rows.append({
                "Тарифен код": "",
                "wid": "",
                "Количество": "",
                "kolichestvo": "",
                "тегло": ""
            })

        total_sum = sum(
            Decimal(str(x))
            for sublist in grouped["тегло"]
            for x in sublist
        )

        total_rounded = float(
            total_sum.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        )

        rows.append({
            "Тарифен код": "GRAND TOTAL",
            "wid": "",
            "Количество": "",
            "kolichestvo": grouped["kolichestvo"].sum(),
            "тегло": total_rounded
        })

        return pd.DataFrame(rows)

    # ✅ ✅ ВСИЧКИ ДРУГИ (MOTUL, NESTE, CASTROL)
    else:

        grouped = df.groupby(
            ["Тарифен код", "wid"],
            as_index=False
        ).agg({
            "Количество": "sum",
            "kolichestvo": "sum",
            "тегло": "sum"
        })

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
# ✅ AMTRA EXCEL
# ======================================================
def parse_amtra_excel(file):

    raw = pd.read_excel(
        file,
        sheet_name=1,
        header=None
    )

    header_row = None

    for i in range(len(raw)):

        row_text = " ".join(
            str(x)
            for x in raw.iloc[i]
            if pd.notna(x)
        ).upper()

        if (
            "PRODUCT NAME" in row_text
            and
            "CODE CN" in row_text
        ):
            header_row = i
            break

    if header_row is None:
        st.error("❌ AMTRA header не е намерен")
        return pd.DataFrame()

    df = pd.read_excel(
        file,
        sheet_name=1,
        header=header_row
    )

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    rows = []

    for _, row in df.iterrows():

        try:

            description = str(df.iloc[_ , 2])
            qty = pd.to_numeric(df.iloc[_ , 3], errors="coerce")
            code = str(df.iloc[_ , 6])
            net_weight = pd.to_numeric(df.iloc[_ , 9], errors="coerce")

            code = re.sub(r"\D", "", code)[:8]

            if code not in ALLOWED_CODES:
                continue

            txt = re.sub(
                r"\([^)]*\)",
                "",
                description
            ).upper()

            wid = None

            m = re.search(r"(\d+(?:[.,]\d+)?)\s*ML", txt)
            if m:
                wid = float(m.group(1).replace(",", ".")) / 1000

            if wid is None:
                m = re.search(r"(\d+(?:[.,]\d+)?)\s*L\b", txt)
                if m:
                    wid = float(m.group(1).replace(",", "."))

            if wid is None:
                m = re.search(r"(\d+(?:[.,]\d+)?)\s*KG", txt)
                if m:
                    wid = float(m.group(1).replace(",", "."))

            if wid is None:
                m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:GR|G)\b", txt)
                if m:
                    wid = float(m.group(1).replace(",", ".")) / 1000

            if wid is None:
                continue

            if pd.isna(qty):
                continue

            if pd.isna(net_weight):
                continue

            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,
                "kolichestvo": qty * wid,
                "тегло": net_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ AMTRA parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
    # ======================================================
# ✅ ELROMI RONAX
# ======================================================
def parse_elromi_excel(file):

    xl = pd.ExcelFile(file)

    sheet_name = None

    for s in xl.sheet_names:

        if str(s).strip().upper() == "INHALT":
            sheet_name = s
            break

    if sheet_name is None:

        if len(xl.sheet_names) > 1:
            sheet_name = xl.sheet_names[1]
        else:
            sheet_name = xl.sheet_names[0]

    df = pd.read_excel(
        file,
        sheet_name=sheet_name
    )

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    rows = []

    for _, row in df.iterrows():

        try:

            code = str(row["tariff"])

            code = re.sub(
                r"\D",
                "",
                code
            )[:8]

            if code not in ALLOWED_CODES:
                continue

            qty = pd.to_numeric(
                row["Menge"],
                errors="coerce"
            )

            unit_weight = pd.to_numeric(
                row["Gewicht, kg"],
                errors="coerce"
            )

            if pd.isna(unit_weight):
                continue

            # ✅ игнорирай всичко под 0.50 кг
            if unit_weight < 0.50:
                continue

            if unit_weight <= 0:
                continue

            wid = max(
                1,
                round(float(unit_weight))
            )

            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,
                "kolichestvo": qty * wid,
                "тегло": qty * unit_weight
            })

        except:
            continue

    if not rows:
        st.error("❌ ELROMI parser не извлече данни")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = df_out.groupby(
        ["Тарифен код", "wid"],
        as_index=False
    ).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out
 # ======================================================
# ✅ BRECHMANN
# ======================================================
def parse_brechmann_excel(file):

    # търси реда с истинските заглавия
    raw = pd.read_excel(
        file,
        header=None
    )

    header_row = None

    for idx in range(len(raw)):

        row_text = " ".join(
            [str(x) for x in raw.iloc[idx].tolist()]
        )

        if (
            "HS Code" in row_text
            and "Qty" in row_text
        ):
            header_row = idx
            break

    if header_row is None:
        st.error("❌ Не намерих header на BRECHMANN")
        return pd.DataFrame()

    df = pd.read_excel(
        file,
        header=header_row
    )

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    rows = []

    for _, row in df.iterrows():

        try:

            # -------------------------------------------------
            # CODE
            # -------------------------------------------------
            code = str(
                row.get("HS Code", "")
            )

            code = re.sub(
                r"\D",
                "",
                code
            )[:8]

            if not code:
                continue

            if code not in ALLOWED_CODES:
                continue

            # -------------------------------------------------
            # BROJ
            # -------------------------------------------------
            qty = pd.to_numeric(
                row.get("Qty"),
                errors="coerce"
            )

            if pd.isna(qty):
                continue

            # -------------------------------------------------
            # NET WEIGHT
            # -------------------------------------------------
            net_weight = pd.to_numeric(
                row.get("Net Weight"),
                errors="coerce"
            )

            if pd.isna(net_weight):
                net_weight = 0

            # -------------------------------------------------
            # WID
            # -------------------------------------------------
            package = str(
                row.get(
                    "Gebindegröße Öl",
                    ""
                )
            ).upper()

            wid = None

            # 12x1L -> 1
            m = re.search(
                r'X\s*(\d+(?:[.,]\d+)?)\s*L',
                package
            )

            if m:
                wid = float(
                    m.group(1).replace(",", ".")
                )

            # 4x20KG -> 20
            if wid is None:

                m = re.search(
                    r'X\s*(\d+(?:[.,]\d+)?)\s*KG',
                    package
                )

                if m:
                    wid = float(
                        m.group(1).replace(",", ".")
                    )

            # 12x500G -> 0.5
            if wid is None:

                m = re.search(
                    r'X\s*(\d+(?:[.,]\d+)?)\s*G',
                    package
                )

                if m:
                    wid = (
                        float(
                            m.group(1).replace(",", ".")
                        )
                        / 1000
                    )

            if wid is None:
                continue

            # -------------------------------------------------
            # REPORT ROW
            # -------------------------------------------------
            rows.append({
                "Тарифен код": code,
                "Количество": qty,
                "wid": wid,
                "kolichestvo": qty * wid,
                "тегло": qty * net_weight
            })

        except Exception:
            continue

    if not rows:
        st.error(
            "❌ BRECHMANN parser не извлече данни"
        )
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    df_out = (
        df_out.groupby(
            ["Тарифен код", "wid"],
            as_index=False
        )
        .agg({
            "Количество": "sum",
            "kolichestvo": "sum",
            "тегло": "sum"
        })
    )

    return df_out
# ======================================================
# ✅ FEBI EXCEL
# ======================================================
def parse_febi_excel(file):

    try:

        df = pd.read_xml(file)

        st.write("COLUMNS:")
        st.write(df.columns.tolist())

        return pd.DataFrame()

    except Exception as e:

        st.error(f"❌ FEBI ERROR: {e}")

        return pd.DataFrame()

# ======================================================
# ✅ ORLEN (EXCEL)
# ======================================================
def parse_orlen_excel(file):

    df = pd.read_excel(file)

    df.columns = df.columns.astype(str).str.strip()

    rename_map = {}

    for col in df.columns:
        c = col.lower()

        if "code cn" in c or "cn code" in c:
            rename_map[col] = "Тарифен код"

        elif c == "qty":
            rename_map[col] = "Количество"

        elif "net weight" in c:
            rename_map[col] = "тегло"

        elif "material" in c:
            rename_map[col] = "material"

    df = df.rename(columns=rename_map)

    required = [
        "Тарифен код",
        "Количество",
        "тегло",
        "material"
    ]

    for col in required:
        if col not in df.columns:
            st.error(f"❌ ORLEN: липсва колона {col}")
            return pd.DataFrame()

    # ✅ само позволените кодове
    df["Тарифен код"] = (
        df["Тарифен код"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
        .str[:8]
    )

    df = df[df["Тарифен код"].isin(ALLOWED_CODES)]

    # ==================================================
    # ✅ извличане на разфасовка от Material
    # ==================================================
    def extract_wid(material):

        txt = str(material).upper().replace(",", ".")

        # 20L, 205L, 4.5L, 0.6L и т.н.
        m = re.search(r'(\d+(?:\.\d+)?)\s*L\b', txt)
        if m:
            return float(m.group(1))

        # 17KG, 9KG, 4.5KG...
        m = re.search(r'(\d+(?:\.\d+)?)\s*KG\b', txt)
        if m:
            return float(m.group(1))

        # 800G, 400G...
        m = re.search(r'(\d+(?:\.\d+)?)\s*G\b', txt)
        if m:
            return float(m.group(1)) / 1000

        return None

    df["wid"] = df["material"].apply(extract_wid)

    df = df[df["wid"].notna()]

    # ✅ числа
    df["Количество"] = pd.to_numeric(
        df["Количество"],
        errors="coerce"
    )

    df["тегло"] = pd.to_numeric(
        df["тегло"],
        errors="coerce"
    )

    # ✅ Qty × wid
    df["kolichestvo"] = (
        df["Количество"] * df["wid"]
    )

    df = df.dropna(
        subset=[
            "Тарифен код",
            "Количество",
            "wid",
            "тегло"
        ]
    )

    # ✅ групиране
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
# ✅ PROCESS
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        df = None

        # ✅ CASTROL + NESTE
        if menu == "CASTROL & NESTE" and source_type == "Excel":
            df = parse_castrol_excel(file)

        # ✅ FLUKAR
        elif menu == "FLUKAR":
            df = parse_flukar_excel(file)
        # ✅ ELROMI
        elif menu == "ELROMI RONAX":
            df = parse_elromi_excel(file)

        # ✅ NISTA
        elif menu == "NISTA":
            df = parse_nista_excel(file)

        # ✅ ORLEN
        elif menu == "ORLEN":
            df = parse_orlen_excel(file)

        # ✅ AUTO MEGA
        elif menu == "AUTO MEGA":
            df = parse_auto_mega_excel(file)
         # ✅ AMTRA
        elif menu == "AMTRA":
            df = parse_amtra_excel(file)
        # ✅ EMINIA
        elif menu == "EMINIA":
            df = parse_eminia_excel(file)
            
        # ✅ BRECHMANN
        elif menu == "Brehman":
            df = parse_brechmann_excel(file)
            
        # ✅ FEBI
        elif menu == "FEBI":
            df = parse_febi_excel(file)


        # ✅ CHEMPIOIL EXCEL
        elif menu == "Chempioil (FANFARO)" and source_type == "Excel":
            df = parse_chempioil_excel(file)

        # ✅ VALVOLINE
        elif menu == "VALVOLINE":
            df = parse_valvoline_excel(file)

        # ✅ PDF SECTION
        elif source_type == "PDF":

            reader = PdfReader(file)

            text = ""

            for page in reader.pages:

                t = page.extract_text()

                if t:
                    text += t + "\n"

            if menu == "FUCHS":
                df = parse_fuchs(text)

            elif menu == "Chempioil (FANFARO)":
                df = parse_chempioil_pdf(text)

            else:
                df = parse_motul(text)

        else:

            df = pd.read_excel(file)
            df.columns = df.columns.str.strip()

        if isinstance(df, pd.DataFrame) and not df.empty:
            all_data.append(df)

    if not all_data:
        st.warning("⚠️ Няма данни")
        st.stop()

    final_df = pd.concat(
        all_data,
        ignore_index=True
    )

    if "Тарифен код" not in final_df.columns:
        st.warning("⚠️ Данните не съдържат тарифен код")
        st.stop()

    final_df["Тарифен код"] = (
        final_df["Тарифен код"]
        .astype(str)
    )

    final_df = final_df[
        final_df["тегло"] > 0
    ]

    report = build_final_report(
        final_df,
        menu
    )

    report["Тарифен код"] = (
        report["Тарифен код"]
        .astype(str)
    )

    report["Тарифен код"] = report["Тарифен код"].str.replace(
        "38119000",
        "38119000 - EMCS",
        regex=False
    )

    special_codes = [
        "38112100",
        "38249992",
        "27101225",
        "38140090",
        "38249996"
    ]

    for code in special_codes:

        report["Тарифен код"] = report["Тарифен код"].str.replace(
            f"{code} -",
            f"{code} - ( ! )",
            regex=False
        )

        report["Тарифен код"] = report["Тарифен код"].replace(
            {code: f"{code} ( ! )"}
        )

    st.subheader("📊 Финален отчет")
    st.dataframe(report)

    report = report.rename(columns={
        "Тарифен код": "Code",
        "wid": "wid",
        "Количество": "Broj",
        "kolichestvo": "colic-v L",
        "тегло": "teglo"
    })

    from openpyxl.styles import Font

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        report.to_excel(
            writer,
            index=False
        )

        ws = writer.sheets["Sheet1"]

        red_codes = [
            "34039900",
            "34031910",
            "34031980"
        ]

        for row in ws.iter_rows(min_row=2):

            code_cell = row[0]

            value = str(code_cell.value)

            for code in red_codes:

                if value.startswith(code):

                    code_cell.font = Font(
                        bold=True,
                        color="FF0000"
                    )

                    break

    output.seek(0)

    st.download_button(
        label="📥 Изтегли Excel",
        data=output,
        file_name="final_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:

    st.markdown(
        "**⬆️ Качи файл, за да генерираш отчет**"
    )
