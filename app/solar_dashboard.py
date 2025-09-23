import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("☀️ Smart Solar Allocator (Prototype)")
st.write("Upload a CSV with `hour,solar_output,city_demand` to simulate energy allocation.")

uploaded_file = st.file_uploader("Upload solar_data.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []

    for _, row in df.iterrows():
        hour = int(row["hour"])
        solar_output = float(row["solar_output"])
        city_demand = float(row["city_demand"])
        
        solar_used = min(solar_output, city_demand)
        grid_used = city_demand - solar_used

        results.append({"hour": hour, "solar_used": solar_used, "grid_used": grid_used})

    results_df = pd.DataFrame(results)
    st.subheader("📊 Allocation Results")
    st.dataframe(results_df)

    # Plot
    fig, ax = plt.subplots()
    ax.plot(results_df["hour"], results_df["solar_used"], marker="o", label="Solar Usage")
    ax.plot(results_df["hour"], results_df["grid_used"], marker="o", label="Grid Usage")
    ax.set_xlabel("Hour")
    ax.set_ylabel("kWh")
    ax.set_title("Solar vs Grid Allocation")
    ax.legend()
    st.pyplot(fig)

