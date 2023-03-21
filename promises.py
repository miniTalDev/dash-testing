from dash import Dash, dcc, html, Input, Output, dash_table

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Dropdown(
            options=[
                {
                    "label": "Car-sharing data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/carshare_data.json",
                },
                {
                    "label": "Iris data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
                },
            ],
            value="https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
            id="data-select",
        ),
        html.Br(),
        dash_table.DataTable(id="my-table-promises", page_size=10),
    ]
)

app.clientside_callback(
    """
    async function(value) {
    const response = await fetch(value);
    const data = await response.json();
    return data;
    }
    """,
    Output("my-table-promises", "data"),
    Input("data-select", "value"),
)

if __name__ == "__main__":
    app.run_server(debug=True)
