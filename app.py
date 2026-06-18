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
# ✅ LOGIN SYSTEM (с различен background)
# ======================================================
def check_login():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # ✅ ако НЕ е логнат → login фон
    if not st.session_state["logged_in"]:

        set_bg("background_login.png")

        st.markdown(
            "<h1 style='text-align:center; color:white;'>🔐 Вход в системата</h1>",
            unsafe_allow_html=True
        )

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


# ✅ ако не е логнат → спира всичко
if not check_login():
    st.stop()


# ======================================================
# ✅ MAIN APP BACKGROUND (след login)
# ======================================================
set_bg("background.png")
# ======================================================
# ✅ МИТНИЧЕСКИ КОДОВЕ
# ======================================================
ALLOWED_CODES = [
    "27101991","27101981","27101983","27101987",
    "27101993","27101999","34031910","34039900",
    "34031980","38119000","38112100","38249992",
    "27101225","38140090"
]


# ======================================================
# ✅ UI
# ======================================================

# ✅ Header (CustomsFlow горе вдясно)
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

# ✅ (по желание) лого – ако файлът съществува
try:
    st.image("logo.png", width=120)
except:
    pass

# ✅ Основни избори
source_type = st.radio("👉 Избери източник", ["PDF", "Excel"])
menu = st.sidebar.selectbox("Доставчик", ["Castrol", "MOTUL"])

# ======================================================
# ✅ MOTUL (ФИНАЛЕН 100%)
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

        # ✅ тегло (само със запетая)
        weights = re.findall(r"\d+,\d+", line)
        if weights:
            try:
                current_weight = float(weights[0].replace(",", "."))
            except:
                pass

        # ✅ multipack (L + kg + 0,300)
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

                # ✅ ✅ ключов FIX: нормализиране до 8 цифри
                code_value = code.group(1)[:8]

                # ✅ защита от двойно умножение
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

    # ✅ row-level density (най-точното)
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
# ✅ PDF
# ======================================================
if source_type == "PDF":

    uploaded_files = st.file_uploader(
        "Качи PDF файлове",
        type=["pdf"],
        accept_multiple_files=True
    )

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

        # ✅ филтър по кодове
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
            file_name="pdf_final_report.xlsx"
        )

# ======================================================
# ✅ EXCEL
# ======================================================
elif source_type == "Excel":

    excel_file = st.file_uploader("Качи Excel", type=["xlsx", "xls"])

    if excel_file:

        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.strip()

        column_map = {}

        for col in df.columns:
            c = col.lower()

            if "commodity" in c:
                column_map[col] = "Commodity code"
            elif "pack" in c:
                column_map[col] = "Type of packaging"
            elif "delivery quantity" in c:
                column_map[col] = "Delivery quantity"
            elif "volume" in c:
                column_map[col] = "Volume"
            elif "net weight" in c:
                column_map[col] = "Net Weight"

        df = df.rename(columns=column_map)

        df_common = df.groupby(
            ["Commodity code", "Type of packaging"],
            as_index=False
        ).agg({
            "Delivery quantity": "sum",
            "Volume": "sum",
            "Net Weight": "sum"
        })

        df_common = df_common.rename(columns={
            "Commodity code": "Тарифен код",
            "Type of packaging": "wid",
            "Delivery quantity": "Количество",
            "Volume": "kolichestvo",
            "Net Weight": "тегло"
        })

        report = build_final_report(df_common)

        st.subheader("📊 Финален отчет")
        st.dataframe(report)

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            report.to_excel(writer, index=False)

        st.download_button(
            "📥 Изтегли Excel",
            data=output.getvalue(),
            file_name="excel_final_report.xlsx"
        )
