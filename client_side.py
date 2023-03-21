from dash import Dash, dcc, html, Input, Output
import pandas as pd
import json

import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

available_countries = df['country'].unique()

app.layout = html.Div([
    dcc.Graph(
        id='clientside-graph-px'
    ),
    dcc.Store(
        id='clientside-figure-store-px'
    ),
    'Indicator',
    dcc.Dropdown(
        {'pop' : 'Population', 'lifeExp': 'Life Expectancy', 'gdpPercap': 'GDP per Capita'},
        'pop',
        id='clientside-graph-indicator-px'
    ),
    'Country',
    dcc.Dropdown(available_countries, 'Canada', id='clientside-graph-country-px'),
    'Graph scale',
    dcc.RadioItems(
        ['linear', 'log'],
        'linear',
        id='clientside-graph-scale-px'
    ),
    html.Hr(),
    html.Details([
        html.Summary('Contents of figure storage'),
        dcc.Markdown(
            id='clientside-figure-json-px'
        )
    ])
])


@app.callback(
    Output('clientside-figure-store-px', 'data'),
    Input('clientside-graph-indicator-px', 'value'),
    Input('clientside-graph-country-px', 'value')
)
def update_store_data(indicator, country):
    dff = df[df['country'] == country]
    return px.scatter(dff, x='year', y=str(indicator))


app.clientside_callback(
    """
    function(figure, scale) {
        if(figure === undefined) {
            return {'data': [], 'layout': {}};
        }
        const fig = Object.assign({}, figure, {
            'layout': {
                ...figure.layout,
                'yaxis': {
                    ...figure.layout.yaxis, type: scale
                }
             }
        });
        return fig;
    }
    """,
    Output('clientside-graph-px', 'figure'),
    Input('clientside-figure-store-px', 'data'),
    Input('clientside-graph-scale-px', 'value')
)


@app.callback(
    Output('clientside-figure-json-px', 'children'),
    Input('clientside-figure-store-px', 'data')
)
def generated_px_figure_json(data):
    return '```\n'+json.dumps(data, indent=2)+'\n```'


if __name__ == '__main__':
    app.run_server(debug=True)
