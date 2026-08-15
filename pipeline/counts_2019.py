"""JICA 2019 Appendix 4 traffic counts -> data/processed/counts_2019.parquet.

Schema (long): intersection str, leg int, direction {in,out}, metric
{observed_pcu, hours_observed, pcu_24h}, value float. 77 leg-directions
x 3 metrics = 231 rows. Tinkune is three sub-intersections (South/West/
North); "Jadhibuti" keeps the source spelling.

ponytail: only Table 4.1 (daily leg summaries) is text in the PDF; the
15-min classified turning-movement data exists solely as embedded images
(spec sheets A4-2..11, flow diagrams, pie/line charts). Upgrade path:
OCR/camelot pass over those pages.
"""

import re

import pandas as pd

from pipeline.common import REPO, pdf_text

PDF = REPO / "research/library/data-jica-2019-urban-transport-survey-vol02.pdf"
OUT = REPO / "data/processed/counts_2019.parquet"

# one leg-direction record: name, leg, direction, observed PCU, hours, 24h PCU
ROW = re.compile(
    r"([A-Za-z][A-Za-z ]*?)\s+(\d)\s+(in|out|Out)\s+([\d,]+)\s+(15|14\.75|14\.5)\s+([\d,]+)"
)


def extract() -> pd.DataFrame:
    text = pdf_text(PDF)
    # regex could match tabular text elsewhere in the 151-page report
    table = text[text.index("Table 4.1 Summary of Traffic Volume Data"):]
    table = table[: table.index("Appendix 5")]

    rows = []
    for name, leg, direction, obs, hours, day in ROW.findall(table):
        for metric, value in (
            ("observed_pcu", float(obs.replace(",", ""))),
            ("hours_observed", float(hours)),
            ("pcu_24h", float(day.replace(",", ""))),
        ):
            rows.append((name, int(leg), direction.lower(), metric, value))
    df = pd.DataFrame(
        rows, columns=["intersection", "leg", "direction", "metric", "value"]
    )
    # trust boundary: Table 4.1 has exactly 77 leg-direction rows
    if len(df) != 231:
        raise ValueError(f"expected 231 rows from Table 4.1, parsed {len(df)}")
    return df


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    extract().to_parquet(OUT, index=False)
    print(f"wrote {OUT}")
