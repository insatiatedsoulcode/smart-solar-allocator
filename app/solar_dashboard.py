import json
import pandas as pd
import numpy as np
import streamlit as st
from ollama import chat  # Local Ollama Python client

# ----------------------------------------------------------
# 1️⃣  Compute deterministic allocation using Python
# ----------------------------------------------------------
def compute_allocation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute how much city demand is met by solar vs. grid.
    Adds two new columns:
        - solar_used : kWh supplied by solar
        - grid_used  : kWh supplied by grid
    """
    df = df.copy()
    # amount of demand that can be met by solar
    df["solar_used"] = np.minimum(df["solar_output"], df["city_demand"])
    # remainder met by grid
    df["grid_used"] = np.maximum(df["city_demand"] - df["solar_output"], 0)
    return df


# ----------------------------------------------------------
# 2️⃣  Generate AI insights from summary data
# ----------------------------------------------------------
def generate_insights(summary: dict) -> str:
    """
    Ask the Mistral model (via local Ollama API) for natural-language insights
    based on aggregated summary statistics.
    """
    prompt = (
        "You are an expert energy analyst.\n"
        "Given the following summary of solar power usage, "
        "provide 3–5 bullet points with key insights and recommendations "
        "to improve solar efficiency and reduce grid dependence.\n\n"
        f"Summary Data:\n{json.dumps(summary, indent=2)}"
    )
    try:
        resp = chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.3},  # a bit of creativity
        )
        return resp["message"]["content"]
    except Exception as e:
        return f"⚠️ Error contacting Mistral: {e}"


# ----------------------------------------------------------
# 3️⃣  Streamlit UI
# ----------------------------------------------------------
st.title("⚡ Smart Solar Allocator – Python Computation + Mistral Insights")

uploaded_file = st.file_uploader(
    "Upload a CSV with columns: hour, solar_output, city_demand",
    type=["csv"]
)

if uploaded_file:
    # ---- Load and preview ----
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Input Preview")
    st.dataframe(df.head())

    # ---- Compute allocation in Python ----
    computed_df = compute_allocation(df)

    st.subheader("🔢 Python Computed Allocation")
    st.dataframe(computed_df.head(20))

    # ---- Aggregate summary for AI ----
    summary = {
        "total_hours": int(len(computed_df)),
        "avg_solar_output": round(computed_df["solar_output"].mean(), 2),
        "avg_city_demand": round(computed_df["city_demand"].mean(), 2),
        "avg_solar_used": round(computed_df["solar_used"].mean(), 2),
        "avg_grid_used": round(computed_df["grid_used"].mean(), 2),
        "max_grid_peak": round(computed_df["grid_used"].max(), 2),
        "solar_share_percent": round(
            computed_df["solar_used"].sum() /
            computed_df["city_demand"].sum() * 100, 2
        ),
    }

    st.markdown("### 🔎 Summary for AI")
    st.json(summary)

    # ---- Download deterministic results ----
    st.download_button(
        label="⬇️ Download Python Results CSV",
        data=computed_df.to_csv(index=False),
        file_name="python_computed_allocation.csv",
        mime="text/csv",
    )

    # ---- AI Insights ----
    if st.button("✨ Generate AI Insights with Mistral"):
        st.info("Contacting Mistral model for analysis...")
        insights = generate_insights(summary)
        st.markdown("### 🌐 AI Insights")
        st.write(insights)
else:
    st.info("Please upload a CSV to begin.")
