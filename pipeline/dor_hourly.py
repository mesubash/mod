"""Hourly traffic profiles from the DoR SSRN traffic-count portal.

Source: https://ssrn.dor.gov.np/traffic_controller/get_detail/<station>/<id>
The detail pages carry per-hour, per-direction counts by vehicle class for the
survey days behind each station-year AADT row in
research/library/data-dor-ssrn-aadt-kathmandu-valley-stations.csv.

Output data/processed/hourly_profile.parquet: station, location, date, hour,
total_veh, plus the pooled share-of-daily per hour used as the A1 departure
profile (specs/model-spec.md §4).
"""

import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict

import pandas as pd

from pipeline.common import REPO

# Latest (FY 2024/25) detail pages for three valley stations: the corridor's own
# Arniko Highway crossing, a Ring Road station, and a southern radial. Detail
# ids come from the AADT scrape's hourly_detail_url column.
STATIONS = {
    64: ("Manohara Bridge", "Manohara Bridge/1582"),
    65: ("Ring Road (Sinamangal)", "Ring Road -2Sinamangal-1/1583"),
    58: ("Satdobato South (Chapagaun)", "Satdobato South -2Chapagaun-1/1578"),
}
BASE = "https://ssrn.dor.gov.np/traffic_controller/get_detail/"
TOTAL_COL = 34  # both-direction total, last cell of each hourly row


def fetch(path):
    url = BASE + urllib.parse.quote(path)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "ignore")


def parse(html, station, location):
    body = html[html.find("Bullock Cart"):]
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        cells = [
            re.sub(r"<[^>]+>", "", c).replace("\xa0", "").strip()
            for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        ]
        if len(cells) > TOTAL_COL and re.match(r"\d{4}-\d{2}-\d{2}", cells[0]):
            rows.append(
                {
                    "station": station,
                    "location": location,
                    "date": cells[0],
                    "hour": int(cells[1][:2]),
                    "total_veh": float(cells[TOTAL_COL]),
                }
            )
    if not rows:
        raise ValueError(f"no hourly rows parsed for {location}")
    return rows


def hourly_shares(df):
    """Share of daily traffic per hour, pooled over stations and survey days."""
    per_day = df.groupby(["station", "date"])["total_veh"].transform("sum")
    df = df.assign(share=df["total_veh"] / per_day)
    return df.groupby("hour")["share"].mean()


def main():
    rows = []
    for station, (location, path) in STATIONS.items():
        rows += parse(fetch(path), station, location)
    df = pd.DataFrame(rows)
    out = REPO / "data/processed/hourly_profile.parquet"
    df.to_parquet(out, index=False)

    shares = hourly_shares(df)
    print(f"{out}: {len(df)} station-day-hours, {df['station'].nunique()} stations")
    for hour, share in shares.items():
        print(f"  {hour:02d}:00  {share * 100:5.2f}%")
    print(f"08-11 window: {shares.loc[8:10].sum() * 100:.1f}%")


if __name__ == "__main__":
    sys.exit(main())
