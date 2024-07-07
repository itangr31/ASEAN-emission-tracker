import pandas as pd
import dash
from dash import html
from dash import dcc, ctx
import plotly.express as px
import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

#Read Dataset

df_all = pd.read_csv("df_asean.csv")
df_all.reset_index(inplace=True)
df_all = df_all[(df_all["gas"] != "co2e_100yr") & (df_all["gas"]!="co2e_20yr")]

f =open("world-administrative-boundaries.geojson")
geojson_1 = json.load(f)

#Dash App

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])

#App Layout

#Dropdown
controls = dbc.Card([

    html.Div(
        [
            dbc.Label("Gas Type"),
            dcc.Dropdown(
                id="gas-dropdown",
                options=[{"label":"All","value":"all"}]+
                [{"label":i,"value":i}for i in df_all["gas"].unique()],
                value="all"  
            ),
        ]
    ),
    html.Div(
        [
            dbc.Label("Sector"),
            dcc.Dropdown(
                id="sector-dropdown",
                options=[{"label":"All","value":"all"}]+
                [{"label":j,"value":j}for j in df_all["sector"].unique()],
                value="all"
            ),
        ]
    ),html.Div(
        [
            dbc.Label("Year"),
            dcc.Slider(
                df_all["Year"].min(),
                df_all["Year"].max(),
                step=1,
                id="year-slider",
                value=df_all["Year"].max(),
                marks = {str(year): str(year) for year in df_all["Year"].unique()}
            ),
        ]
    )
],body=True,
)
trends = dbc.Card([
    
    html.Div(
        className="div-trend-chart",
        children=[
            dcc.Graph(id="trend-chart")
        ]
    ),
    html.Br(),
    html.Div(
        className="div-subsector-chart",
        children=[
            dcc.Graph(id="subsector-chart")
        ]
    )


],)
graphics = html.Div([
                dbc.Card([html.Div(
                            className="div-map-chart",
                            children=[
                            dcc.Graph(id="map-chart")]
                        ),
                        html.Br(),
                        html.Div(
                            className="div-bar-chart",
                            children=[
                            " Select country in map to filter bar chart by country",
                            dcc.Graph(id="bar-chart")
                            ]
                        ),
html.Button('Reset to ASEAN',id='btn-click',n_clicks=0),]),])

app.layout = dbc.Container([
    html.H1("ASEAN Emissions Tracker"),
    html.Hr(),
    dbc.Row([
        dbc.Col([controls,trends],md=5),
        dbc.Col([graphics],lg=7)
    ])
],style={"max-width":"none"})

@app.callback(
    Output("map-chart","figure"),
    [Input("gas-dropdown","value"),Input("sector-dropdown","value"),Input("year-slider","value")]
)
def update_chart(gas,sector,year):
    df = df_all[df_all["Year"] == year]
    if(gas == 'all' and sector == 'all'):
        df = df.groupby("iso3_country",as_index=False)[["emissions_quantity"]].sum()
    elif(gas!='all' and sector == 'all'):
        df = df[df["gas"] == gas]
        df = df.groupby("iso3_country",as_index=False)[["emissions_quantity"]].sum()
    elif(gas=='all' and sector != 'all'):
        df = df[df["sector"] == sector]
        df = df.groupby("iso3_country",as_index=False)[["emissions_quantity"]].sum()
    else:
        df = df[(df["sector"] == sector) & (df["gas"] == gas)]
        df = df.groupby("iso3_country",as_index=False)[["emissions_quantity"]].sum()
    fig = px.choropleth_mapbox(df, geojson=geojson_1, color="emissions_quantity",
                                   locations="iso3_country", featureidkey="properties.color_code",height=600,
                                   color_continuous_scale="jet",
                                   center={"lat": 1.3521, "lon": 103.8198},zoom=3,
                                   labels={'emissions_quantity':'tonnes'})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_coloraxes(colorbar={'orientation':'h','y': -0.1})
    return fig
@app.callback(
    Output("map-chart", "clickData"),
    Input("btn-click", "n_clicks")
)
def reset_to_asean(*args):
    return None

@app.callback(
    Output("bar-chart","figure"),
    [Input("gas-dropdown","value"),Input("sector-dropdown","value"),Input("year-slider","value"),Input("map-chart","clickData")]
)
def update_bar_chart(gas,sector,year,country):
    if(gas == 'all' and sector == 'all' and country is None ):
        dff = df_all[df_all["Year"]==year]
        dff = dff.groupby(["sector","gas"],as_index=False)[["emissions_quantity"]].sum()
        figg = px.bar(dff,x="sector",y="emissions_quantity",color="gas",title="ASEAN",template="plotly_white")
        return figg
    elif(gas == 'all' and sector == 'all'):
        selected_country = country["points"][0]["location"]
        dff = df_all[(df_all["Year"] == year) & (df_all["iso3_country"] == selected_country)]
        dff = dff.groupby(["sector","gas"],as_index=False)[["emissions_quantity"]].sum()
        figg = px.bar(dff,x="sector",y="emissions_quantity",color="gas",title=f"{selected_country}",template="plotly_white")
        return figg
    elif(gas != 'all' and sector == 'all'):
        if country is None:
            dff = df_all[(df_all["Year"] == year) & (df_all["gas"] == gas)]
            selected_country = "ASEAN"
        else:
            selected_country = country["points"][0]["location"]
            dff = df_all[(df_all["Year"] == year) & (df_all["gas"] == gas) & (df_all["iso3_country"] == selected_country)]
        dff = dff.groupby(["sector","gas"],as_index=False)[["emissions_quantity"]].sum()
        figg = px.bar(dff,x="sector",y="emissions_quantity",color="sector",title=f"{selected_country}",template="plotly_white")
        return figg
    elif(gas == 'all' and sector != 'all'):
        if country is None:
            dff = df_all[(df_all["Year"] == year) & (df_all["sector"] == sector)]
            selected_country = "ASEAN"
        else:
            selected_country = country["points"][0]["location"]
            dff = df_all[(df_all["Year"] == year) & (df_all["sector"] == sector) &(df_all["iso3_country"] == selected_country)]
        dff = dff.groupby(["original_inventory_sector","gas"],as_index=False)[["emissions_quantity"]].sum()
        figg = px.bar(dff,x="original_inventory_sector",y="emissions_quantity",color="gas",title=f"{selected_country}",template="plotly_white")
        return figg
    elif(gas != 'all' and sector != 'all'):
        if country is None:
            dff = df_all[(df_all["Year"] == year) & (df_all["sector"] == sector) & (df_all["gas"] == gas)]
            selected_country = "ASEAN"
        else:
            selected_country = country["points"][0]["location"]
            dff = df_all[(df_all["Year"] == year) & (df_all["sector"] == sector) & (df_all["gas"] == gas) & (df_all["iso3_country"] == selected_country)]
        dff = dff.groupby("original_inventory_sector",as_index=False)[["emissions_quantity"]].sum()
        figg = px.bar(dff,x="original_inventory_sector",y="emissions_quantity",color="original_inventory_sector",title=f"{selected_country}",template="plotly_white")
        return figg

@app.callback(
    Output("trend-chart","figure"),
    [Input("gas-dropdown","value"),Input("sector-dropdown","value"),Input("year-slider","value"),Input("map-chart","clickData")]
)
def update_trend_chart(gas,sector,year,country):
    if(gas == 'all' and sector == 'all' and country is None):
        df = df_all[df_all["Year"] <= year]
        df = df.groupby(["gas","Year"],as_index=False)[["emissions_quantity"]].sum()
        fig = px.line(df,x="Year",y="emissions_quantity",color="gas",template="plotly_white")
        fig.update_xaxes(dtick=1)
        return fig

@app.callback(
    Output("subsector-chart","figure"),
    [Input("gas-dropdown","value"),Input("sector-dropdown","value"),Input("year-slider","value"),Input("map-chart","clickData")]
)
def update_subsector_chart(gas,sector,year,country):
    if(gas == 'all' and sector == 'all' and country is None):
        df = df_all[df_all["Year"] <= year]
        df = df.groupby(["iso3_country","Year"],as_index=False)[["emissions_quantity"]].sum()
        fig = px.line(df,x="Year",y="emissions_quantity",color="iso3_country",template="plotly_white")
        fig.update_xaxes(dtick=1)
        return fig



#Run App
if __name__ == '__main__':
    app.run_server()