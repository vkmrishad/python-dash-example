import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html

from src.db.connection import SessionLocal
from src.db.crud import get_overview_metrics

# Define the layout for the landing page
landing_page_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Overview"),
                        ]
                    )
                ),
            ]
        ),
        dcc.Loading(
            id="loading",
            type="default",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Total Orders", className="card-title"),
                                        html.P(
                                            id="total_orders", className="card-text"
                                        ),
                                        html.P(
                                            id="date_range_orders",
                                            className="card-date",
                                        ),
                                    ]
                                ),
                                color="primary",
                                inverse=True,
                                className="mb-3 text-white hover-card",
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Total Sales", className="card-title"),
                                        html.P(id="total_sales", className="card-text"),
                                        html.P(
                                            id="date_range_sales", className="card-date"
                                        ),
                                    ]
                                ),
                                color="info",
                                inverse=True,
                                className="mb-3 text-white hover-card",
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Total Profit", className="card-title"),
                                        html.P(
                                            id="total_profit", className="card-text"
                                        ),
                                        html.P(
                                            id="date_range_profit",
                                            className="card-date",
                                        ),
                                    ]
                                ),
                                color="success",
                                inverse=True,
                                className="mb-3 text-white hover-card",
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Profit Ratio", className="card-title"),
                                        html.P(
                                            id="profit_ratio", className="card-text"
                                        ),
                                        html.P(
                                            id="date_range_ratio", className="card-date"
                                        ),
                                    ]
                                ),
                                color="dark",
                                inverse=True,
                                className="mb-3 text-white hover-card",
                            ),
                            width=3,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardLink(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H4("Table"),
                                            html.P(
                                                "Go to Table Page",
                                                className="card-link-text",
                                            ),
                                        ]
                                    ),
                                    color="warning",
                                    inverse=True,
                                    className="mb-3 text-white hover-card",
                                ),
                                href="/table",
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dbc.CardLink(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H4("Graph"),
                                            html.P(
                                                "Go to Graph Page",
                                                className="card-link-text",
                                            ),
                                        ]
                                    ),
                                    color="danger",
                                    inverse=True,
                                    className="mb-3 text-white hover-card",
                                ),
                                href="/graph",
                            ),
                            width=6,
                        ),
                    ],
                    id="go-to-pages",
                ),
            ],
        ),
    ],
    fluid=True,
)


@callback(
    Output("total_orders", "children"),
    Output("total_sales", "children"),
    Output("total_profit", "children"),
    Output("profit_ratio", "children"),
    Output("date_range_orders", "children"),
    Output("date_range_sales", "children"),
    Output("date_range_profit", "children"),
    Output("date_range_ratio", "children"),
    Input("url", "pathname"),
)
def update_metrics(pathname):
    # Load the data each time the page is loaded
    with SessionLocal() as session:
        metrics = get_overview_metrics(session)

    total_orders = metrics.get("total_orders", 0)
    total_sales = metrics.get("total_sales", 0)
    total_profit = metrics.get("total_profit", 0)
    profit_ratio = metrics.get("profit_ratio", 0)
    start_date = metrics.get("start_date")
    end_date = metrics.get("end_date")

    # Format the dates like "Jan 1, 2024"
    start_date_formatted = start_date.strftime("%b %-d, %Y") if start_date else "N/A"
    end_date_formatted = end_date.strftime("%b %-d, %Y") if end_date else "N/A"
    date_range_str = f"{start_date_formatted} - {end_date_formatted}"

    return (
        f"{total_orders}",
        f"€{total_sales:,.2f}",
        f"€{total_profit:,.2f}",
        f"{profit_ratio:.2f}%",
        date_range_str,
        date_range_str,
        date_range_str,
        date_range_str,
    )
