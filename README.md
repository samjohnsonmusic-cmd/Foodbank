# Inventory Optimisation Assistant

This tool helps foodbanks forecast stock levels and identify items that may run low soon.

## How to Use

1. Upload your food inventory CSV.
2. View forecasted stock depletion.
3. Get alerts for low-stock items.
4. Optionally, prepare donation request messages.

### CSV Format

The CSV must have the following columns:

- `date` (e.g. 2025-07-01)
- `item_name` (e.g. Canned Tomatoes)
- `type` (either `in` or `out`)
- `quantity` (number of units)

### Run the App

To run locally:
```bash
pip install streamlit pandas
streamlit run app.py
```

Or deploy to [Streamlit Cloud](https://streamlit.io/cloud).