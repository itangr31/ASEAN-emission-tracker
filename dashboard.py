import pandas as pd
import dash
from dash import html
from dash import dcc, ctx
import plotly.express as px
import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash_bootstrap_components._components.Container import Container

#Read Dataset

df_all = pd.read_csv("https://github.com/itangr31/ASEAN-emission-tracker/blob/0fd0e3e9da1b097382231e3ffacefb19a374a475/df_asean.csv?raw=true")#Annual Country Dataset
df_all = df_all[df_all["sector"] != "forestry-and-land-use"]
df_all = df_all.iloc[:,2:]

df_map = pd.read_csv('df_asean_emission_sources.csv')#Emission Source Datase
df_map = df_map.iloc[:,1:]


app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                "ASEAN Emissions Dashboard",
                href="#",
                className="ms-3",
                style={"fontSize": "30px", "fontWeight": "bold", "color": "white"}
            ),
            dbc.Nav(
                [
                    html.Div(
                        [
                            dbc.Label("Country:", className="me-2", style={"color": "white", "fontSize": "20px"}),
                            dcc.Dropdown(
                                id="country-dropdown",
                                options=[
                                    {"label": "ASEAN", "value": "all"},
                                    {"label": "Brunei Darussalam", "value": "BRN"},
                                    {"label": "Cambodia", "value": "KHM"},
                                    {"label": "Indonesia", "value": "IDN"},
                                    {"label": "Lao PDR", "value": "LAO"},
                                    {"label": "Malaysia", "value": "MYS"},
                                    {"label": "Myanmar", "value": "MMR"},
                                    {"label": "Philippines", "value": "PHL"},
                                    {"label": "Singapore", "value": "SGP"},
                                    {"label": "Thailand", "value": "THA"},
                                    {"label": "Viet Nam", "value": "VNM"},
                                ],
                                value = "all",
                                placeholder="Select Country/Region",
                                style={"width": "200px", "marginRight": "20px"},
                            ),
                        ],
                        className="d-flex align-items-center"
                    ),
                    # Year Dropdown
                    html.Div(
                        [
                            dbc.Label("Year:", className="me-2", style={"color": "white", "fontSize": "20px"}),
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=[
                                    {"label": "2016", "value": "2016"},
                                    {"label": "2017", "value": "2017"},
                                    {"label": "2018", "value": "2018"},
                                    {"label": "2019", "value": "2019"},
                                    {"label": "2020", "value": "2020"},
                                    {"label": "2021", "value": "2021"},
                                    {"label": "2022", "value": "2022"},
                                ],
                                value="2022",
                                placeholder="Select Year",
                                style={"width": "200px", "marginRight": "20px"},
                            ),
                        ],
                        className="d-flex align-items-center"
                    ),

                    # Gas Type Dropdown
                    html.Div(
                        [
                            dbc.Label("Gas Type:", className="me-2", style={"color": "white", "fontSize": "20px"}),
                            dcc.Dropdown(
                                id="gas-dropdown",
                                options=[
                                    {"label": "CO2", "value": "co2"},
                                    {"label": "CH4", "value": "ch4"},
                                    {"label": "N2O", "value": "n20"},
                                ],
                                value="co2",
                                placeholder="Select Gas Type",
                                style={"width": "200px"},
                            ),
                        ],
                        className="d-flex align-items-center"
                    ),
                ],
                className="ms-auto d-flex align-items-center",  # Align to the right
                navbar=True,
            ),
        ],
        fluid=True,  # Full width container
    ),
    color="dark",
    dark=True,
)

def data_for_boxes(header, idname):
    """
    Generates card content for Dash Bootstrap Components with a dynamic ID for updating content.

    Parameters:
        header (str): The title of the card.
        idname (str): The unique ID for the card body where content will be updated.

    Returns:
        dbc.Card: A Dash Bootstrap Card component with a header and a body that can be updated dynamically.
    """
    card_content = dbc.Card(
        [
            dbc.CardHeader(header, style={"fontSize": "2vh", "fontWeight": "bold", "textAlign": "center"}),
            dbc.CardBody(
                html.Div(id=idname, style={"fontSize": "3vh", "textAlign": "center"})  # Dynamic content placeholder
            )
        ],
        color='primary',
        inverse=True,
        style={'text-align': 'center', "height": "15vh"}
    )
    return card_content

box_maps = html.Div(
    [
        dbc.Row([
            dbc.Col(dbc.Card(data_for_boxes("Difference from Last Year", "difference-card"),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'16.5vw','padding':'12px 12px 12px 12px'},width="auto"),
            dbc.Col(dbc.Card(data_for_boxes("Biggest Sector Emitters", "sector-card"),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'16.5vw','padding':'12px 12px 12px 12px'},width="auto"),
            dbc.Col(dbc.Card(data_for_boxes("Emissions per Capita", "per-capita-card"),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'16.5vw','padding':'12px 12px 12px 12px'},width="auto"),
            dbc.Col(dbc.Card(data_for_boxes("Total Emissions", "total-emission-card"),color = 'primary',style = {'text-align':'center',"height":"15vh"}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'width':'16.5vw','padding':'12px 12px 12px 12px'},width="auto")
    
        ],
        style={"marginBottom":"3vh"}), #Add spacing below this row
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("GHG Emissions Heatmap",style={"fontSize": "20px", "textAlign": "center",'padding':'12px 12px 12px 12px'}),color='primary',inverse=True),style = {'text-align':'center',"height":"3vh"})
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
        ],style={"marginBottom":"1vh"})
    ]

)

graphs = html.Div([

    dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("Emissions Treemap",style={"fontSize": "20px", "textAlign": "center",'padding':'12px 12px 12px 12px'}),color='primary',inverse=True),style = {'text-align':'center',"height":"3vh"})
        ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.Div(
                    className="div-treemap-chart",
                    children=[
                        dcc.Graph(id='treemap-chart',
                                  style={"height": "40vh", "width": "100%"} )
                    ]
                )
            ])
        )
    ],
    style={"marginBottom":"3vh"}),
    dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody("Total Emissions Time Series",style={"fontSize": "20px", "textAlign": "center",'padding':'12px 12px 12px 12px'}),color='primary',inverse=True),style = {'text-align':'center',"height":"3vh"})
        ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.Div(
                    className="div-timeseries-chart",
                    children=[
                        dcc.Graph(id='timeseries-chart',
                                  style={"height":"35vh"})
                    ]
                )
            ])
        )
    ])



])
app.layout = dbc.Container(
    [
    dbc.Row(
        [dbc.Col(header,width=12)
        ],
        style={"height":"8vh"}

    ),
    dbc.Row(
        [
        dbc.Col(graphs, width=4),
        dbc.Col(box_maps, width = 8, className='bg-light')
        ],
        style={"height":"92vh"}
        ),
    ],
fluid=True
)

#Treemap Chart Callback
@app.callback(
    Output("treemap-chart","figure"),
    [Input("country-dropdown","value"),Input("year-dropdown","value"),Input("gas-dropdown","value")]
)
def update_chart(country, year, gas):
    # Filter data based on inputs
    if country == 'all':
        df = df_all[(df_all["Year"] == int(year)) & (df_all["gas"] == gas)]
        if df.empty:
            print("Filtered DataFrame is empty for 'all' countries")
            return px.treemap(title="No data available for the selected filters.")

        df = df.groupby(["iso3_country"], as_index=False)["emissions_quantity"].sum()
        path = "iso3_country"
        label = "Country"
    else:
        df = df_all[(df_all["Year"] == int(year)) & (df_all["gas"] == gas) & (df_all["iso3_country"] == country)]
        if df.empty:
            print("Filtered DataFrame is empty for country:", country)
            return px.treemap(title="No data available for the selected filters.")

        df = df.groupby(["sector"], as_index=False)["emissions_quantity"].sum()
        path = "sector"
        label = "Sector"

    df["scaled_emissions"] = df["emissions_quantity"]/1000000 
    # Create treemap
    fig = px.treemap(
        df,
        path=[path],
        values="scaled_emissions",
        color=path
    )
    fig.data[0].textinfo = 'label+percent parent+value'
    fig.data[0].texttemplate = '%{label}<br><br>%{value:.2f} MT<br>Share: %{percentParent:.1%}'


# Update font style and size for text
    fig.data[0].textfont = dict(
        size=16,  # Increase font size
        family="Arial Black",  # Specify font family (optional)
        color="black"  # Specify font color (optional)
    )

# Update layout
    fig.update_layout(
        title={
            "text": f"Emission Breakdown by {label} ({year}, MT{gas.upper()})",
            "y": 0.95,  # Position of the title (closer to the top)
            "x": 0.5,   # Center the title
            "xanchor": "center",
            "yanchor": "top"
        },
        uniformtext=dict(minsize=18, mode='hide'),
        margin=dict(t=50, l=25, r=25, b=25)
    )
    return fig

#Timeseries Callback
@app.callback(
    Output("timeseries-chart","figure"),
    [Input("country-dropdown","value"),Input("year-dropdown","value"),Input("gas-dropdown","value")]
)

def update_chart(country, year, gas):
    if country == 'all':
        df = df_all[(df_all["Year"] <= int(year)) & (df_all["gas"] == gas)]
        if df.empty:
            print("Filtered DataFrame is empty for 'all' countries")
            return px.area(title="No data available for the selected filters.")
    else:
        df = df_all[(df_all["Year"] <= int(year)) & (df_all["gas"] == gas) & (df_all["iso3_country"] == country)]
        if df.empty:
            print("Filtered DataFrame is empty for country:", country)
            return px.area(title="No data available for the selected filters.")

    # Ensure 'Year' is an integer
    df["Year"] = df["Year"].astype(int)

    # Group the data
    df = df.groupby(["Year", "sector"], as_index=False)["emissions_quantity"].sum()

    # Create the figure
    fig = px.area(df, x="Year", y="emissions_quantity", color="sector", template="simple_white",
                  labels=dict(emissions_quantity=f"Tonnes {gas.upper()}e"))

    # Update layout for proper integer axis
    fig.update_layout(
        legend=dict(
            orientation="h",  # Make the legend horizontal
            yanchor="bottom",  # Align the legend vertically
            y=1.02,  # Position it above the graph
            xanchor="center",  # Align the legend horizontally
            x=0.5,  # Center the legend
            font=dict(size=16)  # Increase legend font size
        ),
        xaxis=dict(
            title_font=dict(size=20),  # Increase x-axis label font size
            tickmode='linear',  # Use a linear tick mode for integers
            dtick=1,  # Set the interval for ticks to 1 year
            tickformat=None,  # Remove unnecessary formatting
        ),
        yaxis=dict(
            title_font=dict(size=20)  # Increase y-axis label font size
        ),
        font=dict(size=18)  # Increase the overall font size for the chart
    )
    return fig

#Heatmap Callback
@app.callback(
    Output("map-chart","figure"),
    [Input("country-dropdown","value"),Input("year-dropdown","value"),Input("gas-dropdown","value")]
)

def update_chart(country, year, gas):
    # Define the center coordinates and zoom levels for each country
    country_centers = {
        "BRN": {"lat": 4.5353, "lon": 114.7277, "zoom": 7},
        "KHM": {"lat": 12.5657, "lon": 104.9910, "zoom": 7},
        "LAO": {"lat": 19.8563, "lon": 102.4955, "zoom": 6},
        "IDN": {"lat": -0.7893, "lon": 113.9213, "zoom": 5},
        "MYS": {"lat": 4.2105, "lon": 101.9758, "zoom": 5},
        "MMR": {"lat": 21.9162, "lon": 95.9560, "zoom": 6},
        "PHL": {"lat": 12.8797, "lon": 121.7740, "zoom": 6},
        "SGP": {"lat": 1.3521, "lon": 103.8198, "zoom": 10},
        "THA": {"lat": 15.8700, "lon": 100.9925, "zoom": 6},
        "VNM": {"lat": 14.0583, "lon": 108.2772, "zoom": 6}  # Vietnam added
    }
    
    # Precompute 99th percentile values for each gas type
    gas_quantiles = {
        gas_type: df_map[df_map["gas"] == gas_type]["emissions_quantity"].quantile(0.99)
        for gas_type in df_map["gas"].unique()
    }
    
    # Get the range_max for the selected gas
    range_max = gas_quantiles.get(gas, 1)  # Default to 1 if gas is not in the dataset
    
    # If 'all', use ASEAN region's center and default zoom
    if country == 'all':
        df = df_map[(df_map["Year"] == int(year)) & (df_map["gas"] == gas)]
        center = {"lat": 5, "lon": 115}
        zoom = 4
        radius = 10
        if df.empty:
            print("Filtered DataFrame is empty for 'all' countries")
            return px.density_mapbox(title="No data available for the selected filters.")
    else:
        # Use country-specific center and zoom
        df = df_map[(df_map["Year"] == int(year)) & (df_map["gas"] == gas) & (df_map["iso3_country"] == country)]
        country_data = country_centers.get(country, {"lat": 5, "lon": 115, "zoom": 4})  # Default values
        center = {"lat": country_data["lat"], "lon": country_data["lon"]}
        zoom = country_data["zoom"]
        radius = 20
        if df.empty:
            print(f"Filtered DataFrame is empty for country: {country}")
            return px.density_mapbox(title="No data available for the selected filters.")
    
    fig = px.density_mapbox(
        df,
        lat='lat',
        lon='lon',
        z='emissions_quantity',
        radius=radius,  # Increase radius for denser hotspots
        center=center,
        zoom=zoom,
        mapbox_style="carto-positron",
        color_continuous_scale="rainbow",  # Keep rainbow scale
        labels={"emissions_quantity": f"t{gas}"},
        range_color=(0, range_max)  # Apply precomputed gas-specific quantile
    )

    # Update layout for clearer hotspots and thicker colors
    fig.update_layout(
        autosize=True,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title=f"t{gas}",
            titleside="top",
            ticks="outside",
            tickformat=".0f",  # Format tick labels as integers
            dtick=(range_max / 5),  # Divide tick marks into 5 levels
        )
    )
    return fig

@app.callback(
    [
        Output('difference-card', 'children'),
        Output('sector-card', 'children'),
        Output('per-capita-card', 'children'),
        Output('total-emission-card', 'children')
    ],
    [
        Input('year-dropdown', 'value'),
        Input('country-dropdown', 'value'),
        Input('gas-dropdown', 'value')
    ]
)
def update_cards(year, country, gas):
    if country == 'all':
        df = df_all[(df_all["Year"] >= int(year)-1) & (df_all["gas"] == gas)]
        if df.empty:
            print("Filtered DataFrame is empty for 'all' countries")
            return "No data available for the selected filters."
    else:
        df = df_all[(df_all["Year"] >= int(year)-1) & (df_all["gas"] == gas) & (df_all["iso3_country"] == country)]
        if df.empty:
            print("Filtered DataFrame is empty for country:", country)
            return "No data available for the selected filters."
    #Difference from last year
    df_diff = df.groupby(["Year"],as_index=False)["emissions_quantity"].sum()
    df_diff_prev = df_diff[df_diff["Year"] == int(year)-1]["emissions_quantity"].values
    df_diff_current = df_diff[df_diff["Year"] == int(year)]["emissions_quantity"].values

    df_diff = (df_diff_current-df_diff_prev)/df_diff_prev*100
    if df_diff<0:
        annot = ""
    else:
        annot = "+"
    df_diff = round(df_diff[0],2)    
    difference_data = f"{annot}{df_diff}%"

    #Biggest Sector Emitters
    df_sector = df.groupby(["sector"],as_index=False)["emissions_quantity"].sum()
    max_emission_sector = df_sector.loc[df_sector["emissions_quantity"].idxmax()]
    sector_name = str(max_emission_sector["sector"]).capitalize()
    sector_data = f"{sector_name}"

    #Emission per capita

    # Adjusting the population_data DataFrame to reflect the provided data
    population_data = pd.DataFrame({
        "Year": [2016, 2017, 2018, 2019, 2020, 2021, 2022] * 11,
        "iso3_country": ["all", "BRN", "KHM", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM"] * 7,
         "Population": [
            635260800, 423200, 15762400, 258705000, 6758400, 31187300, 52885200, 103663800, 5607300, 67454700, 93250700,
            642278600, 429500, 16005400, 262787000, 6858200, 31623000, 53382800, 105172900, 5612300, 67653200, 94286000,
            648454700, 421300, 16249800, 266927000, 6957700, 32049700, 53905400, 106651400, 5638700, 67831600, 95385200,
            652469000, 429500, 16486500, 270203000, 7058000, 32382300, 54452000, 108116600, 5703600, 65557100, 96484000,
            658878800, 437500, 16718900, 273523600, 7169500, 32697000, 54808000, 109581100, 5685800, 65421100, 97582700,
            663850300, 445400, 16926000, 276361800, 7275600, 32776200, 55073000, 111046900, 5453600, 65213000, 98506200,
            671680000, 453600, 17168600, 279134500, 7379400, 32776200, 55227000, 112508000, 5637000, 65497000, 99462000
            ]
        })
    
    total_emissions = df["emissions_quantity"].sum()

  
    population = population_data[
        (population_data["Year"] == int(year)) & 
        (population_data["iso3_country"] == country)
    ]["Population"].values
    
    emissions_per_capita = total_emissions / population[0]




    per_capita_data = f"{round(emissions_per_capita,2)}\nt{gas.upper()} per capita"
    total_emission_data = f"{round(total_emissions/1000000,2)} MT{gas.upper()}"

    return (
        difference_data,
        sector_data,
        per_capita_data,
        total_emission_data
    )
        




style_header = {'backgroundColor':'primary',
                    'fontWeight':'bold',
                    'border':'4px solid white',
                    'fontSize':'12px'
                    },

if __name__ == "__main__":
    app.run_server(debug=False)
