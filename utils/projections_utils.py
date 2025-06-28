import plotly.graph_objects as go

def plot_rent_projection(initial_rent, growth_rate, years):
    rent_projection = [initial_rent * (1 + growth_rate / 100) ** i for i in range(years + 1)]
    return go.Figure().add_trace(go.Scatter(
        x=list(range(years + 1)),
        y=rent_projection,
        mode="lines+markers",
        name="Projected Rent"
    )).update_layout(
        title="Projected Annual Rent",
        xaxis_title="Year",
        yaxis_title="Total Annual Rent ($)",
        template="plotly_white"
    )

def plot_home_value_projection(price, appreciation_rate, years):
    value_projection = [price * (1 + appreciation_rate / 100) ** i for i in range(years + 1)]
    return go.Figure().add_trace(go.Scatter(
        x=list(range(years + 1)),
        y=value_projection,
        mode="lines+markers",
        name="Projected Home Value"
    )).update_layout(
        title="Projected Home Value",
        xaxis_title="Year",
        yaxis_title="Value ($)",
        template="plotly_white"
    )

def plot_cash_flow_projection(initial_rent, rent_growth, inflation, taxes, tax_growth, years):
    cash_flows = []
    for i in range(years + 1):
        rent = initial_rent * (1 + rent_growth / 100) ** i
        operating_expenses = (0.4 * rent) * (1 + inflation / 100) ** i  # assume 40% OPEX baseline
        tax = taxes * (1 + tax_growth / 100) ** i
        net_cash = rent - operating_expenses - tax
        cash_flows.append(net_cash)

    return go.Figure().add_trace(go.Bar(
        x=list(range(years + 1)),
        y=cash_flows,
        name="Projected Cash Flow"
    )).update_layout(
        title="Projected Annual Cash Flow",
        xaxis_title="Year",
        yaxis_title="Cash Flow ($)",
        template="plotly_white"
    )
