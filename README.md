# Khawar Streamlit App

MRIO analysis application for emissions decomposition visualization.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Streamlit Web App

Run the interactive Streamlit app for emissions decomposition visualization:
```bash
streamlit run streamlit_app.py
```

The app provides:
- 🌍 Region selection dropdown
- 🏭 Sector selection dropdown
- 💨 Stressor selection dropdown
- 📊 Interactive pie chart visualization
- 📈 Detailed breakdown metrics

### Jupyter Notebook

Or open the Jupyter notebook for analysis:
```bash
jupyter notebook test_all_PIE_Chart_S3LAB_.ipynb
```

## Data Requirements

**Important:** Place your CSV data files in the `data/<year>/` folder structure.

For example, for 2022 data:
```
./data/2022/
├── S_2022_all_.csv
└── L_2022.csv
```

For other years, create the appropriate year folder:
```
./data/2023/
├── S_2023_all_.csv
└── L_2023.csv
```

The app will automatically detect and load data from the year-specific folders.

