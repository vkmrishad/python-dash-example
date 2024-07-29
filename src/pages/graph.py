import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, dcc, html

from src.db.crud import load_data

# Load the data
df = load_data()

# Define the layout for the graph page
graph_page_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H2("Graphs")),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="timeline-graph"), width=8),
                dbc.Col(dcc.Graph(id="bubble-chart"), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="x-axis-dropdown",
                        options=[
                            {"label": col, "value": col}
                            for col in [
                                "Days to Ship",
                                "Discount",
                                "Profit",
                                "Profit Ratio",
                                "Quantity",
                                "Returns",
                                "Sales",
                            ]
                        ],
                        placeholder="Select X-Axis",
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="y-axis-dropdown",
                        options=[
                            {"label": col, "value": col}
                            for col in [
                                "Days to Ship",
                                "Discount",
                                "Profit",
                                "Profit Ratio",
                                "Quantity",
                                "Returns",
                                "Sales",
                            ]
                        ],
                        placeholder="Select Y-Axis",
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="size-dropdown",
                        options=[
                            {"label": col, "value": col}
                            for col in [
                                "Days to Ship",
                                "Discount",
                                "Profit",
                                "Profit Ratio",
                                "Quantity",
                                "Returns",
                                "Sales",
                            ]
                        ],
                        placeholder="Select Bubble Size",
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="breakdown-dropdown",
                        options=[
                            {"label": col, "value": col}
                            for col in [
                                "Segment",
                                "Delivery Mode",
                                "Customer Name",
                                "Category",
                                "Sub-Category",
                                "Product Name",
                            ]
                        ],
                        placeholder="Select Breakdown",
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.DatePickerRange(id="date-picker-range")),
                dbc.Col(
                    dcc.Dropdown(
                        id="granularity-dropdown",
                        options=[
                            {"label": "Day", "value": "D"},
                            {"label": "Week", "value": "W"},
                            {"label": "Month", "value": "M"},
                            {"label": "Quarter", "value": "Q"},
                            {"label": "Year", "value": "Y"},
                        ],
                        placeholder="Select Granularity",
                    )
                ),
            ]
        ),
    ],
    fluid=True,
)


# Register callbacks for the graph page
def register_callbacks(app):
    @app.callback(
        Output("timeline-graph", "figure"),
        [
            Input("date-picker-range", "start_date"),
            Input("date-picker-range", "end_date"),
            Input("granularity-dropdown", "value"),
        ],
    )
    def update_timeline_graph(start_date, end_date, granularity):
        filtered_df = df[
            (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)
        ]
        if not granularity:
            granularity = "M"
        fig = px.line(filtered_df, x="Order Date", y="Sales", title="Sales Over Time")
        fig.update_xaxes(dtick=granularity)
        return fig

    @app.callback(
        Output("bubble-chart", "figure"),
        [
            Input("x-axis-dropdown", "value"),
            Input("y-axis-dropdown", "value"),
            Input("size-dropdown", "value"),
            Input("breakdown-dropdown", "value"),
        ],
    )
    def update_bubble_chart(x_axis, y_axis, size, breakdown):
        if x_axis and y_axis and size and breakdown:
            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                size=size,
                color=breakdown,
                title=f"{y_axis} vs {x_axis}",
            )
            return fig
        return {}
