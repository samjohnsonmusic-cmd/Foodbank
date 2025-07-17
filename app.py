import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------- CONFIG ---------- #
WARNING_THRESHOLD_DAYS = 5  # Flag items with fewer than this many days left
LOOKBACK_DAYS = 14          # How many past days to analyse usage from

# ---------- FORECAST FUNCTION ---------- #
def forecast_inventory(df):
    df['date'] = pd.to_datetime(df['date'])
    recent_cutoff = datetime.today() - timedelta(days=LOOKBACK_DAYS)
    recent_df = df[df['date'] >= recent_cutoff]

    summary = []

    for item in df['item_name'].unique():
        item_df = df[df['item_name'] == item]
        current_stock = item_df[item_df['type'] == 'in']['quantity'].sum() - \
                        item_df[item_df['type'] == 'out']['quantity'].sum()

        recent_out = recent_df[(recent_df['item_name'] == item) & (recent_df['type'] == 'out')]
        total_out = recent_out['quantity'].sum()
        days = (datetime.today() - recent_cutoff).days or 1
        daily_usage = total_out / days

        if daily_usage > 0:
            days_remaining = current_stock / daily_usage
        else:
            days_remaining = float('inf')

        needs_attention = days_remaining < WARNING_THRESHOLD_DAYS

        summary.append({
            'Item': item,
            'Current Stock': int(current_stock),
            'Avg Daily Usage': round(daily_usage, 2),
            'Days Remaining': round(days_remaining, 1) if days_remaining != float('inf') else 'N/A',
            'Needs Attention': needs_attention
        })

    return pd.DataFrame(summary).sort_values(by='Needs Attention', ascending=False)

# ---------- STREAMLIT UI ---------- #
st.set_page_config(page_title="Inventory Optimisation Tool", layout="wide")
st.title("📊 Inventory Optimisation Assistant")
st.markdown("Upload your inventory log (CSV format). We'll help forecast which items may run low soon.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {'date', 'item_name', 'type', 'quantity'}

        if not required_cols.issubset(df.columns):
            st.error(f"CSV must include the following columns: {required_cols}")
        else:
            forecast_df = forecast_inventory(df)

            st.subheader("Forecast Summary")
            st.dataframe(forecast_df, use_container_width=True)

            warnings = forecast_df[forecast_df['Needs Attention']]
            if not warnings.empty:
                st.warning("The following items may run out soon:")
                for _, row in warnings.iterrows():
                    st.markdown(f"- **{row['Item']}**: {row['Days Remaining']} days left.\n  → Would you like to prepare a donation request?")
            else:
                st.success("All items appear sufficiently stocked for now.")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to begin.")