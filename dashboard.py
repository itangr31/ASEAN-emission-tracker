import pandas as pd
import dash
from dash import html
from dash import dcc, ctx
import plotly.express as px
import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash_bootstrap_components._components.Container import Container


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("ASEAN Emission Dashboard", href="#", className="ms-3",
                            style={"fontSize": "30px", "fontWeight": "bold", "color": "white"}),
            dbc.Nav(
                [
                    # Label for 'Year' dropdown
                    dbc.Label("Year:", className="me-5 mt-2",style={"color": "white", "fontSize": "24px"}),  # Add margin to right

                    # Year dropdown
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("2016", href="#"),
                            dbc.DropdownMenuItem("2017", href="#"),
                            dbc.DropdownMenuItem("2018", href="#"),
                            dbc.DropdownMenuItem("2019", href="#"),
                            dbc.DropdownMenuItem("2020", href="#"),
                            dbc.DropdownMenuItem("2021", href="#"),
                            dbc.DropdownMenuItem("2022", href="#"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Select Year",
                    ),

                    # Spacer for separation
                    html.Div(style={"width": "80px"}),  # Add a small gap between dropdowns

                    # Label for 'Gas Type' dropdown
                    dbc.Label("Gas Type:", className="me-5 mt-2", style={"color": "white", "fontSize": "24px"}),

                    # Gas Type dropdown
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("co2", href="#"),
                            dbc.DropdownMenuItem("ch4", href="#"),
                            dbc.DropdownMenuItem("n20", href="#"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Select Gas Type",
                    ),
                ],
                className="ms-auto d-flex align-items-center",  # Align everything to the right
                navbar=True,
            ),
        ],
        fluid=True,  # Full width container
    ),
    color="dark",
    dark=True,
)

def data_for_boxes(header,text):
    card_content = [
        dbc.CardHeader(header,
                       style={"fontSize": "30px", "fontWeight": "bold", "textAlign": "center"}),  # Header styling,
        dbc.CardBody(
            [
            dcc.Markdown(dangerously_allow_html = True,
            children=["{}".format(text)],
            style={"fontSize": "50px", "textAlign": "center"})
            ]
        )
    ]
    return card_content

box_maps = html.Div(
    [
        dbc.Row([
            dbc.Col(dbc.Card(data_for_boxes("Difference from last year",100),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'470px','padding':'12px 12px 12px 12px'}),
            dbc.Col(dbc.Card(data_for_boxes("Biggest Sector Emitters",100),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'470px','padding':'12px 12px 12px 12px'}),
            dbc.Col(dbc.Card(data_for_boxes("Emission per Capita",100),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'470px','padding':'12px 12px 12px 12px'}),
            dbc.Col(dbc.Card(data_for_boxes("Total Emission",100),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'470px','padding':'12px 12px 12px 12px'})
    
        ],
        style={"marginBottom":"3vh"}), #Add spacing below this row
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("GHG Emission Heatmap",style={"fontSize": "20px", "textAlign": "center"}),color='primary',inverse=True),style = {'text-align':'center',"height":"3vh"})
        ]),
        dbc.Row([
            dbc.Col(dbc.Card([
                html.Div(
                className="div-map-chart",
                children=[
                    dcc.Graph(id="map-chart",
                              style={"height":"61vh"})
                ]
            ),
            ]))
        ],style={"marginBottom":"1vh"}),
        dbc.Row([
            html.Button('Reset to ASEAN',id='btn-click',n_clicks=0)
        ])
    ]

)

graphs = html.Div(
    [
        html.P('graphs')
    ]
)

app.layout = dbc.Container(
    [
    dbc.Row(
        [dbc.Col(header,width=12)
        ],
        style={"height":"10vh"}

    ),
    dbc.Row(
        [
        dbc.Col(graphs, width=4),
        dbc.Col(box_maps, width = 8, className='bg-light')
        ],
        style={"height":"90vh"}
        ),
    ],
fluid=True
)

style_header = {'backgroundColor':'rgb(224,224,224)',
                    'fontWeight':'bold',
                    'border':'4px solid white',
                    'fontSize':'12px'
                    },

if __name__ == "__main__":
    app.run_server()