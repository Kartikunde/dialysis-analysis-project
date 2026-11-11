"""Offline analysis of data/patients.csv. Run: python analysis.py  (needs pandas)"""
import pandas as pd

df = pd.read_csv("data/patients.csv").drop_duplicates("id")
df["discount"] = df.billed - df.paid
df["discount_pct"] = df.discount / df.billed * 100
out = []
def sec(title, t):
    out.append("\n=== %s ===\n%s" % (title, t.to_string()))

sec("Dataset overview", df.describe().round(1))
sec("Patients by disease", df.dis.value_counts())
sec("Age group x gender", pd.crosstab(df.ag, df.g))
sec("Chain summary", df.groupby("chain").agg(patients=("id", "count"), billed=("billed", "sum"),
    collected=("paid", "sum"), discount_pct=("discount_pct", "mean")).round(1))
fac = df.groupby("fac").agg(chain=("chain", "first"), patients=("id", "count"), stations=("stations", "first"),
    sessions=("sess", "sum"), billed=("billed", "sum"), discount_pct=("discount_pct", "mean"))
fac["sessions_per_station"] = (fac.sessions / fac.stations).round(0)
sec("Facility and station utilisation", fac.round(1).sort_values("sessions_per_station", ascending=False))
sec("Payment mode: share and discounts", df.groupby("pm").agg(records=("id", "count"),
    avg_discount_pct=("discount_pct", "mean"), total_discount=("discount", "sum")).round(1))
sec("Discount % by facility x payment mode", df.pivot_table(index="fac", columns="pm", values="discount_pct", aggfunc="mean").round(1))
text = "\n".join(out)
print(text)
open("reports/summary.txt", "w").write(text)
