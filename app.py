import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jyothy Labs Valuation", layout="centered")

st.title("📊 Jyothy Labs DCF Valuation")
st.write("An automated Discounted Cash Flow (DCF) engine mapping real-time valuation sensitivity.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Valuation Assumptions")
wacc = st.sidebar.slider("WACC (Discount Rate)", 0.05, 0.20, 0.11, format="%.2f")
growth = st.sidebar.slider("Terminal Growth Rate", 0.01, 0.10, 0.05, format="%.2f")

# --- DCF MATH ---
shares = 3672.09
cash = 31003.00
ufcf = [25615.01, 28688.81, 32131.47, 35987.24, 40305.71]
years = ["FY27", "FY28", "FY29", "FY30", "FY31"]

pv = sum([ufcf[i] / (1+wacc)**(i+1) for i in range(5)])
terminal_val = (ufcf[-1] * (1 + growth)) / (wacc - growth)
pv_terminal = terminal_val / ((1+wacc)**5)

share_price = (pv + pv_terminal + cash) / shares

# --- DASHBOARD UI ---
st.divider()

# Big Number Display
st.metric(label="Implied Share Price", value=f"₹ {share_price:,.2f}")

st.divider()

# Excel-style Data Table
st.subheader("Forecasted Unlevered Free Cash Flows (UFCF)")
df = pd.DataFrame({"Financial Year": years, "UFCF (INR)": ufcf})
st.dataframe(df, hide_index=True, use_container_width=True)

# Visual Chart
st.subheader("Cash Flow Trajectory")
st.bar_chart(df.set_index("Financial Year"))
