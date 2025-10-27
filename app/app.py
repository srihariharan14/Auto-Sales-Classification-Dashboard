import dash
import pandas as pd
import os
import pickle
from dash import html # Corrected deprecated import
from app.callbacks import register_callbacks
from app.components import create_header, create_filter_controls, create_sales_trend_chart, \
    create_category_performance_chart, create_regional_heatmap, create_success_classification_chart, \
    create_layout_container, create_kpi_cards

# --- 1. Load Data and Model ---
# Construct paths relative to the current file location (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'processed', 'cleaned_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, '..', 'data', 'model', 'classification_model.pkl')

try:
    df = pd.read_csv(PROCESSED_DATA_PATH)
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✅ Data and Model loaded successfully.")
except FileNotFoundError:
    print(f"FATAL ERROR: Data files not found.")
    print("Please run the setup script: python setup_pipeline_data.py")
    # Use an empty DataFrame if files are missing to prevent crash on layout creation
    df = pd.DataFrame({
        'Manufacturer': [], 'Region': [], 'SalesVolume': [], 'Price_k': [], 
        'Is_Success': [], 'TimePeriod': [], 'Sales_Category': []
    })

# --- 2. Initialize App and Server ---
# Use suppress_callback_exceptions=True for layout elements that are generated later
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server # Required for gunicorn/cloud deployment

# --- 3. Assemble Layout ---
app_title = "Automobile Sales Classification Dashboard"

# Create individual components
header_content = create_header(app_title)
kpis = create_kpi_cards(df)
filters = create_filter_controls(df)
charts = [
    create_sales_trend_chart(df),
    create_regional_heatmap(df),
    html.Div([
        create_category_performance_chart(df),
        create_success_classification_chart(df)
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around'})
]

# Assemble the final layout
app.layout = create_layout_container(header_content, kpis, filters, charts)


# --- 4. Register Callbacks ---
# This activates the interactivity defined in app/callbacks.py
register_callbacks(app, df)


# --- 5. Run the Application ---
if __name__ == '__main__':
    # Using app.run() for modern Dash compatibility
    app.run(debug=True, host='0.0.0.0', port=8050)
