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
    background: rgba(255,255,255,0.00) !important;  /* почти прозрачно */

    backdrop-filter: blur(18px) saturate(140%);
    -webkit-backdrop-filter: blur(18px) saturate(140%);

    border-right: 4px solid rgba(255,255,255,0.7);  /* силен метален борд */

    /* ✅ вътрешен glow */
    box-shadow:
        inset 0 0 10px rgba(255,255,255,0.15),
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
# ✅ FINAL UI (RESET + FIXED ORDER)
# ======================================================

st.markdown("""
<style>
.source-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

/* ✅ Add file малък и прозрачен */
.add-file {
    display:inline-block;
    background: rgba(255,255,255,0.04);
    border-radius: 6px;
    padding: 3px 10px;
    color: white;
    font-size: 14px;
    font-weight: 400;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


# ✅ SIDEBAR (с reset логика)
menu = st.sidebar.selectbox("Suppliers", ["Castrol", "MOTUL"])

# ✅ пазим предишния supplier
if "prev_supplier" not in st.session_state:
    st.session_state["prev_supplier"] = menu

# ✅ АКО смениш supplier → reset
if st.session_state["prev_supplier"] != menu:
    st.session_state["source_type"] = ""   # reset PDF/Excel
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


# ✅ цветове + текст
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


# ✅ бутон стил
st.markdown(f"""
<style>

/* PDF */
div[data-testid="column"]:nth-of-type(1) button {{
    background-color: {pdf_color};
    height: 60px;
    border-radius: 12px;
}}

/* Excel */
div[data-testid="column"]:nth-of-type(2) button {{
    background-color: {excel_color};
    height: 60px;
    border-radius: 12px;
}}

</style>
""", unsafe_allow_html=True)


# ✅ overlay текст вдясно
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


# ✅ ✅ ADD FILE НАД UPLOAD (малък)
st.markdown("<div class='add-file'>Add file</div>", unsafe_allow_html=True)


# ✅ UPLOAD (под него)
uploaded_files = st.file_uploader(
    "",
    type=["pdf"] if source_type == "PDF" else ["xlsx", "xls"],
    accept_multiple_files=True
)

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
