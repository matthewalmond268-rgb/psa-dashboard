import pandas as pd
import streamlit as st

st.title("PSA Threshold Explorer")

df = pd.read_csv("psa_results.csv")

threshold = st.slider(
    "Threshold (£/QALY)",
    min_value=0,
    max_value=5000,
    value=1000,
    step=50
)

st.write(f"Current threshold: £{threshold}")

df["NMB_NT"] = threshold * df["QALY_NT"] - df["Cost_NT"]
df["NMB_EST"] = threshold * df["QALY_EST"] - df["Cost_EST"]
df["NMB_ANG"] = threshold * df["QALY_ANG"] - df["Cost_ANG"]

df["Optimal"] = df[["NMB_NT", "NMB_EST", "NMB_ANG"]].idxmax(axis=1)
df["Optimal"] = df["Optimal"].str.replace("NMB_", "")


probs = (
    df["Optimal"]
    .value_counts(normalize=True)
    .reindex(["NT", "EST", "ANG"], fill_value=0)
)

st.subheader("Probability optimal")
st.write(probs)
st.bar_chart(probs)

st.subheader("Mean NMB")
st.write(df[["NMB_NT", "NMB_EST", "NMB_ANG"]].mean())
