"""Extract the 2011 OD matrices from JICA 2012 traffic survey Vol.4 appendix."""

import pandas as pd

from pipeline.common import REPO, pdf_text

PDF_PATH = REPO / "research/library/data-jica-2012-traffic-survey-vol04.pdf"
OUT_PATH = REPO / "data/processed/od_2011.parquet"

MARKERS = [
    ("person_all", "Person Trip OD Table"),
    ("motorcycle", "Motorcycle VT OD"),
    ("car", "Car VT OD"),
    ("truck", "Truck VT OD"),
    ("bus", "Bus VT OD"),
]


def _tables(lines):
    """Split pdftotext -layout output into column blocks (two per matrix).

    A block's rows are (label, values); label is an origin code, "Total",
    or None — the person block 2 prints no origin column, so its rows ride
    on block-1 origin order.
    """
    blocks, mode, cur = [], None, None
    for line in lines:
        hit = next((m for m, pat in MARKERS if pat in line), None)
        if hit:
            mode, cur = hit, None
            continue
        toks = line.split()
        if len(toks) >= 20 and all(t == "Total" or (len(t) == 3 and t.isdigit()) for t in toks):
            cur = {
                "mode": mode,
                "dests": [int(t) for t in toks if t.isdigit()],
                # car/truck/bus block-2 headers omit the "Total" label even
                # though their rows carry a total column; row width decides there
                "header_total": toks[-1] == "Total",
                "rows": [],
            }
            blocks.append(cur)
            continue
        if cur is None or not toks:
            continue
        label, vals = (toks[0], toks[1:]) if toks[0] == "Total" else (None, toks)
        nums = [t.replace(",", "") for t in vals]
        if not all(t.isdigit() for t in nums):
            continue
        nums = [int(t) for t in nums]
        n = len(cur["dests"])
        if label == "Total":
            if len(nums) not in (n, n + 1):
                continue
        elif len(nums) == n + 2 or (len(nums) == n + 1 and not cur["header_total"]):
            label, nums = nums[0], nums[1:]
        elif len(nums) != n + 1:
            continue
        cur["rows"].append((label, nums))
    return blocks


def _assemble(blocks):
    by_mode = {}
    for b in blocks:
        by_mode.setdefault(b["mode"], []).append(b)
    out = {}
    for mode, _ in MARKERS:
        b1, b2 = by_mode[mode]
        d1 = dict(b1["rows"])
        col_tot1 = d1.pop("Total")
        origins = [lab for lab, _ in b1["rows"] if lab != "Total"]
        rows2 = b2["rows"]
        if rows2[0][0] is None:
            # positional join: last unlabeled row is the column-totals row
            if len(rows2) != len(origins) + 1:
                raise ValueError(f"{mode}: block-2 row count != origins + totals row")
            d2 = dict(zip(origins, (v for _, v in rows2)))
            col_tot2 = rows2[-1][1]
        else:
            d2 = dict(rows2)
            col_tot2 = d2.pop("Total")
            if list(d2) != origins:
                raise ValueError(f"{mode}: block-2 origins != block-1 origins")
        n2 = len(b2["dests"])
        out[mode] = {
            "matrix": pd.DataFrame(
                [d1[o] + d2[o][:n2] for o in origins],
                index=origins, columns=b1["dests"] + b2["dests"]),
            "row_totals": pd.Series({o: d2[o][n2] for o in origins}),
            "col_totals": pd.Series(col_tot1 + col_tot2[:n2], index=b1["dests"] + b2["dests"]),
            "grand_total": col_tot2[n2],
        }
    return out


def extract(pdf_path):
    """Full printed matrices per mode, external zones (900/901) included."""
    out = _assemble(_tables(pdf_text(pdf_path).splitlines()))
    for mode, m in out.items():
        mat = m["matrix"]
        if not (mat.sum(axis=1) == m["row_totals"]).all():
            raise ValueError(f"{mode}: row sums != printed")
        # person table's printed column totals include an unprinted 901-origin
        # row; the shortfall must be nonnegative and account exactly for the
        # grand-total gap (zero gap for the vehicle tables => exact match)
        gap = m["col_totals"] - mat.sum()
        if not (gap >= 0).all():
            raise ValueError(f"{mode}: col sums exceed printed")
        if gap.sum() != m["grand_total"] - m["row_totals"].sum():
            raise ValueError(f"{mode}: grand total mismatch")
    return out


def build_long(mats):
    # person-table origins are the 50 survey zones; 900/901 are external-cordon
    # destinations/origins dropped from the deliverable
    zones = mats["person_all"]["matrix"].index
    parts = []
    for mode, m in mats.items():
        long = (m["matrix"].loc[zones, zones].stack().rename("trips")
                .rename_axis(["origin_zone", "dest_zone"]).reset_index())
        long.insert(2, "mode", mode)
        parts.append(long)
    return pd.concat(parts, ignore_index=True)


if __name__ == "__main__":
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    build_long(extract(PDF_PATH)).to_parquet(OUT_PATH, index=False)
