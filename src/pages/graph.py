import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from src.db.connection import SessionLocal
from src.db.model import Order

# Load the data
with SessionLocal() as session:
    # Query all data from the orders table
    orders = session.query(Order).order_by(Order.id.desc()).all()

    # Convert ORM objects to a DataFrame
    df = pd.DataFrame([order.__dict__ for order in orders])
    df.drop(columns=["_sa_instance_state"], inplace=True)  # Remove SQLAlchemy state

# Convert SQLAlchemy Date to datetime
df["order_date"] = pd.to_datetime(
    df["order_date"].astype(str), errors="coerce"
)  # Convert to datetime
df["dispatch_date"] = pd.to_datetime(
    df["dispatch_date"].astype(str), errors="coerce"
)  # Convert to datetime

# Calculate additional columns
df["days_to_ship"] = (df["dispatch_date"] - df["order_date"]).dt.days
df["profit_ratio"] = df["profit"] / df["sales"]

# List of expected numerical columns
numerical_columns = [
    "days_to_ship",
    "discount",
    "profit",
    "profit_ratio",
    "quantity",
    "returns",
    "sales",
]

# Calculate the first day of the month of the max order_date
min_order_date = df["order_date"].min()
max_order_date = df["order_date"].max()

# Define the layout for the graph page
graph_page_layout = dbc.Container(
    [
        dbc.Row([dbc.Col(html.H2("Graph"))]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.DatePickerRange(
                            id="date-picker-range",
                            start_date=min_order_date.date(),
                            end_date=max_order_date.date(),
                        ),
                    ],
                    width=12,
                    className="mt-2 mb-2",
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
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id="granularity-dropdown",
                                                    options=[
                                                        {
                                                            "label": "Daily",
                                                            "value": "D",
                                                        },
                                                        {"label": "Week", "value": "W"},
                                                        {
                                                            "label": "Month",
                                                            "value": "ME",
                                                        },
                                                        {
                                                            "label": "Quarter",
                                                            "value": "QE",
                                                        },
                                                        {
                                                            "label": "Year",
                                                            "value": "YE",
                                                        },
                                                    ],
                                                    value="ME",
                                                )
                                            ],
                                            width=4,
                                            align="start",
                                        ),
                                    ]
                                ),
                                dcc.Graph(id="timeline-graph"),
                            ],
                            width=6,
                            align="start",
                            className="mt-2 mb-2",
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id="x-axis-dropdown",
                                                    options=[
                                                        {
                                                            "label": col.replace(
                                                                "_", " "
                                                            ).title(),
                                                            "value": col,
                                                        }
                                                        for col in numerical_columns
                                                    ],
                                                    value="sales",
                                                )
                                            ],
                                            width=4,
                                            align="start",
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id="y-axis-dropdown",
                                                    options=[
                                                        {
                                                            "label": col.replace(
                                                                "_", " "
                                                            ).title(),
                                                            "value": col,
                                                        }
                                                        for col in numerical_columns
                                                    ],
                                                    value="profit",
                                                )
                                            ],
                                            width=4,
                                            align="start",
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id="breakdown-dropdown",
                                                    options=[
                                                        {
                                                            "label": "Segment",
                                                            "value": "segment",
                                                        },
                                                        {
                                                            "label": "Ship Mode",
                                                            "value": "delivery_mode",
                                                        },
                                                        {
                                                            "label": "Customer Name",
                                                            "value": "customer_name",
                                                        },
                                                        {
                                                            "label": "Category",
                                                            "value": "category",
                                                        },
                                                        {
                                                            "label": "Sub-Category",
                                                            "value": "sub_category",
                                                        },
                                                        {
                                                            "label": "Product Name",
                                                            "value": "product_name",
                                                        },
                                                    ],
                                                    value="category",
                                                )
                                            ],
                                            width=4,
                                            align="start",
                                        ),
                                    ],
                                    className="mt-2 mb-2",
                                ),
                                dcc.Graph(id="bubble-chart"),
                            ],
                            width=6,
                        ),
                    ]
                ),
            ],
        ),
    ],
    fluid=True,
)


# Callback for updating the timeline graph
@callback(
    Output("timeline-graph", "figure"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("granularity-dropdown", "value"),
)
def update_timeline_graph(start_date, end_date, granularity):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date, errors="coerce")
    end_date = pd.to_datetime(end_date, errors="coerce")

    # Filter DataFrame
    dff = df[(df["order_date"] >= start_date) & (df["order_date"] <= end_date)]

    if dff.empty:
        return px.line()  # Return an empty figure if no data is available

    # Ensure 'order_date' is the index
    dff.set_index("order_date", inplace=True)

    # Ensure only numerical columns are included
    numerical_columns_present = [col for col in numerical_columns if col in dff.columns]

    # Check if there are numerical columns to resample
    if not numerical_columns_present:
        return px.line()  # Return an empty figure if no numerical columns are present

    # Handle invalid granularity
    if granularity not in ["D", "W", "ME", "QE", "YE"]:
        granularity = "ME"

    try:
        dff_resampled = (
            dff[numerical_columns_present].resample(granularity).sum().reset_index()
        )
    except Exception as e:
        print(f"Error during resampling: {e}")
        return px.line()  # Return an empty figure if resampling fails

    # Create line plot
    figure = px.line(dff_resampled, x="order_date", y=numerical_columns_present)
    figure.update_layout(title="Timeline Graph")
    return figure


# Callback for updating the bubble chart
@callback(
    Output("bubble-chart", "figure"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value"),
    Input("breakdown-dropdown", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def update_bubble_chart(x_axis, y_axis, breakdown, start_date, end_date):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date, errors="coerce")
    end_date = pd.to_datetime(end_date, errors="coerce")

    # Filter DataFrame
    dff = df[(df["order_date"] >= start_date) & (df["order_date"] <= end_date)]

    if dff.empty:
        return px.scatter()  # Return an empty figure if no data is available

    # Ensure x_axis and y_axis are present in the DataFrame
    if x_axis not in dff.columns or y_axis not in dff.columns:
        return px.scatter()  # Return an empty figure if any axis is missing

    # Create scatter plot
    figure = px.scatter(
        dff,
        x=x_axis,
        y=y_axis,
        size="quantity",
        color=breakdown,
        hover_name=breakdown,
        size_max=60,
    )
    figure.update_layout(title="Bubble Chart")
    return figure


# Callback to exclude selected axis in other dropdown
@callback(Output("y-axis-dropdown", "options"), Input("x-axis-dropdown", "value"))
def set_y_axis_options(selected_x):
    options = [
        {"label": col.replace("_", " ").title(), "value": col}
        for col in numerical_columns
    ]
    return [option for option in options if option["value"] != selected_x]


@callback(Output("x-axis-dropdown", "options"), Input("y-axis-dropdown", "value"))
def set_x_axis_options(selected_y):
    options = [
        {"label": col.replace("_", " ").title(), "value": col}
        for col in numerical_columns
    ]
    return [option for option in options if option["value"] != selected_y]
