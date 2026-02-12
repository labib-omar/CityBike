# CityBike — Bike-Sharing Analytics Platform

A Python-based analytics platform for a fictional city bike-sharing service.
This project demonstrates object-oriented design, data analysis with Pandas & NumPy,
custom algorithms, and Matplotlib visualizations.

## Project Structure

```
citybike/
├── main.py              # Entry point — runs the full pipeline
├── models.py            # OOP domain classes (Entity, Bike, Station, …)
├── analyzer.py          # BikeShareSystem — data loading, cleaning, analytics
├── algorithms.py        # Custom sorting & searching + benchmarks
├── numerical.py         # NumPy computations (distances, stats, outliers)
├── visualization.py     # Matplotlib chart functions
├── pricing.py           # Strategy Pattern — pricing strategies
├── factories.py         # Factory Pattern — object creation from dicts
├── utils.py             # Validation & formatting helpers
├── generate_data.py     # Synthetic data generator (run once)
├── requirements.txt     # Python dependencies
├── data/
│   ├── trips.csv        # Raw trip data
│   ├── stations.csv     # Station metadata
│   └── maintenance.csv  # Maintenance records
├── output/
│   ├── summary_report.txt
│   ├── top_stations.csv
│   ├── top_users.csv
│   └── figures/         # Exported PNG charts
└── tests/
    ├── __init__.py
    └── test_models.py   # Unit tests (pytest)
```

## Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd citybike

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data (already included, or regenerate)
python generate_data.py

# 5. Run the pipeline
python main.py
```

## Running Tests

```bash
pytest tests/ -v
```

## Milestones

| # | Milestone               | Status |
|---|-------------------------|--------|
| 1 | Project Setup           | ✅     |
| 2 | Domain Models           | ✅     |
| 3 | Data Loading & Cleaning | ✅     |
| 4 | Algorithms              | ✅     |
| 5 | Numerical Computing     | ✅     |
| 6 | Analytics               | ✅     |
| 7 | Visualization           | ✅     |
| 8 | Polish & Delivery       | ✅     |

## Dependencies

- Python 3.10+
- pandas
- numpy
- matplotlib
- pytest *(optional, for unit tests)*

## License

For educational use only.
