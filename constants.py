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
TITLE = "Collaborative Network Dashboard"
ST2 = "https://st2.newmexicowaterdata.org/FROST-Server/v1.1"
DEPTH_TO_WATER_FT_BGS = "Depth To Water (ft bgs)"

DTFORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
DEBUG_OBS = False
DEBUG_LIMIT_OBS = 0

USGS_BM = {
    "below": "traces",
    "sourcetype": "raster",
    "sourceattribution": 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>',
    "source": [
        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}",
    ],
}
# ============= EOF =============================================
