
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
import plotly.express as px


app = Dash(__name__)

df = pd.read_csv('output.csv')

df['date'] = pd.to_datetime(df['date'])

df = df.sort_values('date')

daily_sales = df.groupby('date')['sales'].sum().reset_index()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=daily_sales['date'],
    y=daily_sales['sales'],
    mode='lines',
    name='Daily Sales',
    line=dict(color='#2E86AB', width=2),
    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Sales</b>: $%{y:,.2f}<extra></extra>'
))

price_increase_date = pd.to_datetime('2021-01-15')

fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(color="red", width=2, dash="dash")
)

fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref="paper",
    text="Price Increase<br>Jan 15, 2021",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="red",
    ax=40,
    ay=-40,
    bgcolor="rgba(255, 255, 255, 0.9)",
    bordercolor="red",
    borderwidth=2,
    font=dict(size=12, color="red")
)

fig.update_layout(
    title={
        'text': 'Pink Morsel Sales Over Time',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#1a1a1a'}
    },
    xaxis_title='Date',
    yaxis_title='Total Daily Sales ($)',
    hovermode='x unified',
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=12, color='#333333'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        showline=True,
        linewidth=1,
        linecolor='#cccccc'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        showline=True,
        linewidth=1,
        linecolor='#cccccc',
        tickformat='$,.0f'
    ),
    height=600,
    margin=dict(l=80, r=40, t=100, b=80)
)

before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()
percentage_change = ((after_increase - before_increase) / before_increase) * 100

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'maxWidth': '1400px',
        'margin': '0 auto'
    },
    children=[
        html.Div(
            style={
                'backgroundColor': '#2E86AB',
                'padding': '30px',
                'borderRadius': '10px',
                'marginBottom': '30px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
            },
            children=[
                html.H1(
                    'Pink Morsel Sales Dashboard',
                    style={
                        'color': 'white',
                        'textAlign': 'center',
                        'margin': '0',
                        'fontSize': '36px',
                        'fontWeight': 'bold'
                    }
                ),
                html.P(
                    'Analyzing sales trends before and after the January 15, 2021 price increase',
                    style={
                        'color': '#e8f4f8',
                        'textAlign': 'center',
                        'margin': '10px 0 0 0',
                        'fontSize': '16px'
                    }
                )
            ]
        ),
        
        html.Div(
            style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'marginBottom': '30px',
                'gap': '20px'
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': '#f0f7fb',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'flex': '1',
                        'textAlign': 'center',
                        'border': '2px solid #2E86AB'
                    },
                    children=[
                        html.H3('Before Price Increase', style={'color': '#2E86AB', 'margin': '0 0 10px 0'}),
                        html.P(
                            f'${before_increase:,.2f}',
                            style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1a1a1a', 'margin': '0'}
                        ),
                        html.P('Average Daily Sales', style={'color': '#666', 'margin': '5px 0 0 0'})
                    ]
                ),
                
                html.Div(
                    style={
                        'backgroundColor': '#fff0f0' if percentage_change < 0 else '#f0fbf0',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'flex': '1',
                        'textAlign': 'center',
                        'border': f'2px solid {"#dc3545" if percentage_change < 0 else "#28a745"}'
                    },
                    children=[
                        html.H3('After Price Increase', style={'color': '#dc3545' if percentage_change < 0 else '#28a745', 'margin': '0 0 10px 0'}),
                        html.P(
                            f'${after_increase:,.2f}',
                            style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1a1a1a', 'margin': '0'}
                        ),
                        html.P('Average Daily Sales', style={'color': '#666', 'margin': '5px 0 0 0'})
                    ]
                ),
                
                html.Div(
                    style={
                        'backgroundColor': '#fff9e6',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'flex': '1',
                        'textAlign': 'center',
                        'border': '2px solid #ffc107'
                    },
                    children=[
                        html.H3('Change', style={'color': '#f57c00', 'margin': '0 0 10px 0'}),
                        html.P(
                            f'{percentage_change:+.2f}%',
                            style={
                                'fontSize': '28px',
                                'fontWeight': 'bold',
                                'color': '#dc3545' if percentage_change < 0 else '#28a745',
                                'margin': '0'
                            }
                        ),
                        html.P('Percentage Change', style={'color': '#666', 'margin': '5px 0 0 0'})
                    ]
                )
            ]
        ),
        
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            },
            children=[
                dcc.Graph(
                    id='sales-chart',
                    figure=fig,
                    config={'displayModeBar': True, 'displaylogo': False}
                )
            ]
        ),
        
        html.Div(
            style={
                'marginTop': '30px',
                'padding': '20px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'borderLeft': '4px solid #2E86AB'
            },
            children=[
                html.H3('Business Insight', style={'color': '#2E86AB', 'marginTop': '0'}),
                html.P(
                    f'Sales were {"HIGHER" if percentage_change > 0 else "LOWER"} after the price increase on January 15, 2021. '
                    f'The average daily sales {"increased" if percentage_change > 0 else "decreased"} by {abs(percentage_change):.2f}%, '
                    f'from ${before_increase:,.2f} to ${after_increase:,.2f}.',
                    style={'fontSize': '16px', 'lineHeight': '1.6', 'color': '#333', 'margin': '10px 0'}
                )
            ]
        )
    ]
)


if __name__ == '__main__':
    app.run(debug=True, port=8050)
