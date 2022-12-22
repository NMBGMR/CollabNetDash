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
import pprint

import dash_bootstrap_components as dbc
from dash import (
    Dash,
    html,
    dcc,
    Output,
    Input,
    DiskcacheManager,
    CeleryManager,
    ctx,
    State,
)
import plotly.express as px
import plotly.graph_objects as go

from app import dash_app
from mainlayout import load_layout, xaxis, yaxis, maplayout
from flask_caching import Cache

from st import get_observations, get_location

load_layout(dash_app)

app = dash_app.server
config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_DIR": "/tmp/cache",
}
cache = Cache(app, config=config)


@cache.memoize()
def get_obs(*args, **kw):
    return get_observations(*args, **kw)


@cache.memoize()
def get_loc(*args, **kw):
    return get_location(*args, **kw)


@dash_app.callback(
    Output("download_selected_csv", "data"),
    [Input("download_selected_btn", "n_clicks"),
     State("hydrograph", "figure")],
    prevent_initial_call=True,
)
def handle_download_selected(n, fig):
    if ctx.triggered_id == "download_selected_btn":
        return make_fig_csv(fig)


def make_fig_csv(fig):
    data = fig["data"]
    if data:
        content = [
            "please cite this data: New Mexico Water Data Initiative https://newmexicowaterdata.org"
        ]
        for di in data:
            content.append(f'location_name: {di["name"]}')
            content.append(f"measurement_timestamp, depth_to_water_ft_bgs")
            for xi, yi in zip(di["x"], di["y"]):
                row = f"{xi},{yi}"
                content.append(row)

        content = "\n".join(content)
        return dict(content=content, filename="download.csv")


# make callbacks
@dash_app.callback([Output('hydrograph', 'figure'),
                    Output('observationstable', 'data')],
                   [Input('point_id_search_btn', 'n_clicks'),
                    State('point_id_search', 'value'),
                    # State('map', 'figure')
                    ]
                   # prevent_initial_call=True
                   )
# def handle_point_id_search(n, v, figmap):
def handle_point_id_search(n, v):
    loc, totalobs = None, []
    fd = []
    if n and v:
        loc = get_loc(v)
        if loc:
            for dsname in ('Groundwater Levels',
                           'Groundwater Levels(Pressure)',
                           'Groundwater Levels(Acoustic)'):
                _, obs = get_obs(loc['@iot.id'], dsname=dsname)
                if obs:
                    # print('nasadfme', name, len(obs), len(uxs) if uxs else 0)
                    obs = sorted(obs, key=lambda x: x["phenomenonTime"])

                    xs = [xi["phenomenonTime"] for xi in obs]
                    ys = [xi["result"] for xi in obs]

                    fd.append(go.Scatter(x=xs, y=ys, name=dsname))
                    totalobs.extend(obs)
            # locations = [loc]
            # lats = [l["location"]["coordinates"][1] for l in locations]
            # lons = [l["location"]["coordinates"][0] for l in locations]
            # ids = [l["name"] for l in locations]
            #
            # mapdata = [go.Scattermapbox(lat=lats, lon=lons, text=ids,
            #                             marker={'size': 15, 'color': 'blue'})]
            # figmap['data'] = mapdata
            # figmap = px.scatter_mapbox(lat=lats, lon=lons, text=ids, size=[15,],
            #                            mapbox_style="open-street-map")
            # figmap['data'][0]['lat'] = lats
            # figmap['data'][0]['lon'] = lons
            # figmap['data'][0]['name'] = 'selection'

            # print('fas', figmap)
    # else:
    #     figmap = px.scatter_mapbox(lat=[], lon=[], mapbox_style="open-street-map")
        # mapdata = [go.Scattermapbox()]
        # figmap = go.Figure(layout=maplayout, data=mapdata)




    layout = dict(
        height=350,
        margin=dict(t=50, b=50, l=50, r=25),
        xaxis=xaxis,
        yaxis=yaxis,
        title=loc["name"] if loc else "",
        # paper_bgcolor=chart_bgcolor,
    )

    fig = go.Figure(data=fd, layout=layout)

    return fig, totalobs


if __name__ == "__main__":
    dash_app.run_server(debug=True, port=8051)
# ============= EOF =============================================
