import streamlit as st
import pandas as pd
from utils.analyzer_utils import run_underwriting

# -- Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/listings.csv")
    df["price_per_unit"] = df["List Price"] / df["Number of Units"]
    df["Full Address"] = df["Street #"].astype(str) + " " + df["Street Name"]
    return df.sort_values(by=["price_per_unit", "Days on Market"])

df = load_data()

# -- Sidebar Inputs
st.sidebar.header("📊 Underwriting Inputs")

# Property selection
selected_address = st.sidebar.selectbox(
    "Select a property to analyze:",
    df["Full Address"]
)

# Selected property data
property_data = df[df["Full Address"] == selected_address].iloc[0]

# --- Property Info ---
st.sidebar.subheader("🏠 Property Information")

purchase_price = st.sidebar.text_input("Purchase Price ($)", value=str(round(property_data["List Price"])))
down_payment_pct = st.sidebar.slider("Down Payment (%)", 10, 40, 20)
interest_rate = st.sidebar.text_input("Interest Rate (%)", value="7.5")
loan_term_months = 360  # 30-year fixed

# Number of units input
units = st.sidebar.number_input("Number of Units", min_value=1, max_value=50, value=int(property_data.get("Number of Units", 5)))

# --- Income ---
st.sidebar.subheader("💰 Income (Monthly per Unit)")

unit_rents = []
for i in range(units):
    rent_input = st.sidebar.text_input(f"Unit {i+1} Rent ($)", value="1000", key=f"unit_rent_{i}")
    try:
        unit_rents.append(float(rent_input))
    except:
        unit_rents.append(0.0)

gross_monthly_income = sum(unit_rents)
st.sidebar.markdown(f"**Total Gross Income: ${gross_monthly_income:,.0f}**")

# --- Expenses ---
st.sidebar.subheader("📉 Expenses (Monthly)")

# Calculate estimated mortgage payment
try:
    price = float(purchase_price)
    down_payment = price * (down_payment_pct / 100)
    loan_amount = price - down_payment
    monthly_interest = float(interest_rate) / 100 / 12
    mortgage_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** loan_term_months) / ((1 + monthly_interest) ** loan_term_months - 1)
except:
    mortgage_payment = 0.0

st.sidebar.markdown(f"**Est. Mortgage Payment: ${mortgage_payment:,.0f}**")

# Expense inputs (monthly)
property_tax = st.sidebar.text_input("Property Tax ($)", value="0")
insurance = st.sidebar.text_input("Landlord Insurance ($)", value="0")
mortgage_insurance = st.sidebar.text_input("Mortgage Insurance Premium ($)", value="0")
pm_fee_pct = st.sidebar.text_input("Property Management Fee (% of income)", value="10")
utilities = st.sidebar.text_input("Utilities ($)", value="0")
capex = st.sidebar.text_input("Maintenance & Capex Reserves ($)", value="0")
other_expenses = st.sidebar.text_input("Other Expenses ($)", value="0")
vacancy_pct = st.sidebar.text_input("Vacancy (% of income)", value="5")
try:
    vacancy_amt = gross_monthly_income * (float(vacancy_pct) / 100) * 12
except:
    vacancy_amt = 0


# --- Main Content ---
st.title("🏘️ Multifamily Deal Analyzer")

st.markdown("### 🔎 Listings Overview (Sorted by Price/Unit and Days on Market)")

st.dataframe(
    df[["Full Address", "Town", "Number of Units", "List Price", "price_per_unit", "Days on Market"]],
    use_container_width=True
)

st.markdown("---")
st.markdown(f"### 📍 Selected Property: **{selected_address}**")
# -- Run Analysis Button
if st.button("Run Analysis"):

    try:
        # Convert to numeric safely
        taxes = float(property_tax) * 12
        insurance = float(insurance) * 12
        mortgage_ins = float(mortgage_insurance) * 12
        utilities = float(utilities) * 12
        capex = float(capex) * 12
        other = float(other_expenses) * 12
        pm_fee = float(pm_fee_pct) / 100 * gross_monthly_income * 12

        results = run_underwriting(
            price=price,
            units=units,
            down_payment_pct=down_payment_pct,
            interest_rate=float(interest_rate),
            loan_term=30,
            pm_fee=pm_fee,
            vacancy=vacancy_amt,
            capex=capex,
            rents=gross_monthly_income,
            taxes=taxes,
            insurance=insurance,
            utilities=utilities + other,
            mortgage_payment=mortgage_payment,
            mortgage_insurance=mortgage_ins
        )

        st.markdown("### 📈 Deal Summary")
        st.write(results)

    except Exception as e:
        st.error(f"Error running analysis: {e}")
