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
import datetime
import pprint

import requests

from constants import DEBUG_OBS, DTFORMAT, ST2, DEBUG_LIMIT_OBS


def get_location(name=None):
    if name:
        url = f"{ST2}/Locations?$filter=name eq '{name}'"
        resp = requests.get(url)
        if resp.status_code == 200:
            try:
                return resp.json()["value"][0]
            except IndexError:
                print(f"no location found for {name}")


def get_observations(location_iotid=None, datastream_id=None, limit=1000, dsname=None):
    if DEBUG_OBS:
        now = datetime.datetime.now()
        t0 = now - datetime.timedelta(hours=0)
        t1 = now - datetime.timedelta(hours=12)
        t2 = now - datetime.timedelta(hours=24)
        l = {"name": "Foo"}
        obs = [
            {
                "phenomenonTime": t0.strftime(DTFORMAT),
                "result": 0,
            },
            {
                "phenomenonTime": t1.strftime(DTFORMAT),
                "result": 0,
            },
            {
                "phenomenonTime": t2.strftime(DTFORMAT),
                "result": 0,
            },
        ]
        return l, obs

    obs, location = None, None
    if datastream_id is None:
        url = f"{ST2}/Locations({location_iotid})?$expand=Things/Datastreams"
        resp = requests.get(url)

        if resp.status_code == 200:
            location = resp.json()
            ds = location["Things"][0]["Datastreams"]
            pprint.pprint(ds)
            if dsname:
                for di in ds:
                    if di["name"] == dsname:
                        datastream_id = di["@iot.id"]
                        break
            else:
                datastream_id = ds[0]["@iot.id"]
    else:
        location = None

    if DEBUG_LIMIT_OBS:
        limit = DEBUG_LIMIT_OBS

    if datastream_id:
        url = (
            f"{ST2}/Datastreams({datastream_id})/Observations?$orderby=phenomenonTime desc&$select=phenomenonTime,"
            f"result&$top={limit}"
        )

        resp = requests.get(url)
        if resp.status_code == 200:
            j = resp.json()
            obs = j["value"]
            nextlink = j.get("@iot.nextLink")

            while len(obs) < limit and nextlink:
                resp = requests.get(nextlink)
                if resp.status_code == 200:
                    j = resp.json()
                    obs.extend(j["value"])
                    nextlink = j.get("@iot.nextLink")

    return location, obs


# ============= EOF =============================================
