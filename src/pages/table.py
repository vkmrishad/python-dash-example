from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, html, dcc, callback, Output, Input, State, dash
from dash.exceptions import PreventUpdate
from dash import callback_context

from dash.exceptions import PreventUpdate
from sqlalchemy import func

from db.connection import SessionLocal
from db.crud import load_data, save_data, Order  # Ensure your CRUD functions are adapted for SQLAlchemy

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout definition
default_page_size = 25

table_page_layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("Data Table"))]),

    dcc.Loading(
        id="loading",
        type="default",
        children=[
            dbc.Row([
                dbc.Col([
                    dbc.Label("Country/Region"),
                    country_dropdown := dcc.Dropdown([], multi=False, style={'width': '100%'}),
                ], width=4),
                dbc.Col([
                    dbc.Label("State/Province"),
                    state_dropdown := dcc.Dropdown([], multi=False, style={'width': '100%'}),
                ], width=4),
                dbc.Col([
                    dbc.Label("City"),
                    city_dropdown := dcc.Dropdown([], multi=False, style={'width': '100%'}),
                ], width=4),
            ], justify="start", className='mt-2 mb-2'),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Category"),
                    category_dropdown := dcc.Dropdown([], multi=False, style={'width': '100%'}),
                ], width=4),
                dbc.Col([
                    dbc.Label("Sub-Category"),
                    sub_category_dropdown := dcc.Dropdown([], multi=False, style={'width': '100%'}),
                ], width=4),
            ], justify="start", className='mt-2 mb-2'),

            dbc.Row([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Show number of rows"),
                        page_size := dcc.Dropdown(
                            value=default_page_size, clearable=False, style={'width': '100%'},
                            options=[{'label': x, 'value': x} for x in [10, 25, 50, 100]]
                        ),
                    ], width=2),
                ], className='mt-2 mb-2'),
                dbc.Col([
                    my_table := dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in Order.__table__.columns.keys()],
                        data=[],
                        filter_action='none',
                        page_size=default_page_size,
                        style_table={'overflowX': 'auto'},
                    ),
                ]),
            ]),

            # Add these input fields and the "Add" button at the bottom of your layout
            dbc.Row([
                dbc.Col(dbc.Input(id='row-id-input', placeholder='Row ID', type='text', disabled=True), width=2),
                dbc.Col(dbc.Input(id='order-date-input', placeholder='Order Date', required='true', type='date'),
                        width=2),
                dbc.Col(dbc.Input(id='city-input', placeholder='City', required='true', type='text'), width=2),
                dbc.Col(
                    dbc.Input(id='state-province-input', placeholder='State/Province', required='true', type='text'),
                    width=2),
                dbc.Col(
                    dbc.Input(id='country-region-input', placeholder='Country/Region', required='true', type='text'),
                    width=2),
                dbc.Col(dbc.Input(id='category-input', placeholder='Category', required='true', type='text'), width=2),
                dbc.Col(dbc.Input(id='sub-category-input', placeholder='Sub-Category', required='true', type='text'),
                        width=2),
            ], className='mt-2 mb-2'),
            dbc.Row([
                dbc.Col(dbc.Button("Add", id='add-button', n_clicks=0), width=2),
            ], className='mt-2 mb-2'),
        ]
    ),

], fluid=True)


@callback(
    Output(country_dropdown, 'options'),
    Output(state_dropdown, 'options'),
    Output(city_dropdown, 'options'),
    Output(category_dropdown, 'options'),
    Output(sub_category_dropdown, 'options'),
    Input(country_dropdown, 'value'),
    Input(state_dropdown, 'value'),
    Input(category_dropdown, 'value')
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

        dff = query.all()
        dff = pd.DataFrame([o.__dict__ for o in dff])

        country_options = [{'label': country, 'value': country} for country in sorted(dff['country_region'].unique())]
        state_options = [{'label': state, 'value': state} for state in
                         sorted(dff['state_province'].unique())] if selected_country else []
        city_options = [{'label': city, 'value': city} for city in
                        sorted(dff['city'].unique())] if selected_state else []

        category_options = [{'label': cat, 'value': cat} for cat in sorted(dff['category'].unique())]
        sub_category_options = [{'label': sub_cat, 'value': sub_cat} for sub_cat in
                                sorted(dff['sub_category'].unique())] if selected_category else []

        return country_options, state_options, city_options, category_options, sub_category_options


@callback(
    Output(my_table, 'data', allow_duplicate=True),
    Output(my_table, 'page_size'),
    Input(country_dropdown, 'value'),
    Input(state_dropdown, 'value'),
    Input(city_dropdown, 'value'),
    Input(category_dropdown, 'value'),
    Input(sub_category_dropdown, 'value'),
    Input(page_size, 'value'),
    prevent_initial_call=True,
)
def update_table_data(country_v, state_v, city_v, category_v, sub_category_v, page_size):
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

        dff = query.all()

        aa = [
            {
                'id': r.id,
                'order_id': r.order_id,
                'order_date': r.order_date,
                'dispatch_date': r.dispatch_date,
                'delivery_mode': r.delivery_mode,
                'customer_id': r.customer_id,
                'customer_name': r.customer_name,
                'segment': r.segment,
                'city': r.city,
                'state_province': r.state_province,
                'country_region': r.country_region,
                'region': r.region,
                'product_id': r.product_id,
                'category': r.category,
                'sub_category': r.sub_category,
                'product_name': r.product_name,
                'sales': r.sales,
                'quantity': r.quantity,
                'discount': r.discount,
                'profit': r.profit
            }
            for r in dff
        ]

        # print(aa)

        # dff = pd.DataFrame(aa




        # aa = [list(row.__dict__.values()) for row in dff]

        # # Pagination
        # start_index = 0
        # end_index = page_size
        # paginated_data = dff[start_index:end_index]

        return aa, page_size

        # # Pagination
        # start_index = 0
        # end_index = page_size
        # paginated_data = dff[start_index:end_index]

        # print(paginated_data)

        # return [], page_size


@callback(
    Output('row-id-input', 'value'),
    Output(my_table, 'data'),
    Input('page-content', 'children'),
    Input('add-button', 'n_clicks'),
    State('order-date-input', 'value'),
    State('city-input', 'value'),
    State('state-province-input', 'value'),
    State('country-region-input', 'value'),
    State('category-input', 'value'),
    State('sub-category-input', 'value'),
    prevent_initial_call=True,
)
def update_table_and_row_id(page_content, n_clicks, order_date, city, state_province, country_region, category, sub_category):
    ctx = callback_context

    # Determine which input triggered the callback
    if not ctx.triggered:
        trigger_id = 'page-content'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    with SessionLocal() as session:
        max_id = session.query(func.max(Order.id)).scalar() or 0
        new_id = max_id + 1

        dff = session.query(Order).order_by(Order.id.desc()).all()
        aa = [
            {
                'id': r.id,
                'order_id': r.order_id,
                'order_date': r.order_date,
                'dispatch_date': r.dispatch_date,
                'delivery_mode': r.delivery_mode,
                'customer_id': r.customer_id,
                'customer_name': r.customer_name,
                'segment': r.segment,
                'city': r.city,
                'state_province': r.state_province,
                'country_region': r.country_region,
                'region': r.region,
                'product_id': r.product_id,
                'category': r.category,
                'sub_category': r.sub_category,
                'product_name': r.product_name,
                'sales': r.sales,
                'quantity': r.quantity,
                'discount': r.discount,
                'profit': r.profit
            }
            for r in dff
        ]

    if trigger_id == 'page-content':
        # Only update the Row ID input field when the page is loaded
        return new_id, aa

    elif trigger_id == 'add-button' and n_clicks > 0:
        with SessionLocal() as session:
            # Check for duplicates
            existing = session.query(Order).filter(
                Order.order_date == order_date,
                Order.city == city,
                Order.state_province == state_province,
                Order.country_region == country_region,
                Order.category == category,
                Order.sub_category == sub_category
            ).first()

            if not existing:
                new_row = Order(
                    id=new_id,
                    order_date=datetime.strptime(order_date, '%Y-%m-%d').date() if order_date else None,
                    city=city,
                    state_province=state_province,
                    country_region=country_region,
                    category=category,
                    sub_category=sub_category,
                )

                session.add(new_row)
                session.commit()

                # Refresh the data
                dff = session.query(Order).order_by(Order.id.desc()).all()
                aa = [
                    {
                        'id': r.id,
                        'order_id': r.order_id,
                        'order_date': r.order_date,
                        'dispatch_date': r.dispatch_date,
                        'delivery_mode': r.delivery_mode,
                        'customer_id': r.customer_id,
                        'customer_name': r.customer_name,
                        'segment': r.segment,
                        'city': r.city,
                        'state_province': r.state_province,
                        'country_region': r.country_region,
                        'region': r.region,
                        'product_id': r.product_id,
                        'category': r.category,
                        'sub_category': r.sub_category,
                        'product_name': r.product_name,
                        'sales': r.sales,
                        'quantity': r.quantity,
                        'discount': r.discount,
                        'profit': r.profit
                    }
                    for r in dff
                ]

                return new_id + 1, aa

    raise PreventUpdate
