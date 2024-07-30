from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, callback_context, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from sqlalchemy import func

from src.db.connection import SessionLocal
from src.db.crud import order_to_dict
from src.db.model import Order

default_page_size = 25


table_page_layout = dbc.Container(
    [
        dbc.Row([dbc.Col(html.H2("Data Table"))]),
        html.Br(),
        dcc.Loading(
            id="loading",
            type="default",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Country/Region"),
                                country_dropdown := dcc.Dropdown(
                                    [], multi=False, style={"width": "100%"}
                                ),
                            ],
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("State/Province"),
                                state_dropdown := dcc.Dropdown(
                                    [], multi=False, style={"width": "100%"}
                                ),
                            ],
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("City"),
                                city_dropdown := dcc.Dropdown(
                                    [], multi=False, style={"width": "100%"}
                                ),
                            ],
                            width=4,
                        ),
                    ],
                    justify="start",
                    className="mt-2 mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Category"),
                                category_dropdown := dcc.Dropdown(
                                    [], multi=False, style={"width": "100%"}
                                ),
                            ],
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Sub-Category"),
                                sub_category_dropdown := dcc.Dropdown(
                                    [], multi=False, style={"width": "100%"}
                                ),
                            ],
                            width=4,
                        ),
                    ],
                    justify="start",
                    className="mt-2 mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Show number of rows"),
                                        page_size := dcc.Dropdown(
                                            value=default_page_size,
                                            clearable=False,
                                            style={"width": "100%"},
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [10, 25, 50, 100]
                                            ],
                                        ),
                                    ],
                                    width=2,
                                ),
                            ],
                            className="mt-2 mb-2",
                        ),
                        dbc.Col(
                            [
                                my_table := dash_table.DataTable(
                                    columns=[
                                        {"name": i, "id": i}
                                        for i in Order.__table__.columns.keys()
                                    ],
                                    data=[],
                                    filter_action="none",
                                    page_size=default_page_size,
                                    style_table={"overflowX": "auto"},
                                ),
                            ]
                        ),
                    ]
                ),
                # Add these input fields and the "Add" button at the bottom of your layout
                html.Br(),
                dbc.Row([dbc.Col(html.H4("Add Record"))]),
                # Alerts for success and error messages
                dbc.Row(
                    [
                        dbc.Alert(
                            "Record added successfully!",
                            id="success-alert",
                            color="success",
                            is_open=False,
                            dismissable=True,
                            duration=10000,
                        ),
                        dbc.Alert(
                            """An error occurred while adding the record.
                * All fields are required.
                * Order ID should be unique
            """,
                            id="error-alert",
                            color="danger",
                            is_open=False,
                            dismissable=True,
                            duration=10000,
                        ),
                    ],
                    className="mt-2 mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="id-input",
                                placeholder="ID",
                                type="text",
                                disabled=True,
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="order-id-input",
                                placeholder="Order ID",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="order-date-input",
                                placeholder="Order Date",
                                required=True,
                                type="date",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="dispatch-date-input",
                                placeholder="Dispatch Date",
                                required=True,
                                type="date",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="delivery-mode-input",
                                placeholder="Delivery Mode",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="customer-id-input",
                                placeholder="Customer ID",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                    ],
                    className="mt-2 mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="customer-name-input",
                                placeholder="Customer Name",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="segment-input",
                                placeholder="Segment",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="city-input",
                                placeholder="City",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="state-province-input",
                                placeholder="State/Province",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="country-region-input",
                                placeholder="Country/Region",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="region-input",
                                placeholder="Region",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                    ],
                    className="mt-2 mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="product-id-input",
                                placeholder="Product ID",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="category-input",
                                placeholder="Category",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="sub-category-input",
                                placeholder="Sub-Category",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="product-name-input",
                                placeholder="Product Name",
                                required=True,
                                type="text",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="sales-input",
                                placeholder="Sales",
                                required=True,
                                type="number",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="quantity-input",
                                placeholder="Quantity",
                                required=True,
                                type="number",
                            ),
                            width=2,
                        ),
                    ],
                    className="mt-2 mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="discount-input",
                                placeholder="Discount",
                                required=True,
                                type="number",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="profit-input",
                                placeholder="Profit",
                                required=True,
                                type="number",
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Button("Add", id="add-button", n_clicks=0), width=2
                        ),
                    ],
                    className="mt-2 mb-2",
                ),
            ],
        ),
    ],
    fluid=True,
)


@callback(
    Output(country_dropdown, "options"),
    Output(state_dropdown, "options"),
    Output(city_dropdown, "options"),
    Output(category_dropdown, "options"),
    Output(sub_category_dropdown, "options"),
    Input(country_dropdown, "value"),
    Input(state_dropdown, "value"),
    Input(category_dropdown, "value"),
)
def set_dropdown_options(selected_country, selected_state, selected_category):
    with SessionLocal() as session:
        query = session.query(Order)
        if selected_country:
            query = query.filter(Order.country_region == selected_country)
        if selected_state:
            query = query.filter(Order.state_province == selected_state)
        if selected_category:
            query = query.filter(Order.category == selected_category)

        orders = query.order_by(Order.id.desc()).all()
        df = pd.DataFrame([o.__dict__ for o in orders])

        country_options = [
            {"label": country, "value": country}
            for country in sorted(df["country_region"].unique())
        ]
        state_options = (
            [
                {"label": state, "value": state}
                for state in sorted(df["state_province"].unique())
            ]
            if selected_country
            else []
        )
        city_options = (
            [{"label": city, "value": city} for city in sorted(df["city"].unique())]
            if selected_state
            else []
        )

        category_options = [
            {"label": cat, "value": cat} for cat in sorted(df["category"].unique())
        ]
        sub_category_options = (
            [
                {"label": sub_cat, "value": sub_cat}
                for sub_cat in sorted(df["sub_category"].unique())
            ]
            if selected_category
            else []
        )

        return (
            country_options,
            state_options,
            city_options,
            category_options,
            sub_category_options,
        )


@callback(
    Output(my_table, "data", allow_duplicate=True),
    Output(my_table, "page_size"),
    Input(country_dropdown, "value"),
    Input(state_dropdown, "value"),
    Input(city_dropdown, "value"),
    Input(category_dropdown, "value"),
    Input(sub_category_dropdown, "value"),
    Input(page_size, "value"),
    prevent_initial_call=True,
)
def update_table_data(
    country_v, state_v, city_v, category_v, sub_category_v, page_size
):
    with SessionLocal() as session:
        query = session.query(Order)
        if country_v:
            query = query.filter(Order.country_region == country_v)
        if state_v:
            query = query.filter(Order.state_province == state_v)
        if city_v:
            query = query.filter(Order.city == city_v)
        if category_v:
            query = query.filter(Order.category == category_v)
        if sub_category_v:
            query = query.filter(Order.sub_category == sub_category_v)

        orders = query.order_by(Order.id.desc()).all()
        results = order_to_dict(orders)

        return results, page_size


@callback(
    Output("id-input", "value"),
    Output(my_table, "data"),
    Output("success-alert", "is_open"),
    Output("error-alert", "is_open"),
    [
        Output(f'{field.replace("_", "-")}-input', "value")
        for field in Order.__table__.columns.keys()
        if field != "id"
    ],
    Input("page-content", "children"),
    Input("add-button", "n_clicks"),
    State("order-id-input", "value"),
    State("order-date-input", "value"),
    State("dispatch-date-input", "value"),
    State("delivery-mode-input", "value"),
    State("customer-id-input", "value"),
    State("customer-name-input", "value"),
    State("segment-input", "value"),
    State("city-input", "value"),
    State("state-province-input", "value"),
    State("country-region-input", "value"),
    State("region-input", "value"),
    State("product-id-input", "value"),
    State("category-input", "value"),
    State("sub-category-input", "value"),
    State("product-name-input", "value"),
    State("sales-input", "value"),
    State("quantity-input", "value"),
    State("discount-input", "value"),
    State("profit-input", "value"),
    prevent_initial_call=True,
)
def update_table_and_row_id(
    page_content,
    n_clicks,
    order_id,
    order_date,
    dispatch_date,
    delivery_mode,
    customer_id,
    customer_name,
    segment,
    city,
    state_province,
    country_region,
    region,
    product_id,
    category,
    sub_category,
    product_name,
    sales,
    quantity,
    discount,
    profit,
):
    ctx = callback_context
    clear_inputs = [""] * (len(Order.__table__.columns.keys()) - 1)
    values = [
        order_id,
        order_date,
        dispatch_date,
        delivery_mode,
        customer_id,
        customer_name,
        segment,
        city,
        state_province,
        country_region,
        region,
        product_id,
        category,
        sub_category,
        product_name,
        sales,
        quantity,
        discount,
        profit,
    ]

    # Determine which input triggered the callback
    if not ctx.triggered:
        trigger_id = "page-content"
    else:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    with SessionLocal() as session:
        max_id = session.query(func.max(Order.id)).scalar() or 0
        new_id = max_id + 1

        orders = session.query(Order).order_by(Order.id.desc()).all()
        results = order_to_dict(orders)

    if trigger_id == "page-content":
        # Only update the Row ID input field when the page is loaded
        return [new_id, results, False, False] + clear_inputs

    elif trigger_id == "add-button" and n_clicks > 0:
        with SessionLocal() as session:
            # Check for duplicates order_id
            existing = session.query(Order).filter(Order.order_id == order_id).first()

            if not all(values):
                return [new_id, results, False, True] + values

            if not existing:
                new_row = Order(
                    id=new_id,
                    order_id=order_id,
                    order_date=datetime.strptime(order_date, "%Y-%m-%d").date()
                    if order_date
                    else None,
                    dispatch_date=datetime.strptime(dispatch_date, "%Y-%m-%d").date()
                    if dispatch_date
                    else None,
                    delivery_mode=delivery_mode,
                    customer_id=customer_id,
                    customer_name=customer_name,
                    segment=segment,
                    city=city,
                    state_province=state_province,
                    country_region=country_region,
                    region=region,
                    product_id=product_id,
                    category=category,
                    sub_category=sub_category,
                    product_name=product_name,
                    sales=sales,
                    quantity=quantity,
                    discount=discount,
                    profit=profit,
                )

                session.add(new_row)
                session.commit()

                # Refresh the data
                orders = session.query(Order).order_by(Order.id.desc()).all()
                results = order_to_dict(orders)

                return [new_id + 1, results, True, False] + clear_inputs

            else:
                return [new_id, results, False, True] + values

    raise PreventUpdate
