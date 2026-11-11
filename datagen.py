"""Synthetic dialysis billing data generator (shared by server and CSV builder)."""
import csv, random

DIS = ["Diabetic Nephropathy", "Hypertensive Nephropathy", "Chronic Glomerulonephritis",
       "Polycystic Kidney Disease", "Acute Kidney Injury", "Obstructive Uropathy"]
DW = [34, 28, 14, 8, 10, 6]
FAC = [("Apex Renal Care", "NephroLife", 9, 2600), ("Lotus Dialysis Centre", "NephroLife", 7, 2400),
       ("Sai Kidney Institute", "NephroLife", 6, 2200), ("Metro Renal Hub", "CarePlus Network", 10, 3300),
       ("Green Valley Dialysis", "CarePlus Network", 6, 2800), ("Sunrise Nephrology", "CarePlus Network", 8, 3000),
       ("City Care Dialysis", "Unity Health", 7, 2500), ("Riverside Renal Unit", "Unity Health", 5, 2300)]
FW = [9, 6, 5, 10, 5, 8, 6, 4]
PM = ["Insurance", "Government Scheme", "Cash", "Card", "Corporate Tie-up"]
PW = [30, 28, 16, 14, 12]
DR = {"Insurance": .12, "Government Scheme": .26, "Cash": .06, "Card": .04, "Corporate Tie-up": .16}
FIELDS = ["id", "age", "ag", "g", "dis", "fac", "chain", "st", "pm", "mo", "sess", "billed", "paid", "stations"]
INTS = {"age", "mo", "sess", "billed", "paid", "stations"}

def make(rng, n, mo=None):
    f = rng.choices(FAC, FW)[0]
    dis = rng.choices(DIS, DW)[0]
    pm = rng.choices(PM, PW)[0]
    age = int(max(18, min(88, round(58 + (rng.random() + rng.random() + rng.random() - 1.5) * 28))))
    ag = "18-29" if age < 30 else "30-44" if age < 45 else "45-59" if age < 60 else "60-74" if age < 75 else "75+"
    sess = round(6 + rng.random() * 10)
    billed = round(sess * f[3] * (0.9 + rng.random() * .25))
    dp = DR[pm] * (0.5 + rng.random())
    if f[0] == "Metro Renal Hub" and pm == "Insurance":
        dp += .08
    dp = min(.6, dp)
    if rng.random() < .35 and pm != "Government Scheme":
        dp = 0
    return {"id": "P%d" % (1000 + n), "age": age, "ag": ag, "g": "Male" if rng.random() < .58 else "Female",
            "dis": dis, "fac": f[0], "chain": f[1], "st": "S%d" % (1 + int(rng.random() * f[2])), "pm": pm,
            "mo": rng.randrange(12) if mo is None else mo, "sess": sess, "billed": billed,
            "paid": round(billed * (1 - dp)), "stations": f[2]}

def write_csv(path, n=1400, seed=42):
    rng = random.Random(seed)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS); w.writeheader()
        for i in range(1, n + 1):
            w.writerow(make(rng, i))

def read_csv(path):
    with open(path, newline="") as fh:
        return [{k: (int(v) if k in INTS else v) for k, v in r.items()} for r in csv.DictReader(fh)]

if __name__ == "__main__":
    write_csv("data/patients.csv"); print("Wrote data/patients.csv")
