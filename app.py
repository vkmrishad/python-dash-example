from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from src.pages.landing import landing_page_layout
from src.pages.table import table_page_layout
from src.pages.graph import graph_page_layout, register_callbacks

# Initialize the Dash app with Bootstrap theme and suppress callback exceptions
app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, 'assets/css/style.css'], suppress_callback_exceptions=True)
app.title = "Superstore Dashboard"


# Define the callback for navigating between pages
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/table':
        return table_page_layout
    elif pathname == '/graph':
        return graph_page_layout
    elif pathname == '/landing':
        return landing_page_layout
    else:
        return dcc.Location(id='redirect', href='/landing', refresh=True)


# Define the main app layout with a sidebar for navigation and a top navbar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Superstore Dashboard", href="/"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Landing", href="/landing", active="exact")),
                    dbc.NavItem(dbc.NavLink("Table", href="/table", active="exact")),
                    dbc.NavItem(dbc.NavLink("Graph", href="/graph", active="exact")),
                ], className="me-auto", navbar=True),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            )
        ], fluid=True),
        color="primary",
        dark=True,
        className="navbar-expand-lg w-100",
    ),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavLink("Landing", href="/landing", active="exact"),
                    dbc.NavLink("Table", href="/table", active="exact"),
                    dbc.NavLink("Graph", href="/graph", active="exact"),
                ], vertical=True, pills=True, className="sidebar"),
            ], width=2, className="d-none d-md-block", id="sidebar"),  # Hide sidebar on screens smaller than md
            dbc.Col(html.Div(id='page-content', className="page-content"), width=10, md=10),
            # Take full width on small screens
        ], className="mt-4"),
    ], fluid=True, id="content"),
    html.Footer([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.P("© 2024 Superstore Dashboard"), className="text-center")
            ]),
        ])
    ], className="footer mt-auto py-3 bg-light"),
], style={"padding": "0"})


# Redirect callback
@app.callback(
    Output('redirect', 'pathname'),
    [Input('url', 'pathname')]
)
def redirect_to_landing(pathname):
    if pathname in ['/', '']:
        return '/landing'
    return pathname


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Register the callbacks for the graph page
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
