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
# ✅ LOGOUT BUTTON
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
# ✅ LOGIN
# ======================================================
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:

        set_bg("background_login.png")

        col1, col2 = st.columns([4,1])

        with col1:
            st.markdown("""
            <div style="text-align:right;font-size:32px;font-weight:900;color:white;">
                CustomsFlow
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.image("Screenshot 2026-06-18 093459.png", width=60)

        st.markdown("<br>", unsafe_allow_html=True)

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
# ✅ FUCHS PARSER (НОВИЯ ДОСТАВЧИК)
# ======================================================
def parse_fuchs_pdf(text):

    rows = []
    current_tariff = None
    current_pack = None

    lines = text.split("\n")

    for line in lines:

        # ✅ Material (взимаме разфасовка)
        if "Material" in line and "TITAN" in line:
            pack_match = re.search(r'(\d+L|\d+G)', line)
            if pack_match:
                current_pack = pack_match.group(1)

        # ✅ Commodity Code
        elif "Commodity Code" in line:
            code = re.findall(r'\d{8}', line)
            if code:
                current_tariff = code[0]

        # ✅ Quantity/net/gross
        elif "Quantity/net/gross" in line:
            nums = re.findall(r'[\d,.]+', line)
            if len(nums) >= 2:
                qty = float(nums[0].replace(",", ""))
                kg = float(nums[1].replace(",", ""))

                rows.append({
                    "Тарифен код": current_tariff,
                    "Количество": qty,
                    "wid": current_pack,
                    "kolichestvo": qty,
                    "тегло": kg
                })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # ✅ събира batch редовете
    df = df.groupby(["Тарифен код", "wid"], as_index=False).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df


def parse_fuchs_excel(file):

    df = pd.read_excel(file, engine="openpyxl")

    df_out = df.rename(columns={
        "Comm./imp. code no.": "Тарифен код",
        "Delivery quantity": "Количество",
        "Net Weight": "тегло"
    })

    df_out["wid"] = df["Description"].str.extract(r'(\d+L|\d+G)')
    df_out["kolichestvo"] = df_out["Количество"]

    df_out = df_out.groupby(["Тарифен код", "wid"], as_index=False).agg({
        "Количество": "sum",
        "kolichestvo": "sum",
        "тегло": "sum"
    })

    return df_out


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
# ✅ SIDEBAR
# ======================================================
menu = st.sidebar.selectbox("Suppliers", ["Castrol", "MOTUL", "FUCHS"])

if "prev_supplier" not in st.session_state:
    st.session_state["prev_supplier"] = menu

if st.session_state["prev_supplier"] != menu:
    st.session_state["source_type"] = ""
    st.session_state["prev_supplier"] = menu


# ======================================================
# ✅ UPLOAD
# ======================================================
uploaded_files = st.file_uploader(
    "",
    type=["pdf", "xlsx", "xls"],
    accept_multiple_files=True
)


# ======================================================
# ✅ PROCESS
# ======================================================
if uploaded_files:

    all_data = []

    for file in uploaded_files:

        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            if menu == "FUCHS":
                df = parse_fuchs_pdf(text)
            else:
                continue

        else:
            if menu == "FUCHS":
                df = parse_fuchs_excel(file)
            else:
                df = pd.read_excel(file)

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    final_df["Тарифен код"] = final_df["Тарифен код"].astype(str)
    final_df = final_df[final_df["Тарифен код"].isin(ALLOWED_CODES)]
    final_df = final_df[final_df["тегло"] > 0]

    st.subheader("📊 Финален отчет")
    st.dataframe(final_df)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        final_df.to_excel(writer, index=False)

    st.download_button(
        "📥 Изтегли Excel",
        data=output.getvalue(),
        file_name="final_report.xlsx"
    )
