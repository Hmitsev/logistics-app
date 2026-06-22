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
menu = st.sidebar.selectbox("Suppliers", ["CASTROL", "MOTUL","NESTE","GASOLINE"])

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
# ✅ GASOLINE (FINAL FIXED VERSION ✅)
# ======================================================
def parse_gasoline(file):

    import re
    import pandas as pd
    from PyPDF2 import PdfReader

    def parse_float(val):
        try:
            val = str(val).strip()
            if "." in val and "," in val:
                val = val.replace(".", "").replace(",", ".")
            else:
                val = val.replace(",", ".")
            return float(val)
        except:
            return 0

    reader = PdfReader(file)

    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

    # ✅ SPLIT ПО ПРОДУКТИ (ТОВА Е КЛЮЧА)
    blocks = text.split("Zolltarifnummer")

    rows = []

    for block in blocks:

        try:
            if "Liter" not in block:
                continue

            # =========================
            # ✅ CODE
            # =========================
            code_match = re.search(r"(\d{8})", block)
            if not code_match:
                continue

            code = code_match.group(1)

            # =========================
            # ✅ COLIC (Menge)
            # =========================
            m = re.search(r"([\d\.,]+)\s+Liter", block)
            if not m:
                continue

            colic = parse_float(m.group(1))

            # =========================
            # ✅ WID
            # =========================
            wid = 1

            multi = re.search(r"(\d+)\s*x\s*([\d\.,]+)", block)
            if multi:
                wid = parse_float(multi.group(2))

            single = re.search(r"([\d\.,]+)\s+Liter\s+(Fass|Kanne)", block)
            if single:
                wid = parse_float(single.group(1))

            if wid == 0:
                wid = 1

            # =========================
            # ✅ WEIGHT (точно преди опаковка)
            # =========================
            weight = 0

            w = re.search(
                r"([\d\.,]+)\s+(?:\d+\s*x\s*\d+|\d+\s+Liter\s+(?:Fass|Kanne))",
                block
            )

            if w:
                weight = parse_float(w.group(1))

            # ✅ fallback
            if weight == 0:
                if "Shell Rimula R6 LM 10w40" in block:
                    weight = colic * 0.666
                else:
                    weight = colic * 0.88

            # =========================
            # ✅ BROJ
            # =========================
            broj = colic / wid if wid else 0

            rows.append({
                "Тарифен код": code,
                "wid": wid,
                "Количество": broj,
                "kolichestvo": colic,
                "тегло": weight
            })

        except:
            continue

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # ✅ aggregation след всички PDF-и
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
# ✅ FINAL REPORT
# ======================================================
def build_final_report(df):

    grouped = df.groupby(
    ["Тарифен код", "wid"],
    as_index=False
).agg({
    "Количество": "sum",     # units
    "kolichestvo": "sum",    # liters (реалното)
    "тегло": "sum"           # weight
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
# ✅ PROCESS (FINAL FIXED ✅)
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        df = None

        # ✅ NESTE
        if menu == "NESTE":
            df = parse_neste_excel(file)

        # ✅ PDF
        elif source_type == "PDF":
            reader = PdfReader(file)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            if menu == "CASTROL":
                df = parse_castrol(text)

            elif menu == "GASOLINE":
                df = parse_gasoline(file)

            else:
                df = parse_motul(text)

        # ✅ Excel fallback
        else:

            df = pd.read_excel(file)
            df.columns = df.columns.str.strip()

            column_map = {}

            for col in df.columns:
                c = col.lower()

                if "commodity" in c or "code" in c:
                    column_map[col] = "Commodity code"

                elif "pack" in c:
                    column_map[col] = "Type of packaging"

                elif "delivery quantity" in c or "qty" in c:
                    column_map[col] = "Delivery quantity"

                elif "volume" in c:
                    column_map[col] = "Volume"

                elif "net weight" in c or "weight" in c:
                    column_map[col] = "Net Weight"

            df = df.rename(columns=column_map)
            df = df.loc[:, ~df.columns.duplicated()]

            df = df.rename(columns={
                "Commodity code": "Тарифен код",
                "Type of packaging": "wid",
                "Delivery quantity": "Количество",
                "Volume": "kolichestvo",
                "Net Weight": "тегло"
            })

        # ✅ SAFE APPEND
        if isinstance(df, pd.DataFrame) and not df.empty:
            all_data.append(df)

    # ✅ FINAL COMBINE
    if not all_data:
        st.warning("⚠️ Няма данни")
        st.stop()

    final_df = pd.concat(all_data, ignore_index=True)

    if "Тарифен код" not in final_df.columns:
        st.warning("⚠️ Данните не съдържат тарифен код – файлът не е разпознат")
        st.stop()

    # ======================================================
    # ✅ ✅ ✅ КРИТИЧЕН FIX (ТУК БЕШЕ ПРОБЛЕМЪТ)
    # ======================================================
    final_df["Тарифен код"] = final_df["Тарифен код"].astype(str).str.strip()
    final_df["Тарифен код"] = final_df["Тарифен код"].str.extract(r"(\d{8})")

    # ✅ вместо strict match → стабилен filter
    final_df = final_df[final_df["Тарифен код"].isin(ALLOWED_CODES)]

    # ======================================================

    if "тегло" not in final_df.columns:
        final_df["тегло"] = 0

    if menu in ["MOTUL", "NESTE"]:
        final_df = final_df[final_df["тегло"] > 0]

    # ✅ ако след filter няма редове → показва реалния проблем
    if final_df.empty:
        st.warning("⚠️ Данните бяха намерени, но всички бяха филтрирани (провери кодовете)")
        st.write("Намерени кодове:", pd.concat(all_data)["Тарифен код"].unique())
        st.stop()

    # ✅ REPORT
    report = build_final_report(final_df)

    report = report.rename(columns={
        "Тарифен код": "Code",
        "wid": "wid",
        "тегло": "teglo",
        "kolichestvo": "colic-v L",
        "Количество": "Broj"
    })

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
