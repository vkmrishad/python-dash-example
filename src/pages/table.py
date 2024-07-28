import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
from dash import callback_context

from db.database import load_data, save_data

# Load the data
df = load_data()

default_page_size = 25

# Define the layout for the table page
table_page_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Data Table")),
    ]),

    dcc.Loading(
        id="loading",
        type="default",
        children=[
            dbc.Row([
                dbc.Col([
                    dbc.Label("Country/Region"),
                    country_dropdown := dcc.Dropdown([x for x in sorted(df['Country/Region'].unique())], multi=False,
                                                     style={'width': '100%'}),
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
                    category_dropdown := dcc.Dropdown([x for x in sorted(df['Category'].unique())], multi=False,
                                                      style={'width': '100%'}),
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
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
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
    Output(state_dropdown, 'options'),
    Output(city_dropdown, 'options'),
    Output(category_dropdown, 'options'),
    Output(sub_category_dropdown, 'options'),
    Input(country_dropdown, 'value'),
    Input(state_dropdown, 'value'),
    Input(category_dropdown, 'value')
)
def set_dropdown_options(selected_country, selected_state, selected_category):
    dff = df.copy()

    state_options = []
    city_options = []
    sub_category_options = []

    if selected_country:
        dff = dff[dff['Country/Region'] == selected_country]
        state_options = [{'label': state, 'value': state} for state in sorted(dff['State/Province'].unique())]

    if selected_state:
        dff = dff[dff['State/Province'] == selected_state]
        city_options = [{'label': city, 'value': city} for city in sorted(dff['City'].unique())]

    if selected_category:
        dff = dff[dff['Category'] == selected_category]
        sub_category_options = [{'label': sub_cat, 'value': sub_cat} for sub_cat in
                                sorted(dff['Sub-Category'].unique())]

    return state_options, city_options, [{'label': cat, 'value': cat} for cat in
                                         sorted(df['Category'].unique())], sub_category_options


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
def update_table_data(country_v, state_v, city_v, category_v, sub_category_v, row_v):
    dff = df.copy()

    if country_v:
        dff = dff[dff['Country/Region'] == country_v]

    if state_v:
        dff = dff[dff['State/Province'] == state_v]

    if city_v:
        dff = dff[dff['City'] == city_v]

    if category_v:
        dff = dff[dff['Category'] == category_v]

    if sub_category_v:
        dff = dff[dff['Sub-Category'] == sub_category_v]

    return dff.to_dict('records'), row_v


@callback(
    Output('row-id-input', 'value'),
    Output(my_table, 'data'),
    Input('page-content', 'children'),  # Assuming 'page-content' is the container for the page layout
    Input('add-button', 'n_clicks'),
    State(my_table, 'data'),
    State('order-date-input', 'value'),
    State('city-input', 'value'),
    State('state-province-input', 'value'),
    State('country-region-input', 'value'),
    State('category-input', 'value'),
    State('sub-category-input', 'value')
)
def update_table_and_row_id(page_content, n_clicks, table_data, order_date, city, state_province, country_region, category, sub_category):
    ctx = callback_context

    # Determine which input triggered the callback
    if not ctx.triggered:
        trigger_id = 'page-content'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Load the data
    df = load_data()

    # Generate the new Row ID
    new_row_id = df['Row ID'].max() + 1

    if trigger_id == 'page-content':
        # Only update the Row ID input field when the page is loaded
        return new_row_id, table_data

    elif trigger_id == 'add-button' and n_clicks > 0:
        # Check for duplicates
        if df[(df['Order Date'] == order_date) & (df['City'] == city) & (df['State/Province'] == state_province) &
              (df['Country/Region'] == country_region) & (df['Category'] == category) & (df['Sub-Category'] == sub_category)].empty:
            # Create the new row
            new_row = {
                'Row ID': new_row_id,
                'Order Date': order_date,
                'City': city,
                'State/Province': state_province,
                'Country/Region': country_region,
                'Category': category,
                'Sub-Category': sub_category
            }

            # Append the new row to the DataFrame
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Save the updated DataFrame to the Excel file
            save_data(df)

            # Return updated data and new Row ID
            return new_row_id + 1, df.to_dict('records')

    raise PreventUpdate
