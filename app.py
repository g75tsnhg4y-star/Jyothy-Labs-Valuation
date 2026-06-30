import streamlit as st
import pandas as pd
import numpy as np
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Jyothy Labs Valuation Dashboard", page_icon="📈", layout="wide")

# --- SIDEBAR: RESUME & DOWNLOAD ---
st.sidebar.header("👨‍💻 Analyst Profile")
st.sidebar.markdown("""
**Financial Modelling:**
Three-statement models, DCF/FCFF/FCFE, DDM, residual income, SoTP, relative valuation - advanced.

**Data & Analytics:**
Advanced Excel (VBA, Power Query, dynamic arrays, scenario analysis), Python (pandas, NumPy, portfolio back testing, factor return analytics), R (econometrics, OLS regression).

**Market Data Platforms:**
Bloomberg Terminal (EQS, FA, EE, PORT, Excel API), CMIE Prowess, Refinitiv/Eikon.

**Presentation & Research:**
PowerPoint (investment decks, IC presentations), Word (formal research notes).
""")

st.sidebar.divider()
st.sidebar.subheader("📥 Deep Dive Analysis")
st.sidebar.write("Download the full integrated 3-statement model and historical working capital schedules.")

# Robust Download Button (prevents crashes if file is missing)
excel_file = "Jyothy_Labs_DCF.xlsx"
if os.path.exists(excel_file):
    with open(excel_file, "rb") as file:
        st.sidebar.download_button(
            label="📄 Download Full Excel Model",
            data=file,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.sidebar.warning("⚠️ Please upload 'Jyothy_Labs_DCF.xlsx' to GitHub to enable the download link.")

# --- MAIN DASHBOARD ---
st.title("📊 Jyothy Labs - Interactive DCF Engine")
st.write("An automated Discounted Cash Flow engine mapping real-time valuation sensitivity.")

# --- INPUT PANEL (COLUMNS) ---
st.markdown("### 🎛️ Control Panel")
col1, col2, col3 = st.columns(3)
with col1:
    wacc = st.slider("WACC (Discount Rate)", 0.05, 0.20, 0.11, format="%.2f")
with col2:
    growth = st.slider("Terminal Growth Rate", 0.01, 0.10, 0.05, format="%.2f")
with col3:
    shares = st.number_input("Shares Outstanding (Cr)", value=3672.09)

# --- VALUATION ENGINE (MATH) ---
cash = 31003.00
ufcf = [25615.01, 28688.81, 32131.47, 35987.24, 40305.71]
years = ["FY27", "FY28", "FY29", "FY30", "FY31"]

# PV of Cash Flows
pv = sum([ufcf[i] / (1+wacc)**(i+1) for i in range(5)])
# Terminal Value
terminal_val = (ufcf[-1] * (1 + growth)) / (wacc - growth)
pv_terminal = terminal_val / ((1+wacc)**5)
# Bridge
enterprise_value = pv + pv_terminal
equity_value = enterprise_value + cash
share_price = equity_value / shares

# --- TABS FOR ORGANIZATION ---
tab1, tab2, tab3 = st.tabs(["🧮 Valuation Output", "🔬 Scenario Matrix", "📘 Methodology"])

with tab1:
    st.markdown("### 🏆 Output & Bridge to Equity")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Implied Share Price", f"₹ {share_price:,.2f}")
    metric_col2.metric("Enterprise Value", f"₹ {enterprise_value:,.2f}")
    metric_col3.metric("Equity Value", f"₹ {equity_value:,.2f}")
    
    st.divider()
    st.markdown("### 📈 Forecasted Unlevered Free Cash Flows")
    df = pd.DataFrame({"Financial Year": years, "UFCF (INR)": ufcf})
    chart_col, table_col = st.columns([2, 1])
    with chart_col:
        st.bar_chart(df.set_index("Financial Year"), color="#4CAF50")
    with table_col:
        st.dataframe(df, hide_index=True, use_container_width=True)

with tab2:
    st.markdown("### 🌡️ Implied Share Price Sensitivity Matrix")
    st.write("Dynamic scenario analysis flexed across Discount Rates and Terminal Growth.")
    
    # Generate dynamic sensitivity table
    wacc_range = [wacc - 0.02, wacc, wacc + 0.02]
    growth_range = [growth - 0.01, growth, growth + 0.01]
    
    matrix = []
    for g in growth_range:
        row = []
        for w in wacc_range:
            if w <= g:
                row.append(None) # Prevent math errors if growth > wacc
            else:
                t_val = (ufcf[-1] * (1 + g)) / (w - g)
                pv_t = t_val / ((1+w)**5)
                pv_c = sum([ufcf[i] / (1+w)**(i+1) for i in range(5)])
                eq_val = pv_c + pv_t + cash
                row.append(round(eq_val / shares, 2))
        matrix.append(row)
        
    sens_df = pd.DataFrame(matrix, 
                           index=[f"Growth {g*100:.1f}%" for g in growth_range],
                           columns=[f"WACC {w*100:.1f}%" for w in wacc_range])
    
    st.dataframe(sens_df.style.background_gradient(cmap="Greens", axis=None), use_container_width=True)

with tab3:
    st.markdown("### 🏛️ Valuation Methodology")
    st.write("This model utilizes a two-stage Discounted Cash Flow methodology. Unlevered Free Cash Flows are discounted to present value using the Weighted Average Cost of Capital (WACC).")
    
    st.write("Terminal Value is calculated utilizing the Gordon Growth Model:")
    st.latex(r"Terminal Value = \frac{FCF_{n} \times (1 + g)}{(WACC - g)}")
    
    st.write("The Enterprise Value to Equity Value bridge incorporates current cash equivalents and total debt to arrive at the final implied per-share valuation.")
