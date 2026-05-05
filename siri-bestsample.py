import streamlit as st
import pandas as pd
import numpy as np
st.markdown("""
    <style>
    .stApp {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: black;
    }

    h1, h2, h3 {
        text-align: center;
        color: #ffffff;
    }

    .stButton>button {
        background-color: #ff7eb3;
        color: brown;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #ff2d94;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)
st.title("📊 Smart Sampling App (Low Bias using Standard Deviation)")

# ===== Upload Dataset =====
file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.write("📂 Dataset Preview:")
    st.dataframe(df.head())

    # ===== Select Column =====
    column = st.selectbox(
        "Select Numeric Column",
        df.select_dtypes(include=np.number).columns
    )

    if column:
        data = df[column].dropna().values

        # ===== Population Stats =====
        pop_std = np.std(data)
        pop_mean = np.mean(data)

        st.write(f"📈 Population Mean: {pop_mean:.4f}")
        st.write(f"📉 Population Std Dev: {pop_std:.4f}")

        # ===== Sample Size =====
        sample_size = st.slider("Sample Size", 5, len(data), 20)

        if st.button("Generate Low-Bias Sample"):

            best_sample = None
            min_diff = float("inf")

            # Try multiple samples
            for _ in range(200):
                sample = np.random.choice(data, size=sample_size, replace=False)

                sample_std = np.std(sample)
                diff = abs(pop_std - sample_std)

                if diff < min_diff:
                    min_diff = diff
                    best_sample = sample

            # ===== Results =====
            st.subheader("✅ Best Sample Found")

            st.write("Sample Values:")
            st.write(best_sample)

            st.write(f"Sample Mean: {np.mean(best_sample):.4f}")
            st.write(f"Sample Std Dev: {np.std(best_sample):.4f}")
            st.write(f"Difference from Population SD: {min_diff:.4f}")

            # ===== Comparison =====
            st.subheader("📊 Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Population")
                st.write(f"Mean: {pop_mean:.2f}")
                st.write(f"Std Dev: {pop_std:.2f}")

            with col2:
                st.write("Sample")
                st.write(f"Mean: {np.mean(best_sample):.2f}")
                st.write(f"Std Dev: {np.std(best_sample):.2f}")