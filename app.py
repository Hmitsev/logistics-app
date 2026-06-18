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
# ✅ CASTROL (СТАРАТА РАБОТЕЩА ЛОГИКА)
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
# ✅ MOTUL (ФИНАЛНА РАБОТЕЩА ВЕРСИЯ)
# ======================================================
def parse_motul(text):

    rows = []
    lines = text.split("\n")

    for i, line in enumerate(lines):

        match = re.findall(r'(\d{1,4})\s+(\d{1,3}(?:\s\d{3})*,\d+)', line)

        if match:
            try:
                qty = float(match[0][0])
                weight = float(match[0][1].replace(" ", "").replace(",", "."))

                # ✅ код
                code = None
                for j in range(i, min(i + 6, len(lines))):
                    code_match = re.search(r'\b\d{8}\b', lines[j])
                    if code_match:
                        code = code_match.group(0)
                        break

                # ✅ wid
                wid = 1
                for j in range(max(0, i - 8), i + 1):
                    l = lines[j].upper()

                    match_pack = re.search(r'(\d+)X(\d+)L', l)
                    match_l = re.search(r'(\d+)L', l)

                    if match_pack:
                        wid = float(match_pack.group(2))
                    elif match_l:
                        wid = float(match_l.group(1))

                    if "0.500L" in l:
                        wid = 0.5
                    elif "0.250L" in l:
                        wid = 0.25

                if code:
                    rows.append({
                        "Тарифен код": code,
                        "Количество": qty,
                        "wid": wid,
                        "kolichestvo": qty * wid,
                        "тегло": weight
                    })

            except:
                pass

    return pd.DataFrame(rows)


# ======================================================
# ✅ FINAL REPORT (СЪЩИЯ КАТО ВЧЕРА)
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
