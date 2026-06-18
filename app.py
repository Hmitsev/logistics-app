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
# ✅ FINAL UI (WORKING + COLORED TEXT INSIDE)
# ======================================================

st.markdown("""
<style>
.source-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ✅ заглавие
st.markdown('<div class="source-title">👇 Choose Source</div>', unsafe_allow_html=True)


# ✅ STATE
if "source_type" not in st.session_state:
    st.session_state["source_type"] = ""


# ✅ ЛОГИКА ЗА ТЕКСТ + ЦВЯТ
if st.session_state["source_type"] == "PDF":
    pdf_label = "You chose: PDF"
    excel_label = "Excel"

    pdf_color = "#ff3b3b"
    excel_color = "#444"

    pdf_text_color = "#ff3b3b"
    excel_text_color = "white"

elif st.session_state["source_type"] == "Excel":
    pdf_label = "PDF"
    excel_label = "You chose: Excel"

    pdf_color = "#444"
    excel_color = "#36c165"

    pdf_text_color = "white"
    excel_text_color = "#36c165"

else:
    pdf_label = "PDF"
    excel_label = "Excel"

    pdf_color = "#444"
    excel_color = "#444"

    pdf_text_color = "white"
    excel_text_color = "white"


# ✅ БУТОНИ
col1, col2 = st.columns(2)

with col1:
    if st.button(pdf_label, key="pdf_btn", use_container_width=True):
        st.session_state["source_type"] = "PDF"
        st.rerun()

with col2:
    if st.button(excel_label, key="excel_btn", use_container_width=True):
        st.session_state["source_type"] = "Excel"
        st.rerun()


# ✅ ОЦВЕТЯВАНЕ НА БУТОНИТЕ + ТЕКСТА
st.markdown(f"""
<style>

/* PDF бутон */
button#pdf_btn {{
    background-color: {pdf_color} !important;
    color: {pdf_text_color} !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    height: 60px !important;
}}

/* Excel бутон */
button#excel_btn {{
    background-color: {excel_color} !important;
    color: {excel_text_color} !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    height: 60px !important;
}}

</style>
""", unsafe_allow_html=True)


# ✅ ADD FILE
st.markdown(
    "<div style='font-size:20px; font-weight:900; color:white; margin-top:15px;'>Add file</div>",
    unsafe_allow_html=True
)


# ✅ UPLOADER
uploaded_files = st.file_uploader(
    "",
    type=["pdf"] if st.session_state["source_type"] == "PDF" else ["xlsx", "xls"],
    accept_multiple_files=True
)


# ✅ SIDEBAR
menu = st.sidebar.selectbox("Suppliers", ["Castrol", "MOTUL"])


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
