import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import datetime

# Initialisation de l'app
app = dash.Dash(__name__)
app.title = "Cours Apple (AAPL)"

# Layout de l'app
app.layout = html.Div([
    html.H1("Cours de l'action Apple (AAPL) - Live Tracker", style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(id='AAPL-graph'),
        html.Div(id='daily-report', style={"marginTop": "30px"})
    ]),

    html.Div(id='last-update', style={"textAlign": "center", "marginTop": "10px"}),

    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  
        n_intervals=0
    )
])

# Callback pour mettre à jour le graphique et le rapport
@app.callback(
    Output('aapl-graph', 'figure'),
    Output('last-update', 'children'),
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    try:
        df = pd.read_csv("AAPL_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.dropna(subset=["price"])  # On enlève les NA

        fig = px.line(df, x='timestamp', y='price', title="Évolution de l'action AAPL",
                      labels={"timestamp": "Heure", "price": "Prix ($)"})
        fig.update_layout(xaxis_title='Temps', yaxis_title='Prix ($)', template="plotly_white")

        last_time = df['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')

        # Rapport du jour
        today = pd.Timestamp.now().normalize()
        daily_data = df[df['timestamp'].dt.normalize() == today]

        if not daily_data.empty:
            open_price = daily_data['price'].iloc[0]
            close_price = daily_data['price'].iloc[-1]
            evolution = ((close_price - open_price) / open_price) * 100
            volatility = daily_data['price'].std()

            report = html.Div([
                html.H4("Rapport du jour - Apple (AAPL)"),
                html.P(f"Prix d'ouverture : {open_price:.2f} $"),
                html.P(f"Prix de clôture : {close_price:.2f} $"),
                html.P(f"Évolution : {evolution:.2f}%"),
                html.P(f"Volatilité : {volatility:.4f}"),
            ], style={"textAlign": "left", "border": "1px solid #ddd", "padding": "15px", "borderRadius": "10px"})
        else:
            report = html.Div([
                html.H4("Rapport du jour - Apple (AAPL)"),
                html.P("Aucune donnée disponible pour aujourd’hui.")
            ])

        return fig, f"Dernière mise à jour : {last_time}", report

    except Exception as e:
        return {}, f"Erreur lors de la lecture des données : {e}", html.Div()

# Exécution de l'app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050, use_reloader=True)
