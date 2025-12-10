
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


app = Dash(__name__)

df = pd.read_csv('output.csv')

df['date'] = pd.to_datetime(df['date'])

df = df.sort_values('date')

price_increase_date = pd.to_datetime('2021-01-15')

app.layout = html.Div(
    style={
        'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        'backgroundColor': '#f5f7fa',
        'minHeight': '100vh',
        'padding': '0',
        'margin': '0'
    },
    children=[
        html.Div(
            style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'padding': '40px 20px',
                'boxShadow': '0 4px 20px rgba(0,0,0,0.15)',
                'marginBottom': '30px'
            },
            children=[
                html.H1(
                    '🍬 Pink Morsel Sales Dashboard',
                    style={
                        'color': 'white',
                        'textAlign': 'center',
                        'margin': '0',
                        'fontSize': '42px',
                        'fontWeight': '700',
                        'letterSpacing': '1px',
                        'textShadow': '2px 2px 4px rgba(0,0,0,0.2)'
                    }
                ),
                html.P(
                    'Interactive Analysis of Sales Trends | Price Increase: January 15, 2021',
                    style={
                        'color': '#e8f4f8',
                        'textAlign': 'center',
                        'margin': '15px 0 0 0',
                        'fontSize': '18px',
                        'fontWeight': '300'
                    }
                )
            ]
        ),
        
        html.Div(
            style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '0 20px'
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 12px rgba(0,0,0,0.08)',
                        'marginBottom': '25px',
                        'border': '1px solid #e1e8ed'
                    },
                    children=[
                        html.Label(
                            '📍 Filter by Region:',
                            style={
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'color': '#2c3e50',
                                'marginBottom': '15px',
                                'display': 'block'
                            }
                        ),
                        dcc.RadioItems(
                            id='region-filter',
                            options=[
                                {'label': ' 🌐 All Regions', 'value': 'all'},
                                {'label': ' ⬆️ North', 'value': 'north'},
                                {'label': ' ➡️ East', 'value': 'east'},
                                {'label': ' ⬇️ South', 'value': 'south'},
                                {'label': ' ⬅️ West', 'value': 'west'}
                            ],
                            value='all',
                            inline=True,
                            style={
                                'display': 'flex',
                                'gap': '20px',
                                'flexWrap': 'wrap'
                            },
                            labelStyle={
                                'padding': '12px 24px',
                                'backgroundColor': '#f8f9fa',
                                'borderRadius': '25px',
                                'cursor': 'pointer',
                                'fontSize': '16px',
                                'fontWeight': '500',
                                'transition': 'all 0.3s ease',
                                'border': '2px solid #e1e8ed',
                                'color': '#495057'
                            },
                            inputStyle={
                                'marginRight': '8px',
                                'cursor': 'pointer'
                            }
                        )
                    ]
                ),
                
                html.Div(id='stats-cards'),
                
                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 12px rgba(0,0,0,0.08)',
                        'marginBottom': '25px',
                        'border': '1px solid #e1e8ed'
                    },
                    children=[
                        dcc.Graph(
                            id='sales-chart',
                            config={
                                'displayModeBar': True,
                                'displaylogo': False,
                                'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                            }
                        )
                    ]
                ),
                
                html.Div(id='insights-footer')
            ]
        ),
        
        html.Div(
            style={
                'textAlign': 'center',
                'padding': '30px',
                'color': '#7f8c8d',
                'fontSize': '14px',
                'marginTop': '40px'
            },
            children=[
                html.P('© 2025 Soul Foods Analytics | Powered by Dash & Plotly', style={'margin': '0'})
            ]
        )
    ]
)


@app.callback(
    [Output('sales-chart', 'figure'),
     Output('stats-cards', 'children'),
     Output('insights-footer', 'children')],
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
        name='Daily Sales',
        line=dict(color='#667eea', width=3),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Sales</b>: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="#e74c3c", width=3, dash="dash")
    )
    
    fig.add_annotation(
        x=price_increase_date,
        y=1,
        yref="paper",
        text="💰 Price Increase<br>Jan 15, 2021",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#e74c3c",
        ax=50,
        ay=-50,
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#e74c3c",
        borderwidth=2,
        borderpad=8,
        font=dict(size=13, color="#e74c3c", family="Arial Black")
    )
    
    fig.update_layout(
        title={
            'text': f'Pink Morsel Sales Over Time - {region_label}',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 26, 'color': '#2c3e50', 'family': 'Arial Black'}
        },
        xaxis_title='Date',
        yaxis_title='Total Daily Sales ($)',
        hovermode='x unified',
        plot_bgcolor='#fafbfc',
        paper_bgcolor='white',
        font=dict(family="'Segoe UI', Arial, sans-serif", size=13, color='#2c3e50'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#e1e8ed',
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor='#cbd5e0'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e1e8ed',
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor='#cbd5e0',
            tickformat='$,.0f'
        ),
        height=550,
        margin=dict(l=80, r=40, t=80, b=80),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        )
    )
    
    before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
    after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()
    percentage_change = ((after_increase - before_increase) / before_increase) * 100
    
    stats_cards = html.Div(
        style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))',
            'gap': '20px',
            'marginBottom': '25px'
        },
        children=[
            html.Div(
                style={
                    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'padding': '25px',
                    'borderRadius': '12px',
                    'textAlign': 'center',
                    'boxShadow': '0 6px 20px rgba(102, 126, 234, 0.3)',
                    'transform': 'translateY(0)',
                    'transition': 'transform 0.3s ease'
                },
                children=[
                    html.H3('Before Price Increase', style={'color': 'white', 'margin': '0 0 12px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P(
                        f'${before_increase:,.2f}',
                        style={'fontSize': '32px', 'fontWeight': 'bold', 'color': 'white', 'margin': '0', 'textShadow': '2px 2px 4px rgba(0,0,0,0.2)'}
                    ),
                    html.P('Average Daily Sales', style={'color': 'rgba(255,255,255,0.9)', 'margin': '8px 0 0 0', 'fontSize': '14px'})
                ]
            ),
            
            html.Div(
                style={
                    'background': f'linear-gradient(135deg, {"#e74c3c" if percentage_change < 0 else "#27ae60"} 0%, {"#c0392b" if percentage_change < 0 else "#229954"} 100%)',
                    'padding': '25px',
                    'borderRadius': '12px',
                    'textAlign': 'center',
                    'boxShadow': f'0 6px 20px rgba({"231, 76, 60" if percentage_change < 0 else "39, 174, 96"}, 0.3)',
                    'transform': 'translateY(0)',
                    'transition': 'transform 0.3s ease'
                },
                children=[
                    html.H3('After Price Increase', style={'color': 'white', 'margin': '0 0 12px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P(
                        f'${after_increase:,.2f}',
                        style={'fontSize': '32px', 'fontWeight': 'bold', 'color': 'white', 'margin': '0', 'textShadow': '2px 2px 4px rgba(0,0,0,0.2)'}
                    ),
                    html.P('Average Daily Sales', style={'color': 'rgba(255,255,255,0.9)', 'margin': '8px 0 0 0', 'fontSize': '14px'})
                ]
            ),
            
            html.Div(
                style={
                    'background': 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)',
                    'padding': '25px',
                    'borderRadius': '12px',
                    'textAlign': 'center',
                    'boxShadow': '0 6px 20px rgba(243, 156, 18, 0.3)',
                    'transform': 'translateY(0)',
                    'transition': 'transform 0.3s ease'
                },
                children=[
                    html.H3('Percentage Change', style={'color': 'white', 'margin': '0 0 12px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P(
                        f'{percentage_change:+.2f}%',
                        style={'fontSize': '32px', 'fontWeight': 'bold', 'color': 'white', 'margin': '0', 'textShadow': '2px 2px 4px rgba(0,0,0,0.2)'}
                    ),
                    html.P(
                        f'{"📈 Increase" if percentage_change > 0 else "📉 Decrease"}',
                        style={'color': 'rgba(255,255,255,0.9)', 'margin': '8px 0 0 0', 'fontSize': '14px', 'fontWeight': '600'}
                    )
                ]
            )
        ]
    )
    
    insights = html.Div(
        style={
            'backgroundColor': 'white',
            'padding': '30px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.08)',
            'borderLeft': f'6px solid {"#27ae60" if percentage_change > 0 else "#e74c3c"}',
            'border': '1px solid #e1e8ed'
        },
        children=[
            html.H3(
                '💡 Business Insight',
                style={
                    'color': '#2c3e50',
                    'marginTop': '0',
                    'fontSize': '22px',
                    'fontWeight': '700',
                    'marginBottom': '15px'
                }
            ),
            html.P(
                f'For {region_label}, sales were ',
                style={'fontSize': '17px', 'lineHeight': '1.8', 'color': '#34495e', 'margin': '0', 'display': 'inline'}
            ),
            html.Span(
                f'{"HIGHER ✅" if percentage_change > 0 else "LOWER ⚠️"}',
                style={
                    'fontWeight': 'bold',
                    'color': '#27ae60' if percentage_change > 0 else '#e74c3c',
                    'fontSize': '18px'
                }
            ),
            html.P(
                f' after the price increase on January 15, 2021. '
                f'The average daily sales {"increased" if percentage_change > 0 else "decreased"} by ',
                style={'fontSize': '17px', 'lineHeight': '1.8', 'color': '#34495e', 'margin': '0', 'display': 'inline'}
            ),
            html.Span(
                f'{abs(percentage_change):.2f}%',
                style={'fontWeight': 'bold', 'color': '#f39c12', 'fontSize': '18px'}
            ),
            html.P(
                f', from ${before_increase:,.2f} to ${after_increase:,.2f}.',
                style={'fontSize': '17px', 'lineHeight': '1.8', 'color': '#34495e', 'margin': '0', 'display': 'inline'}
            )
        ]
    )
    
    return fig, stats_cards, insights


if __name__ == '__main__':
    app.run(debug=True, port=8050)
