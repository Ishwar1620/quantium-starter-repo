
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

df = pd.read_csv('output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

price_increase_date = pd.to_datetime('2021-01-15')

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    },
    children=[
        html.Div(
            style={
                'backgroundColor': '#2c3e50',
                'padding': '30px',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'textAlign': 'center'
            },
            children=[
                html.H1(
                    'Pink Morsel Sales Dashboard',
                    style={
                        'color': 'white',
                        'margin': '0',
                        'fontSize': '32px'
                    }
                ),
                html.P(
                    'Analyzing sales before and after the January 15, 2021 price increase',
                    style={
                        'color': '#ecf0f1',
                        'margin': '10px 0 0 0',
                        'fontSize': '16px'
                    }
                )
            ]
        ),
        
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '8px',
                'marginBottom': '20px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            },
            children=[
                html.Label(
                    'Filter by Region:',
                    style={
                        'fontSize': '16px',
                        'fontWeight': 'bold',
                        'marginBottom': '10px',
                        'display': 'block',
                        'color': '#2c3e50'
                    }
                ),
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': ' All Regions', 'value': 'all'},
                        {'label': ' North', 'value': 'north'},
                        {'label': ' East', 'value': 'east'},
                        {'label': ' South', 'value': 'south'},
                        {'label': ' West', 'value': 'west'}
                    ],
                    value='all',
                    inline=True,
                    labelStyle={
                        'marginRight': '20px',
                        'fontSize': '14px',
                        'cursor': 'pointer'
                    }
                )
            ]
        ),
        
        html.Div(id='stats-section'),
        
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            },
            children=[
                dcc.Graph(id='sales-chart')
            ]
        )
    ]
)


@app.callback(
    [Output('sales-chart', 'figure'),
     Output('stats-section', 'children')],
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df.copy()
        region_label = 'All Regions'
    else:
        filtered_df = df[df['region'] == selected_region].copy()
        region_label = selected_region.capitalize()
    
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_sales['date'],
        y=daily_sales['sales'],
        mode='lines',
        name='Sales',
        line=dict(color='#3498db', width=2),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Sales: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="#e74c3c", width=2, dash="dash")
    )
    
    fig.add_annotation(
        x=price_increase_date,
        y=1,
        yref="paper",
        text="Price Increase<br>Jan 15, 2021",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-30,
        bgcolor="white",
        bordercolor="#e74c3c",
        borderwidth=2,
        font=dict(size=11, color="#e74c3c")
    )
    
    fig.update_layout(
        title=f'Sales Over Time - {region_label}',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#ecf0f1'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#ecf0f1',
            tickformat='$,.0f'
        ),
        height=500,
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
    after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()
    percentage_change = ((after_increase - before_increase) / before_increase) * 100
    
    stats_section = html.Div(
        style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
            'gap': '15px',
            'marginBottom': '20px'
        },
        children=[
            html.Div(
                style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'borderTop': '4px solid #3498db'
                },
                children=[
                    html.H4('Before Price Increase', style={'color': '#2c3e50', 'margin': '0 0 10px 0', 'fontSize': '14px'}),
                    html.P(f'${before_increase:,.2f}', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#3498db', 'margin': '0'}),
                    html.P('Avg Daily Sales', style={'color': '#7f8c8d', 'margin': '5px 0 0 0', 'fontSize': '12px'})
                ]
            ),
            
            html.Div(
                style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'borderTop': f'4px solid {"#27ae60" if percentage_change > 0 else "#e74c3c"}'
                },
                children=[
                    html.H4('After Price Increase', style={'color': '#2c3e50', 'margin': '0 0 10px 0', 'fontSize': '14px'}),
                    html.P(f'${after_increase:,.2f}', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#27ae60' if percentage_change > 0 else '#e74c3c', 'margin': '0'}),
                    html.P('Avg Daily Sales', style={'color': '#7f8c8d', 'margin': '5px 0 0 0', 'fontSize': '12px'})
                ]
            ),
            
            html.Div(
                style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'borderTop': '4px solid #f39c12'
                },
                children=[
                    html.H4('Change', style={'color': '#2c3e50', 'margin': '0 0 10px 0', 'fontSize': '14px'}),
                    html.P(f'{percentage_change:+.1f}%', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#f39c12', 'margin': '0'}),
                    html.P('Percentage', style={'color': '#7f8c8d', 'margin': '5px 0 0 0', 'fontSize': '12px'})
                ]
            )
        ]
    )
    
    return fig, stats_section


if __name__ == '__main__':
    app.run(debug=True, port=8050)
