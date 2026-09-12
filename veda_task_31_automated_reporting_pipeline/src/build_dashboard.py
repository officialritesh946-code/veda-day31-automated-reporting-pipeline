"""Build a lightweight HTML dashboard from pipeline output files."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import base64

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "output"
ASSETS = ROOT / "dashboard" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

def chart(df, x, y, title, name):
    fig, ax = plt.subplots(figsize=(8,4.5))
    ax.bar(df[x].astype(str), df[y])
    ax.set_title(title)
    ax.set_ylabel("Attrition rate")
    ax.yaxis.set_major_formatter(lambda v, pos: f"{v:.0%}")
    fig.tight_layout()
    p = ASSETS/name
    fig.savefig(p, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return p

# Extend this script with your preferred layout or Power BI export if required.
print("Dashboard assets can be rebuilt from data/output/*.csv")
