import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import datetime

# Création de l'app Dash
app = dash.Dash(__name__)
app.title = "APPLE Dashboard"


app.layout = html.Div([
    html.H1("Cours d'Apple - Live Tracker", style={"textAlign": "center"}),

    dcc.Graph(id='AAPL-graph'),

    html.Div(id='last-update', style={"textAlign": "center", "marginTop": "10px"}),

    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  
        n_intervals=0
    )
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output('AAPL-graph', 'figure'),
    Output('last-update', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    try:
        df = pd.read_csv("AAPL_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = px.line(df, x='timestamp', y='price', title="Évolution d'Apple",
                      labels={"timestamp": "Heure", "price": "Prix"})
        fig.update_layout(xaxis_title='Temps', yaxis_title='Prix', template="plotly_white")

        last_time = df['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')
        return fig, f"Dernière mise à jour : {last_time}"
    except Exception as e:
        return {}, f"Erreur lors de la lecture des données : {e}"

# Exécution du serveur
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)
