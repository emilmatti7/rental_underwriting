def run_underwriting(
    price, units, down_payment_pct, interest_rate, loan_term,
    pm_fee, vacancy, capex, rents, taxes, insurance,
    utilities, mortgage_payment, mortgage_insurance
):
    annual_gross_income = rents * 12

    total_expenses = (
        vacancy +  # already annualized
        pm_fee +
        capex +
        taxes +
        insurance +
        utilities +
        mortgage_insurance +
        mortgage_payment * 12
    )

    noi = annual_gross_income - (total_expenses - (mortgage_payment * 12))
    cash_flow = annual_gross_income - total_expenses
    down_payment = price * (down_payment_pct / 100)
    cash_on_cash = (cash_flow / down_payment) * 100 if down_payment > 0 else 0
    cap_rate = (noi / price) * 100 if price > 0 else 0

    return {
        "Gross Rent (Annual)": f"${annual_gross_income:,.0f}",
        "NOI": f"${noi:,.0f}",
        "Annual Debt Service": f"${mortgage_payment * 12:,.0f}",
        "Cash Flow (Annual)": f"${cash_flow:,.0f}",
        "Cap Rate": f"{cap_rate:.2f}%",
        "Cash-on-Cash Return": f"{cash_on_cash:.2f}%"
    }
