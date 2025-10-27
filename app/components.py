import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
# --- FIXED IMPORTS ---
from dash import dcc # Replaces import dash_core_components as dcc
from dash import html # Replaces import dash_html_components as html
# ---------------------

# Global styling dictionary
TEXT_STYLE = {
    'color': '#111111',
    'textAlign': 'center',
    'fontFamily': 'Arial, sans-serif'
}

# --- 1. Filter Components ---

def create_filter_controls(df):
    """Generates the interactive filter components (dropdowns and radio buttons)."""
    manufacturers = sorted(df['Manufacturer'].unique())
    regions = sorted(df['Region'].unique())
    
    return [
        html.Div([
            html.Label('Manufacturer Filter', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='manufacturer-filter',
                options=[{'label': m, 'value': m} for m in manufacturers],
                value=manufacturers, # Default to all
                multi=True
            )
        ], style={'padding': '10px', 'flex': 1}),

        html.Div([
            html.Label('Region Filter', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': r, 'value': r} for r in regions],
                value=regions, # Default to all
                multi=True
            )
        ], style={'padding': '10px', 'flex': 1}),

        html.Div([
            html.Label('Sales Category', style={'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='sales-category-radio',
                options=[
                    {'label': 'High Sales', 'value': 'High'},
                    {'label': 'Medium Sales', 'value': 'Medium'},
                    {'label': 'Low Sales', 'value': 'Low'},
                    {'label': 'All Categories', 'value': 'All'}
                ],
                value='All',
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            )
        ], style={'padding': '10px', 'flex': 1})
    ]

# --- 2. KPI Components ---

def create_kpi_cards(df):
    """
    Creates simple KPI cards for total sales, average price, and success rate.
    These values will be updated by callbacks.
    """
    total_sales = df['SalesVolume'].sum()
    avg_price = df['Price_k'].mean().round(1)

    card_style = {
        'padding': '15px',
        'margin': '10px',
        'textAlign': 'center',
        'backgroundColor': '#ffffff',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px 0 rgba(0,0,0,0.1)',
        'flex': 1
    }

    return html.Div([
        html.Div([
            html.P("Total Sales Volume", style={'fontSize': '14px'}),
            html.H3(f"{total_sales:,.0f}", id='kpi-total-sales', style={'color': '#4CAF50', 'fontSize': '24px'}),
        ], style=card_style),
        html.Div([
            html.P("Average Vehicle Price", style={'fontSize': '14px'}),
            html.H3(f"${avg_price}k", id='kpi-avg-price', style={'color': '#2196F3', 'fontSize': '24px'}),
        ], style=card_style),
        html.Div([
            html.P("Success Rate (ML Target)", style={'fontSize': '14px'}),
            html.H3(f"{df['Is_Success'].mean()*100:.1f}%", id='kpi-success-rate', style={'color': '#FF9800', 'fontSize': '24px'}),
        ], style=card_style)
    ], id='kpi-container', style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around', 'padding': '10px'})


# --- 3. Chart Components ---

def create_sales_trend_chart(df):
    """Creates a time series plot of total sales volume over time."""
    # Group data by TimePeriod and calculate total sales
    trend_data = df.groupby('TimePeriod')['SalesVolume'].sum().reset_index()
    
    fig = px.line(
        trend_data, 
        x='TimePeriod', 
        y='SalesVolume', 
        title='Sales Volume Trend Over Time',
        template='plotly_white'
    )
    fig.update_layout(title_x=0.5)
    return html.Div(dcc.Graph(id='sales-trend-graph', figure=fig), className='card')

def create_category_performance_chart(df):
    """Creates a bar chart comparing performance across different sales categories."""
    # Group data by Sales_Category and calculate average price
    category_data = df.groupby('Sales_Category')['Price_k'].mean().reset_index()
    
    fig = px.bar(
        category_data,
        x='Sales_Category',
        y='Price_k',
        title='Average Price by Sales Category (k)',
        template='plotly_white',
        color='Sales_Category'
    )
    fig.update_layout(title_x=0.5)
    return html.Div(dcc.Graph(id='category-performance-graph', figure=fig), className='card')

def create_regional_heatmap(df):
    """Creates a heatmap of sales volume across Region and Manufacturer."""
    # Aggregate data for heatmap
    heatmap_data = df.groupby(['Region', 'Manufacturer'])['SalesVolume'].sum().reset_index()
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data['SalesVolume'],
        x=heatmap_data['Region'],
        y=heatmap_data['Manufacturer'],
        colorscale='Viridis',
    ))
    
    fig.update_layout(
        title='Sales Volume Heatmap by Region and Manufacturer',
        xaxis_title='Region',
        yaxis_title='Manufacturer',
        title_x=0.5
    )
    
    return html.Div(dcc.Graph(id='regional-heatmap', figure=fig), className='card')

def create_success_classification_chart(df):
    """
    Creates a pie chart showing the distribution of the classification target (Is_Success).
    """
    success_counts = df['Is_Success'].map({1: 'Successful Sales', 0: 'Unsuccessful Sales'}).value_counts().reset_index()
    success_counts.columns = ['Classification', 'Count']
    
    fig = px.pie(
        success_counts,
        names='Classification',
        values='Count',
        title='Sales Classification Distribution (Target Variable)',
        template='plotly_white',
        color_discrete_sequence=['#4CAF50', '#F44336'] # Green for Success, Red for Unsuccessful
    )
    fig.update_layout(title_x=0.5)
    return html.Div(dcc.Graph(id='success-classification-graph', figure=fig), className='card')


# --- 4. Header/Layout Component ---

def create_header(title):
    """Creates the header section of the dashboard."""
    return html.Div([
        html.H1(title, style=TEXT_STYLE),
        html.P("Interactive dashboard showcasing sales patterns, regional performance trends, and ML classification targets.", style=TEXT_STYLE),
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9'})

# --- 5. Layout Container ---

def create_layout_container(header, kpis, filters, charts):
    """Creates the main responsive layout for the dashboard."""
    return html.Div([
        header,
        # KPIs section
        html.Div(kpis, style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-around',
            'padding': '10px',
            'backgroundColor': '#f9f9f9'
        }),
        # Filters section
        html.Div(filters, style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'wrap',
            'justifyContent': 'space-around',
            'padding': '10px',
            'backgroundColor': '#e8e8e8'
        }),
        # Charts section
        html.Div(charts, style={
            'display': 'flex',
            'flexDirection': 'column',
            'padding': '20px'
        })
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'border': '1px solid #ccc', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'})
