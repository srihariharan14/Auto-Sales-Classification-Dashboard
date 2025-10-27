import dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Define the path to the processed data
# Note: The data is loaded in app.py, this path is redundant but kept for context if needed.
# However, we rely on the DataFrame passed into register_callbacks.

def register_callbacks(app, df):
    """
    Registers the main callback function to update all charts and KPIs.
    
    Args:
        app (dash.Dash): The Dash application instance.
        df (pd.DataFrame): The full, loaded dataset.
    """

    @app.callback(
        [Output('kpi-total-sales', 'children'),
         Output('kpi-avg-price', 'children'),
         Output('kpi-success-rate', 'children'),
         Output('sales-trend-graph', 'figure'),
         Output('category-performance-graph', 'figure'),
         Output('regional-heatmap', 'figure'),
         Output('success-classification-graph', 'figure')],
        [Input('manufacturer-filter', 'value'),
         Input('region-filter', 'value'),
         Input('sales-category-radio', 'value')]
    )
    def update_dashboard(selected_manufacturers, selected_regions, selected_category):
        """Filters the DataFrame and regenerates all visualizations and KPIs."""
        
        # --- 1. Filter Data ---
        
        # Filter by Manufacturer and Region (multi-select dropdowns)
        filtered_df = df[
            (df['Manufacturer'].isin(selected_manufacturers)) &
            (df['Region'].isin(selected_regions))
        ]

        # Filter by Sales Category (radio items)
        if selected_category and selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Sales_Category'] == selected_category]

        # Handle empty DataFrame case gracefully
        if filtered_df.empty:
            empty_fig = go.Figure().update_layout(title="No data to display based on filters.")
            
            # Return placeholder values for KPIs and charts
            return (
                "0", "$0k", "0.0%", empty_fig, empty_fig, empty_fig, empty_fig
            )

        # --- 2. Update KPIs ---
        
        total_sales = filtered_df['SalesVolume'].sum()
        avg_price = filtered_df['Price_k'].mean().round(1)
        success_rate = filtered_df['Is_Success'].mean() * 100
        
        kpi_sales = f"{total_sales:,.0f}"
        kpi_price = f"${avg_price}k"
        kpi_success = f"{success_rate:.1f}%"


        # --- 3. Update Sales Trend Chart (Line Chart) ---
        
        trend_data = filtered_df.groupby('TimePeriod')['SalesVolume'].sum().reset_index()
        fig_trend = px.line(
            trend_data, 
            x='TimePeriod', 
            y='SalesVolume', 
            title='Sales Volume Trend Over Time',
            template='plotly_white'
        )
        fig_trend.update_layout(title_x=0.5, margin=dict(t=50, b=50))


        # --- 4. Update Category Performance (Bar Chart) ---
        
        category_data = filtered_df.groupby('Sales_Category')['Price_k'].mean().reset_index()
        fig_category = px.bar(
            category_data,
            x='Sales_Category',
            y='Price_k',
            title='Average Price by Sales Category (k)',
            template='plotly_white',
            color='Sales_Category'
        )
        fig_category.update_layout(title_x=0.5, margin=dict(t=50, b=50))

        # --- 5. Update Regional Heatmap ---
        
        heatmap_data = filtered_df.groupby(['Region', 'Manufacturer'])['SalesVolume'].sum().reset_index()
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data['SalesVolume'],
            x=heatmap_data['Region'],
            y=heatmap_data['Manufacturer'],
            colorscale='Viridis',
        ))
        
        fig_heatmap.update_layout(
            title='Sales Volume Heatmap by Region and Manufacturer',
            xaxis_title='Region',
            yaxis_title='Manufacturer',
            title_x=0.5,
            margin=dict(t=50, b=50)
        )
        
        # --- 6. Update Classification Distribution Chart (Pie Chart) ---

        success_counts = filtered_df['Is_Success'].map({1: 'Successful Sales', 0: 'Unsuccessful Sales'}).value_counts().reset_index()
        success_counts.columns = ['Classification', 'Count']
        
        fig_success = px.pie(
            success_counts,
            names='Classification',
            values='Count',
            title='Sales Classification Distribution (Target Variable)',
            template='plotly_white',
            color_discrete_sequence=['#4CAF50', '#F44336']
        )
        fig_success.update_layout(title_x=0.5, margin=dict(t=50, b=50))


        # --- 7. Return All Outputs ---
        
        return (kpi_sales, kpi_price, kpi_success, fig_trend, fig_category, fig_heatmap, fig_success)
