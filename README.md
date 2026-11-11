# Dialysis Analytics Dashboard

**Analysis of Patient Data (Healthcare domain)**: a live, real-time dashboard and analysis toolkit for patients undergoing dialysis. It covers patient and disease patterns, chain, facility and dialysis station performance, and payment modes with the discounts and payment reductions applied to them.

> All data in this repository is **synthetic**. It contains no real patient information.

---

## Features

- **Real-time updates**: the server streams a new patient billing record every 2 seconds (Server-Sent Events), and the dashboard refreshes automatically.
- **Filters**: chain, disease and payment mode, applied to every chart, KPI and table at once.
- **KPIs**: patients, total sessions, billed amount, collected amount, discount given and discount rate.
- **Patient analysis**: patients by disease, and age group split by gender.
- **Facility, chain and station analysis**: billed vs collected per chain, and a facility table with patients, stations, sessions per station and discount %.
- **Payment and discount analysis**: payment mode share, average discount % by mode, and a monthly billed vs collected trend.
- **Auto-generated insights**: most common disease, deepest-discount payment mode, busiest and quietest facilities, and the facility with the highest discount rate.
- **CSV export** of the currently filtered records, and light/dark theme support.
- **Offline analysis script** (pandas) that writes a text report.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3 standard library (`http.server`), no installs needed |
| Live feed | Server-Sent Events (`/stream`) |
| Frontend | HTML, CSS, vanilla JavaScript, [Chart.js](https://www.chartjs.org/) (loaded from CDN) |
| Analysis | pandas (optional, only for `analysis.py`) |

## Project structure

```
dialysis-analysis-project/
├── server.py            # HTTP server: static files, /api/data, /stream
├── datagen.py           # Synthetic data generator (shared by server and CSV builder)
├── analysis.py          # Offline pandas analysis -> reports/summary.txt
├── static/
│   └── index.html       # Dashboard UI
├── data/
│   └── patients.csv     # Dataset (1,400 starter records, grows while the server runs)
├── reports/
│   └── summary.txt      # Sample analysis output
├── requirements.txt
└── README.md
```

## API

| Endpoint | Description |
|---|---|
| `GET /api/data` | All records as a JSON array |
| `GET /stream` | Server-Sent Events: one new record as JSON every `INTERVAL` seconds |

## Data dictionary

| Column | Meaning |
|---|---|
| `id` | Patient ID |
| `age` | Age in years |
| `ag` | Age group: 18-29, 30-44, 45-59, 60-74, 75+ |
| `g` | Gender |
| `dis` | Primary diagnosis |
| `fac` | Dialysis facility |
| `chain` | Chain organisation that owns the facility |
| `st` | Dialysis station (e.g. S3) |
| `pm` | Payment mode: Insurance, Government Scheme, Cash, Card, Corporate Tie-up |
| `mo` | Month index, 0 to 11 |
| `sess` | Number of dialysis sessions |
| `billed` | Amount billed (₹) |
| `paid` | Amount actually collected after discounts or reductions (₹) |
| `stations` | Number of stations at the facility |

The discount for a record is `billed - paid`, and the discount rate is `(billed - paid) / billed`.

## Using your own data

1. Replace `data/patients.csv` with a file that has the same columns.
2. If your category names differ (diseases, facilities, payment modes), update the lists at the top of `datagen.py` and the constants at the top of the script in `static/index.html`.
3. To stop the simulated live feed and show only your data, remove the line that starts the `producer` thread in `server.py`. To feed live data from a real source, have your system append rows to the CSV and push them to connected clients in the same way `producer` does.

## Notes

- Records added by the live feed are appended to `data/patients.csv`, so the file grows each time the server runs. Add `data/patients.csv` to `.gitignore` if you do not want to commit those rows, and run `python datagen.py` to reset it.
- The dashboard is built for demonstration and learning. It has no authentication and should not be exposed publicly with real patient data.

## Analysis covered

1. Patient and disease distribution by age and gender
2. Chain, facility and dialysis station utilisation
3. Payment mode split, discounts and the gap between billed and collected amounts
4. Insights and recommendations, such as rebalancing station load and reviewing high-discount facilities
