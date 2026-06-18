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
# ✅ LOGIN SYSTEM
# ======================================================
def check_login():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:

        # ✅ login background
        set_bg("background_login.png")

        st.markdown("<h1 style='text-align:center; color:white;'>🔐 Вход</h1>", unsafe_allow_html=True)

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

# ✅ main background
set_bg("background.png")


# ======================================================
# ✅ HEADER
# ======================================================
st.markdown(
    """
    <div style="
        position: fixed;
        top: 10px;
        right: 25px;
        font-size: 36px;
        font-weight: 900;
        color: white;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
        z-index: 9999;
    ">
        CustomsFlow
    </div>
    """,
    unsafe_allow_html=True
)


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
# ✅ FINAL UI (CLEAN VERSION)
# ======================================================

st.markdown("""
<style>

/* ✅ заглавие */
.source-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

/* ✅ стрелка */
.arrow {
    font-size: 22px;
    color: white;
    margin-bottom: 10px;
}

/* ✅ бутони */
.btn-pdf {
    background-color: rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    font-weight: 700;
    color: white;
}

.btn-excel {
    background-color: rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    font-weight: 700;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ✅ Choose Source (само текст + стрелка)
st.markdown('<div class="source-title">👇 Choose Source</div>', unsafe_allow_html=True)


# ✅ state
if "source_type" not in st.session_state:
    st.session_state["source_type"] = "PDF"


# ✅ цветове
if st.session_state["source_type"] == "PDF":
    pdf_color = "#ff3b3b"   # червен
    excel_color = "#444"
else:
    pdf_color = "#444"
    excel_color = "#36c165" # зелен


# ✅ CSS → СКРИВАМЕ истинските бутони
st.markdown("""
<style>
button[kind="secondary"] {
    opacity: 0;
    height: 0px;
    padding: 0px;
    margin: 0px;
}
</style>
""", unsafe_allow_html=True)


# ✅ layout
col1, col2 = st.columns([1,1])

with col1:
    if st.button("PDF"):
        st.session_state["source_type"] = "PDF"

    st.markdown(f"""
        <div style="
            background:{pdf_color};
            padding: 14px;
            border-radius: 12px;
            text-align:center;
            font-weight:800;
            color:white;
            cursor:pointer;
        ">
            PDF
        </div>
    """, unsafe_allow_html=True)


with col2:
    if st.button("Excel"):
        st.session_state["source_type"] = "Excel"

    st.markdown(f"""
        <div style="
            background:{excel_color};
            padding: 14px;
            border-radius: 12px;
            text-align:center;
            font-weight:800;
            color:white;
            cursor:pointer;
        ">
            Excel
        </div>
    """, unsafe_allow_html=True)


source_type = st.session_state["source_type"]

# ✅ визуален цветен статус
if source_type == "PDF":
    st.markdown(
        "<div style='color:#ff3b3b; font-weight:900;'>You Chose: PDF</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div style='color:#36c165; font-weight:900;'>You Chose: Excel</div>",
        unsafe_allow_html=True
    )


# ✅ Add file (точно над upload)
st.markdown(
    "<div style='font-size:20px; font-weight:900; color:white; margin-top:15px;'>Add file</div>",
    unsafe_allow_html=True
)


# ✅ uploader (веднага под текста)
uploaded_files = st.file_uploader(
    "",
    type=["pdf"] if source_type == "PDF" else ["xlsx", "xls"],
    accept_multiple_files=True
)


# ✅ sidebar → само Suppliers
menu = st.sidebar.selectbox("Suppliers", ["Castrol", "MOTUL"])


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

        match = re.search(r"\d+\s+\d+\s+(\d+)\s+[\d,\.]+\s+[\d,\.]+", line)
        if match:
            try:
                current_qty = int(match.group(1))
            except:
                pass

        weights = re.findall(r"\d+,\d+", line)
        if weights:
            try:
                current_weight = float(weights[0].replace(",", "."))
            except:
                pass

        multi = re.findall(r"(\d+)X([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)
        single = re.search(r"([\d\.,]+)(?:L|kg)", line, re.IGNORECASE)

        if multi:
            units_in_box = int(multi[-1][0])
            liters_per_unit = float(multi[-1][1].replace(",", "."))
        elif single:
            units_in_box = 1
            liters_per_unit = float(single.group(1).replace(",", "."))

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

    return pd.DataFrame(rows)


# ======================================================
# ✅ REPORT
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
if uploaded_files:

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
