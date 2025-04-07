import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Buy vs Rent Decision Framework", layout="wide")

st.title("🏠 Buy vs Rent Decision Framework")

st.markdown("""
This app helps you analyze whether it's financially better to buy or rent a property based on the opportunity cost
of your initial investment. The framework considers what return you could get by investing your initial costs
(down payment, taxes, etc.) in the S&P 500 instead.
""")

# Sidebar inputs
st.sidebar.header("Input Parameters")

# Initial costs
st.sidebar.subheader("Initial Costs")
down_payment = st.sidebar.number_input("Down Payment (€)", min_value=0, value=40000, step=5000)
taxes = st.sidebar.number_input("Taxes (IMT, IS) (€)", min_value=0, value=5000, step=1000)
other_costs = st.sidebar.number_input("Other Transaction Costs (€)", min_value=0, value=5000, step=1000)

total_initial_cost = down_payment + taxes + other_costs

# Investment return
st.sidebar.subheader("Investment Parameters")
annual_return = st.sidebar.slider("Expected Annual Return (%)", min_value=1, max_value=15, value=10)
monthly_return = total_initial_cost * (annual_return/100 / 12)

# Rent range
st.sidebar.subheader("Rent Analysis Range")
min_rent = st.sidebar.number_input("Minimum Monthly Rent (€)", min_value=0, value=300, step=100)
max_rent = st.sidebar.number_input("Maximum Monthly Rent (€)", min_value=0, value=1200, step=100)

# Main area calculations and display
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visual Analysis")

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    rendas_mensais = np.linspace(min_rent, max_rent, 50)

    ax.plot(rendas_mensais, rendas_mensais, label='Cost of Renting', color='blue')
    ax.axhline(y=monthly_return, color='r', linestyle='--',
               label=f'Monthly Return on Initial Investment (≈{monthly_return:.2f}€)')

    ax.fill_between(rendas_mensais, rendas_mensais, monthly_return,
                    where=(rendas_mensais > monthly_return),
                    color='green', alpha=0.3, label='Favors Buying')
    ax.fill_between(rendas_mensais, rendas_mensais, monthly_return,
                    where=(rendas_mensais < monthly_return),
                    color='red', alpha=0.3, label='Favors Renting')

    ax.set_xlabel('Monthly Rent (€)')
    ax.set_ylabel('Monthly Cost (€)')
    ax.set_title('Buy vs Rent Decision Framework')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Add explanatory text
    plt.text(min_rent + (max_rent-min_rent)*0.1,
             monthly_return + (max_rent-min_rent)*0.3,
             'If rent > potential return → Buy\n\n' +
             'If rent < potential return → Rent',
             bbox=dict(facecolor='white', alpha=0.8))

    st.pyplot(fig)

with col2:
    st.subheader("Summary")

    st.markdown("#### Initial Investment")
    st.info(f"Total Initial Cost: €{total_initial_cost:,.2f}")

    st.markdown("#### Monthly Return")
    st.success(f"Expected Monthly Return: €{monthly_return:.2f}")

    st.markdown("#### Decision Framework")
    st.markdown("""
    - If your monthly rent is **above** €{:.2f}, buying might be more advantageous
    - If your monthly rent is **below** €{:.2f}, renting might be more advantageous
    """.format(monthly_return, monthly_return))

    st.markdown("#### Important Notes")
    st.warning("""
    This is a simplified analysis that doesn't include:
    - Property appreciation
    - Maintenance costs
    - Property taxes (IMI)
    - Condo fees
    - Insurance costs
    - Mortgage interest
    """)

st.markdown("---")
st.markdown("""
### How to Use This Framework

1. Input your specific values in the sidebar:
   - Initial costs (down payment, taxes, etc.)
   - Expected investment return
   - Rent range for analysis

2. The graph will show:
   - Blue line: Cost of renting
   - Red dashed line: Monthly return you could get from investing initial costs
   - Green area: Where buying might be better
   - Red area: Where renting might be better

3. Use the summary section to understand the specific breakeven point for your situation
""")
