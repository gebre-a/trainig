# Import necessary libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Sample data (replace with your actual data)
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 15, 25, 30]
})

# Initialize the Dash appcls
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Data Science Dashboard"),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df['x'], 'y': df['y'], 'type': 'bar', 'name': 'Data'},
            ],
            'layout': {
                'title': 'Bar Chart Example'
            }
        }
    )
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
