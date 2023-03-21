from dash import Dash, html, dcc, Input, Output, Patch
import plotly.express as px
import random

app = Dash(__name__)

df = px.data.iris()
fig = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species", title="Updating Title Color"
)

app.layout = html.Div(
    [
        html.Button("Update Graph Color", id="update-color-button-2"),
        dcc.Graph(figure=fig, id="my-fig"),
    ]
)


@app.callback(Output("my-fig", "figure"), Input("update-color-button-2", "n_clicks"))
def my_callback(n_clicks):
    # Defining a new random color
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    new_color = f"rgb({red}, {green}, {blue})"

    # Creating a Patch object
    patched_figure = Patch()
    patched_figure["layout"]["title"]["font"]["color"] = new_color
    return patched_figure

if __name__ == "__main__":
    app.run_server(debug=True)
