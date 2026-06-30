import streamlit as st

st.title("Jyothy Labs Valuation Engine")

# Input Sliders
wacc = st.slider("WACC (Discount Rate)", 0.05, 0.20, 0.11)
growth = st.slider("Terminal Growth Rate", 0.01, 0.10, 0.05)

# Assumptions
shares = 3672.09
cash = 31003.00

# DCF Math (Simplified for the app)
ufcf = [25615.01, 28688.81, 32131.47, 35987.24, 40305.71]
pv = sum([ufcf[i] / (1+wacc)**(i+1) for i in range(5)])
terminal_val = (ufcf[-1] * (1 + growth)) / (wacc - growth)
pv_terminal = terminal_val / ((1+wacc)**5)

share_price = (pv + pv_terminal + cash) / shares

st.subheader(f"Implied Share Price: ₹ {share_price:,.2f}")
st.write("Adjust the sliders to see how the valuation sensitivity changes.")
