# ===============================================================================
# Copyright 2022 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dash_table import DataTable

from constants import TITLE, DEPTH_TO_WATER_FT_BGS, USGS_BM

chart_bgcolor = "#b5aeae"
chart_bgcolor = "white"
card_style = {
    "border": "solid",
    "borderRadius": "10px",
    "marginBlock": "3px",
    "backgroundColor": chart_bgcolor,
    "boxShadow": "2px 2px #8d9ea2",
    "borderColor": "7d777a",
}

banner_style = card_style.copy()
# banner_style['background-image']="url('assets/new-mexico-408068_1280.jpg')"
banner_style["background-image"] = "url('assets/1599247175576.jpg')"
banner_style["background-repeat"] = "no-repeat"
# banner_style["background-attachment"]= "fixed"
banner_style["background-size"] = "cover"
# banner_style['background-image']="url('assets/pvacd_logo.png')"
banner_row = dbc.Row(
    [
        dbc.Col(
            # html.A(
            #     href="https://newmexicowaterdata.org",
            #     children=[html.Img(src="assets/newmexicowaterdatalogo.png")],
            # ),
            width=3,
        ),
        dbc.Col(
            html.H1(TITLE, style={"margin-top": "10px"}),
            width=6,
        ),
        dbc.Col(
            # html.A(
            #     href="https://pvacd.com",
            #     children=[
            #         html.Img(
            #             src="assets/pvacd_logo.png",
            #             style={"height": "80%", "margin": "10px"},
            #         )
            #     ],
            # ),
            width=3,
        ),
    ],
    style=banner_style,
)
subbanner_row = dbc.Row(
    [
        html.Div(
            [
                # dbc.Button(
                #     "Pecos Slope Story Map",
                #     color="secondary",
                #     style={"margin": "5px"},
                #     href="https://nmt.maps.arcgis.com/apps/Cascade/index.html?appid=2f22f13a81f04042aabcfbe2e739ca96",
                # )
            ],
            style=card_style,
        )
    ]
)

yaxis = dict(autorange="reversed", title=DEPTH_TO_WATER_FT_BGS, fixedrange=False)

xaxis = dict(
    title="Time",
    rangeselector=dict(
        buttons=list(
            [
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ),
    rangeslider=dict(visible=True),
    type="date",
)

maplayout = go.Layout(
    mapbox_style="open-street-map",
    # mapbox_layers=[USGS_BM],
    mapbox={"zoom": 5, "center": {"lat": 35.25, "lon": -106.5}},
    margin={"r": 10, "t": 30, "l": 10, "b": 20},
    height=450,
    paper_bgcolor=chart_bgcolor,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.66,
        bgcolor="#899DBE",
        borderwidth=3,
    ),
)

tablecomp = DataTable(
    id="observationstable",
    style_cell={"textAlign": "left"},
    columns=[{"name": "Measurement Timestamp", "id": "phenomenonTime"},
             {"name": "Value", "id": "result"}],
    style_as_list_view=True,
    # style_header=header_style,
    # style_data=data_style,
    style_table={"height": "300px", "overflowY": "auto"},
)


def load_layout(app):
    hydrocomp = dcc.Graph(id="hydrograph")
    # figmap = go.Figure(layout=maplayout, data=[go.Scattermapbox(marker={'size': 15, 'color': 'blue'})])
    # mapcomp = dcc.Graph(id="map", figure=figmap)

    children = [
        banner_row,
        # subbanner_row,
        dbc.Row(dbc.Col(
            children=[dbc.Input(id='point_id_search', value='MG-030'),
                      dbc.Button("Search", id='point_id_search_btn')]
        )),
        dbc.Row(
            dbc.Spinner(
                [html.Div(id="loading-output"), hydrocomp],
                # fullscreen=True,
                color="primary",
            ),
        ),
        dbc.Row(dbc.Col([dbc.Button(
                                "Download CSV",
                                style={"margin": "5px"},
                                color="secondary",
                                size="sm",
                                title="Download all the water levels for the selected location"
                                " as a single csv file",
                                id="download_selected_btn",
                            ),
                            dcc.Download(id="download_selected_csv"),],width=3)),
        dbc.Row(
            tablecomp
        )
    ]

    app.layout = dbc.Container(children)
# ============= EOF =============================================
