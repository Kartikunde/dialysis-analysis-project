# Analysis of Patient Data: Dialysis Care (Healthcare)

Live dashboard + analysis for dialysis patients across chains, facilities and stations,
including payment modes and discounts.

## Run (Python 3.8+, no installs)
    python server.py
    # open http://localhost:8000

The server loads `data/patients.csv` (auto-created on first run) and streams a new patient
billing record every 2 seconds, so KPIs, charts, insights and tables update in real time.
New records are also appended to the CSV. Options: `PORT=9000 INTERVAL=1 python server.py`.
Charts load Chart.js from a CDN, so the browser needs internet access.

## Files
| File | Purpose |
|---|---|
| server.py | HTTP server: `/api/data` (JSON) and `/stream` (live Server-Sent Events) |
| datagen.py | Synthetic data generator (`python datagen.py` rebuilds the CSV) |
| static/index.html | Dashboard UI: filters, KPIs, charts, facility/station table, auto insights, CSV export |
| analysis.py | Pandas analysis, writes `reports/summary.txt` (`pip install pandas`) |
| data/patients.csv | Dataset |

## Use your own data
Replace `data/patients.csv` with a file having the same columns:
`id, age, ag, g, dis, fac, chain, st, pm, mo, sess, billed, paid, stations`
(ag = age group, g = gender, dis = disease, fac = facility, st = station, pm = payment mode,
mo = month index 0-11, sess = sessions, billed/paid = amounts, stations = stations at the facility).
Update the lists in `datagen.py` and the constants at the top of `static/index.html` if your category names differ.
Stop the live feed by removing the `producer` thread start in `server.py`.

## Analysis covered
1. Patient and disease distribution by age and gender
2. Chain, facility and dialysis station utilisation
3. Payment mode split, discounts and billed vs collected gap
4. Automatic insights and recommendations
