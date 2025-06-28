import streamlit as st
import pandas as pd
from utils.projections_utils import plot_rent_projection, plot_home_value_projection, plot_cash_flow_projection

st.title("📈 Long-Term Investment Projections")

# Load Analyzer context
@st.cache_data
def load_data():
    df = pd.read_csv("data/listings.csv")
    df["price_per_unit"] = df["List Price"] / df["Number of Units"]
    df["Full Address"] = df["Street #"].astype(str) + " " + df["Street Name"]
    return df.sort_values(by=["price_per_unit", "Days on Market"])

df = load_data()

# Sidebar Inputs
st.sidebar.header("📊 Growth Assumptions")

# Property selection (same as Analyzer)
selected_address = st.sidebar.selectbox(
    "Select a property to project:",
    df["Full Address"]
)

property_data = df[df["Full Address"] == selected_address].iloc[0]
purchase_price = float(property_data["List Price"])
units = int(property_data["Number of Units"])
initial_rent = float(property_data.get("GrossRents", 1000)) * units
initial_taxes = float(property_data.get("Taxes", 3000))

# --- Sidebar Projections ---
years = 10
rent_growth = st.sidebar.slider("Annual Rent Growth (%)", 0.0, 10.0, 3.0)
home_appreciation = st.sidebar.slider("Annual Home Price Appreciation (%)", 0.0, 10.0, 3.0)
inflation_rate = st.sidebar.slider("Annual Inflation (%)", 0.0, 10.0, 2.5)
tax_growth = st.sidebar.slider("Annual Property Tax Growth (%)", 0.0, 10.0, 2.0)
alt_investment_return = st.sidebar.slider("Investment Return if Not Purchased (%)", 0.0, 12.0, 6.0)

# --- Summary Section ---
st.markdown("### 🏠 Property Summary")
st.markdown(f"""
- **Address:** {selected_address}  
- **Purchase Price:** ${purchase_price:,.0f}  
- **Units:** {units}  
- **Monthly Rent (All Units):** ${initial_rent:,.0f}  
- **Annual Property Taxes:** ${initial_taxes:,.0f}
""")

# --- Charts ---
st.markdown("### 📊 Projections Over 10 Years")

st.plotly_chart(
    plot_rent_projection(initial_rent, rent_growth, years),
    use_container_width=True
)

st.plotly_chart(
    plot_home_value_projection(purchase_price, home_appreciation, years),
    use_container_width=True
)

st.plotly_chart(
    plot_cash_flow_projection(initial_rent, rent_growth, inflation_rate, initial_taxes, tax_growth, years),
    use_container_width=True
)
