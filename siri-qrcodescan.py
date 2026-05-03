


import streamlit as st
import qrcode
import pandas as pd
from datetime import datetime
from io import BytesIO
import os
st.markdown(
    """
    <style>
        .stApp {
            background-color: #111;
            color:yellow;
        }
    </style>
    
""", unsafe_allow_html=True)

st.markdown("""
<style>
div.stButton > button {
    background-color: #4CAF10;
    color: black;
    border-radius: 10px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

FILE_NAME="qr_scans.xlsx"

# -------------------------
# INIT EXCEL FILE
# -------------------------
if not os.path.exists(FILE_NAME):
    df_init = pd.DataFrame(columns=["id", "timestamp"])
    df_init.to_excel(FILE_NAME, index=False)

# -------------------------
# QR GENERATOR
# -------------------------
def generate_qr(data):
    qr = qrcode.make(data)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf

# -------------------------
# LOG SCAN (EXCEL)
# -------------------------
def log_scan(qr_id):
    df = pd.read_excel(FILE_NAME)

    new_row = {
        "id": qr_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

# -------------------------
# FETCH DATA
# -------------------------
def get_scan_data():
    df = pd.read_excel(FILE_NAME)
    if not df.empty:
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    return df

# -------------------------
# UI
# -------------------------
st.title("📊 QR Code Tracker ")

tab1, tab2 = st.tabs(["Generate QR", "Analytics"])

# -------------------------
# GENERATE QR
# -------------------------
with tab1:
    st.subheader("Create QR Code")

    destination_url = st.text_input("Enter destination URL")

    if st.button("Generate QR"):
        if destination_url:
            qr_id = str(hash(destination_url))

            tracking_url = f"http://localhost:8501/?scan_id={qr_id}&redirect={destination_url}"

            qr_img = generate_qr(tracking_url)

            st.image(qr_img, caption="Scan this QR")
            st.write("Tracking URL:", tracking_url)

# -------------------------
# TRACK SCAN
# -------------------------
query_params = st.query_params

if "scan_id" in query_params:
    qr_id = query_params["scan_id"]
    redirect_url = query_params.get("redirect", "")

    log_scan(qr_id)

    st.success("✅ Scan recorded!")

    if redirect_url:
        st.markdown(f"Click here to continue]({redirect_url})")

# -------------------------
# ANALYTICS (NO TABLE)
# -------------------------
with tab2:
    st.subheader("📈 Scan Analytics")

    df = get_scan_data()

    if not df.empty:
        summary = df.groupby("date").size().reset_index(name="scans")

        # Total scans
        st.metric("Total Scans", int(summary["scans"].sum()))

        # Chart
        st.line_chart(summary.set_index("date"))

        # Text display
        st.subheader("📅 Date-wise Scans")
        for _, row in summary.iterrows():
            st.write(f"📅 {row['date']} → {row['scans']} scans")

    else:
        st.info("No scans recorded yet.")
