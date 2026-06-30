import pandas as pd

def calculate_dcf():
    print("\n--- Initiating Jyothy Labs DCF Model ---")
    
    # 1. Valuation Assumptions
    wacc = 0.11
    terminal_growth = 0.05
    shares_outstanding = 3672.09 
    cash_and_equiv = 31003.00
    total_debt = 0.00
    
    # 2. Forecasted Unlevered Free Cash Flows (FY27 to FY31)
    years = [1, 2, 3, 4, 5]
    ufcf = [25615.01, 28688.81, 32131.47, 35987.24, 40305.71]
    
    # Create a Pandas DataFrame to display the forecast
    dcf_df = pd.DataFrame({
        'Year': years,
        'UFCF': ufcf
    })
    
    # 3. Time Value of Money (Discounting)
    dcf_df['Discount_Factor'] = (1 + wacc) ** dcf_df['Year']
    dcf_df['PV_of_UFCF'] = dcf_df['UFCF'] / dcf_df['Discount_Factor']
    
    pv_of_5yr_cash = dcf_df['PV_of_UFCF'].sum()
    
    # 4. Terminal Value Calculation (Gordon Growth Model)
    final_year_cash = ufcf[-1]
    terminal_value = (final_year_cash * (1 + terminal_growth)) / (wacc - terminal_growth)
    
    # Discount the Terminal Value back to Year 0 
    pv_of_terminal_value = terminal_value / ((1 + wacc) ** 5)
    
    # 5. Enterprise Value to Equity Value Bridge
    enterprise_value = pv_of_5yr_cash + pv_of_terminal_value
    equity_value = enterprise_value + cash_and_equiv - total_debt
    
    # 6. Implied Share Price
    implied_share_price = equity_value / shares_outstanding
    
    # 7. Output Results
    print(dcf_df.round(2).to_string(index=False))
    print("-" * 40)
    print(f"PV of 5-Year FCFs:    INR {pv_of_5yr_cash:,.2f}")
    print(f"Terminal Value:       INR {terminal_value:,.2f}")
    print(f"PV of Terminal Value: INR {pv_of_terminal_value:,.2f}")
    print(f"Enterprise Value:     INR {enterprise_value:,.2f}")
    print(f"Equity Value:         INR {equity_value:,.2f}")
    print("=" * 40)
    print(f"IMPLIED SHARE PRICE:  INR {implied_share_price:,.2f}")
    print("=" * 40)

# Run the function
calculate_dcf()