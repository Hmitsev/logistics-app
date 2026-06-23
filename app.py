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
menu = st.sidebar.selectbox("Suppliers", ["CASTROL", "MOTUL", "NESTE", "FLUKAR", "GASOLIN", "VALVOLINE", "ORLEN", "Chempioil (FANFARO)", "FUCHS", "FEBI", "ELROMI RONAX","NISTA", "AMTRA" , "AUTO MEGA" ,"EMINIA" ,"Brehman"])
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
    ("NISTA", "Excel"),
    ("AUTO MEGA", "Excel"),
    ("EMINIA", "Excel"),
    ("Brehman", "Excel"),
]

# ✅ обръщаме реда (както искаш)
suppliers_table = suppliers_table[::-1]

# ✅ правим DataFrame за визуализация
df_suppliers = pd.DataFrame(suppliers_table, columns=["Supplier", "File"])

st.sidebar.dataframe(df_suppliers, use_container_width=True, height=350)
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

        # ✅ ✅ ТЕГЛО (ТОЧНО NET след Quantity)
        weight_match = re.search(
            r"\d+\s+\d+\s+(\d+)\s+([\d\s,]+)\s+([\d\s,]+)",
            line
        )

        if weight_match:
            try:
                net_weight = float(
                    weight_match.group(2).replace(" ", "").replace(",", ".")
                )

                # ✅ защита
                if net_weight < 100000:
                    current_weight = net_weight

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
# ✅ FEBI (PDF ✅)
# ======================================================
def parse_febi_pdf(text):

    rows = []
    lines = text.split("\n")

    current_qty = 0
    current_weight = 0
    current_wid = 1

    for line in lines:

        # ✅ Quantity (пример: 36 PCE)
        qty_match = re.search(r"(\d+)\s+PCE", line)
        if qty_match:
            try:
                current_qty = int(qty_match.group(1))
            except:
                pass

        # ✅ wid (пример: = 1PC = 5L или 1L)
        wid_match = re.search(r"=\s*1PC\s*=\s*(\d+)L", line)
        if wid_match:
            current_wid = float(wid_match.group(1))
        else:
            single_wid = re.search(r"=\s*(\d+)L", line)
            if single_wid:
                current_wid = float(single_wid.group(1))

        # ✅ HS CODE
        if "HS Code" in line:
            code_match = re.search(r"HS Code No\.\:\s*(\d+)", line)

            if code_match:

                code = code_match.group(1)

                rows.append({
                    "Тарифен код": code,
                    "Количество": current_qty,
                    "wid": current_wid,
                    "kolichestvo": current_qty * current_wid,
                    "тегло": 0   # ✅ тук ще сложим тегло по-долу
                })

                # reset
                current_qty = 0
                current_wid = 1

    return pd.DataFrame(rows)

# ======================================================
# ✅ CASTROL (EXCEL ✅)
# ======================================================
def parse_castrol_excel(file):

    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    rename_map = {}

    for col in df.columns:
        c = col.lower()

        if "commodity" in c:
            rename_map[col] = "Тарифен код"

        elif "delivery quantity" in c or "quantity" in c:
            rename_map[col] = "Количество"

        elif "volume" in c:
            rename_map[col] = "kolichestvo"

        elif "net weight" in c:
            rename_map[col] = "тегло"

        elif "type of packaging" in c or "packaging" in c:
            rename_map[col] = "wid"

    df = df.rename(columns=rename_map)

    if "Тарифен код" not in df.columns:
        return pd.DataFrame()

    df = df.dropna(subset=["Тарифен код"])

    # fallback wid
    if "wid" not in df.columns and "kolichestvo" in df.columns:
        df["wid"] = df["kolichestvo"] / df["Количество"]

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
# ✅ PROCESS
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        df = None

        # ✅ NESTE
        if menu == "NESTE":
            df = parse_neste_excel(file)

        # ✅ FLUKAR
        elif menu == "FLUKAR":
            df = parse_flukar_excel(file)

        # ✅ FEBI
        elif menu == "FEBI":
            df = parse_febi_excel(file)

        # ✅ CASTROL Excel
        elif menu == "CASTROL" and source_type == "Excel":
            df = parse_castrol_excel(file)

        # ✅ PDF (MOTUL / CASTROL)
        elif source_type == "PDF":
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    if menu == "CASTROL":
        df = parse_castrol(text)
    else:
        df = parse_motul(text)


        # ✅ fallback Excel
        else:
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip()

        # ✅ append result
        if isinstance(df, pd.DataFrame) and not df.empty:
            all_data.append(df)

    # ✅ няма данни
    if not all_data:
        st.warning("⚠️ Няма данни")
        st.stop()

    final_df = pd.concat(all_data, ignore_index=True)

    # ✅ DEBUG (скрит)
    DEBUG = False
    if DEBUG:
        st.write("DEBUG DF:")
        st.dataframe(final_df.head(20))

    # ✅ check
    if "Тарифен код" not in final_df.columns:
        st.warning("⚠️ Данните не съдържат тарифен код")
        st.stop()

    final_df["Тарифен код"] = final_df["Тарифен код"].astype(str)

    # ✅ филтър по тегло
    final_df = final_df[final_df["тегло"] > 0]

    # ✅ final report
    report = build_final_report(final_df, menu)

    report = report.rename(columns={
        "Тарифен код": "Code",
        "wid": "wid",
        "тегло": "teglo",
        "kolichestvo": "colic-v L",
        "Количество": "Broj"
    })

    st.subheader("📊 Финален отчет")
    st.dataframe(report)

    # ✅ EXPORT
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report.to_excel(writer, index=False)

    output.seek(0)

    st.download_button(
        label="📥 Изтегли Excel",
        data=output,
        file_name="final_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.markdown("**⬆️ Качи файл, за да генерираш отчет**")
